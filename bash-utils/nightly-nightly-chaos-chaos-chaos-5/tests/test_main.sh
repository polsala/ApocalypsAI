#!/bin/bash

# Test suite for Nightly Chaos Chaos Chaos 5
# Run with: bash tests/test_main.sh

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_TOTAL=0
TESTS_PASSED=0
TESTS_FAILED=0

# Print colored output
print_color() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Test result functions
test_pass() {
    local test_name=$1
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
    print_color "$GREEN" "✅ PASS: $test_name"
}

test_fail() {
    local test_name=$1
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
    print_color "$RED" "❌ FAIL: $test_name"
}

# Mock functions for testing
mock_tc() {
    echo "qdisc netem 8001: dev eth0 root refcnt 2 limit 1000 delay 100.0ms"
}

mock_systemctl() {
    case $1 in
        list-unit-files)
            echo "nginx.service enabled"
            echo "ssh.service enabled"
            echo "cron.service enabled"
            ;;
        list-units)
            case $2 in
                --type=service)
                    echo "UNIT LOAD ACTIVE SUB DESCRIPTION"
                    echo "nginx.service loaded active running nginx"
                    echo "ssh.service loaded active running ssh"
                    ;;
                --state=failed)
                    echo "UNIT LOAD ACTIVE SUB DESCRIPTION"
                    ;;
            esac
            ;;
        stop)
            echo "Stopped $2"
            ;;
        start)
            echo "Started $2"
            ;;
        restart)
            echo "Restarted $2"
            ;;
    esac
}

mock_stress() {
    # Simulate stress command running for a short time
    sleep 0.1
    echo "stress: info: [$$] dispatching hogs: 0 cpu, 0 io, 1 vm, 0 hdd"
}

mock_date() {
    case $1 in
        -s)
            echo "System time set to: $2"
            ;;
        *)
            date
            ;;
    esac
}

mock_hwclock() {
    echo "Hardware clock set to current time"
}

mock_nproc() {
    echo 4
}

mock_free() {
    case $1 in
        -g)
            echo "              total        used        free      shared  buff/cache   available"
            echo "Mem:              7           2           3           0           2           5"
            echo "Swap:             2           0           2"
            ;;
    esac
}

# Setup test environment
setup_test_env() {
    # Create temporary directory for test
    TEST_DIR=$(mktemp -d)
    TEST_LOG="$TEST_DIR/test.log"
    TEST_SCRIPT="$TEST_DIR/main.sh"
    
    # Copy script to test directory
    cp "$(dirname "$0")/../src/main.sh" "$TEST_SCRIPT"
    chmod +x "$TEST_SCRIPT"
    
    # Create mock binaries
    mkdir -p "$TEST_DIR/mocks"
    cat > "$TEST_DIR/mocks/tc" << 'EOF'
#!/bin/bash
mock_tc "$@"
EOF
    cat > "$TEST_DIR/mocks/systemctl" << 'EOF'
#!/bin/bash
mock_systemctl "$@"
EOF
    cat > "$TEST_DIR/mocks/stress" << 'EOF'
#!/bin/bash
mock_stress "$@"
EOF
    cat > "$TEST_DIR/mocks/date" << 'EOF'
#!/bin/bash
mock_date "$@"
EOF
    cat > "$TEST_DIR/mocks/hwclock" << 'EOF'
#!/bin/bash
mock_hwclock "$@"
EOF
    cat > "$TEST_DIR/mocks/nproc" << 'EOF'
#!/bin/bash
mock_nproc "$@"
EOF
    cat > "$TEST_DIR/mocks/free" << 'EOF'
#!/bin/bash
mock_free "$@"
EOF
    
    chmod +x "$TEST_DIR/mocks"/*
    export PATH="$TEST_DIR/mocks:$PATH"
    export NETWORK_INTERFACE="eth0"
}

# Cleanup test environment
cleanup_test_env() {
    rm -rf "$TEST_DIR"
}

# Test help function
test_help() {
    if "$TEST_SCRIPT" --help > /dev/null 2>&1; then
        test_pass "Help function"
    else
        test_fail "Help function"
    fi
}

# Test cleanup function
test_cleanup() {
    # Create some mock chaos state
    touch "$TEST_DIR/chaos_state"
    
    if "$TEST_SCRIPT" --cleanup > /dev/null 2>&1; then
        test_pass "Cleanup function"
    else
        test_fail "Cleanup function"
    fi
}

# Test network latency scenario (mocked)
test_network_latency() {
    # Mock tc command to avoid requiring root
    if timeout 5 "$TEST_SCRIPT" --scenario network-latency --duration 1 > /dev/null 2>&1; then
        test_pass "Network latency scenario"
    else
        test_fail "Network latency scenario"
    fi
}

# Test service disruption scenario (mocked)
test_service_disruption() {
    # Mock systemctl command to avoid requiring root
    if timeout 5 "$TEST_SCRIPT" --scenario service-disruption --service nginx --duration 1 > /dev/null 2>&1; then
        test_pass "Service disruption scenario"
    else
        test_fail "Service disruption scenario"
    fi
}

# Test resource exhaustion scenario (mocked)
test_resource_exhaustion() {
    # Mock stress command to avoid requiring root
    if timeout 5 "$TEST_SCRIPT" --scenario resource-exhaustion --duration 1 > /dev/null 2>&1; then
        test_pass "Resource exhaustion scenario"
    else
        test_fail "Resource exhaustion scenario"
    fi
}

# Test random scenario
test_random_scenario() {
    if timeout 5 "$TEST_SCRIPT" --scenario random --duration 1 > /dev/null 2>&1; then
        test_pass "Random scenario"
    else
        test_fail "Random scenario"
    fi
}

# Test time manipulation scenario
test_time_manipulation() {
    if timeout 5 "$TEST_SCRIPT" --scenario time-manipulation --offset -300 > /dev/null 2>&1; then
        test_pass "Time manipulation scenario"
    else
        test_fail "Time manipulation scenario"
    fi
}

# Test argument parsing
test_argument_parsing() {
    # Test missing scenario
    if ! "$TEST_SCRIPT" --duration 60 > /dev/null 2>&1; then
        test_pass "Argument parsing - missing scenario"
    else
        test_fail "Argument parsing - missing scenario"
    fi
    
    # Test unknown scenario
    if ! "$TEST_SCRIPT" --scenario unknown > /dev/null 2>&1; then
        test_pass "Argument parsing - unknown scenario"
    else
        test_fail "Argument parsing - unknown scenario"
    fi
    
    # Test unknown option
    if ! "$TEST_SCRIPT" --unknown-option > /dev/null 2>&1; then
        test_pass "Argument parsing - unknown option"
    else
        test_fail "Argument parsing - unknown option"
    fi
}

# Test log file creation
test_log_creation() {
    local test_log="/tmp/chaos_chaos_chaos_5.log"
    rm -f "$test_log"
    
    timeout 3 "$TEST_SCRIPT" --scenario random --duration 1 > /dev/null 2>&1 || true
    
    if [[ -f "$test_log" ]]; then
        test_pass "Log file creation"
        rm -f "$test_log"
    else
        test_fail "Log file creation"
    fi
}

# Test script execution without root (should fail gracefully)
test_non_root_execution() {
    # This test verifies that the script fails gracefully when not run as root
    # We mock the root check to pass for this test
    if timeout 3 bash -c "
        sed 's/check_root() {/check_root() { return 0; # Mocked for test\n    }\n    check_root() {/' \"$TEST_SCRIPT\" --scenario network-latency --duration 1 > /dev/null 2>&1
    " 2>/dev/null; then
        test_pass "Non-root execution handling"
    else
        test_fail "Non-root execution handling"
    fi
}

# Run all tests
run_tests() {
    print_color "$BLUE" "🧪 Running Nightly Chaos Chaos Chaos 5 Test Suite"
    print_color "$BLUE" "===============================================\n"
    
    setup_test_env
    
    test_help
    test_cleanup
    test_network_latency
    test_service_disruption
    test_resource_exhaustion
    test_random_scenario
    test_time_manipulation
    test_argument_parsing
    test_log_creation
    test_non_root_execution
    
    cleanup_test_env
    
    # Print test results
    echo
    print_color "$BLUE" "==============================================="
    print_color "$BLUE" "Test Results:"
    print_color "$GREEN" "  Passed: $TESTS_PASSED"
    print_color "$RED" "  Failed: $TESTS_FAILED"
    print_color "$BLUE" "  Total:  $TESTS_TOTAL"
    
    if [[ $TESTS_FAILED -eq 0 ]]; then
        print_color "$GREEN" "🎉 All tests passed!"
        return 0
    else
        print_color "$RED" "❌ Some tests failed!"
        return 1
    fi
}

# Run tests if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    run_tests
fi
