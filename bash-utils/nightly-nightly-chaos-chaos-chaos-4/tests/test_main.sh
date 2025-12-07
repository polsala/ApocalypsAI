#!/bin/bash

# Tests for Nightly Chaos Chaos Chaos
# These tests use mocked commands to avoid actual system modifications

set -euo pipefail

# Setup mocks directory
MOCKS_DIR="/tmp/test_mocks"
export PATH="$MOCKS_DIR:$PATH"

# Create mocks directory
mkdir -p "$MOCKS_DIR"

# Mock tc command - # Mock rationale: Simulates traffic control without actual network changes
create_mock_tc() {
    cat > "$MOCKS_DIR/tc" << 'EOF'
#!/bin/bash
# Mock tc command that simulates success without actual changes
if [[ "$1" == "qdisc" && "$2" == "add" ]]; then
    echo "Mock: Added qdisc rule"
    exit 0
elif [[ "$1" == "qdisc" && "$2" == "del" ]]; then
    echo "Mock: Deleted qdisc rule"
    exit 0
else
    echo "Mock: tc $*"
    exit 0
fi
EOF
    chmod +x "$MOCKS_DIR/tc"
}

# Mock systemctl command - # Mock rationale: Simulates service management without actual service changes
create_mock_systemctl() {
    cat > "$MOCKS_DIR/systemctl" << 'EOF'
#!/bin/bash
# Mock systemctl command that simulates success without actual changes
if [[ "$1" == "list-units" ]]; then
    echo "mock-service1.service loaded active running Mock Service 1"
    echo "mock-service2.service loaded active running Mock Service 2"
    echo "mock-service3.service loaded active running Mock Service 3"
    exit 0
elif [[ "$1" == "restart" || "$1" == "stop" || "$1" == "start" ]]; then
    echo "Mock: $1 $2"
    exit 0
else
    echo "Mock: systemctl $*"
    exit 0
fi
EOF
    chmod +x "$MOCKS_DIR/systemctl"
}

# Mock stress command - # Mock rationale: Simulates resource stress without actual CPU/memory consumption
create_mock_stress() {
    cat > "$MOCKS_DIR/stress" << 'EOF'
#!/bin/bash
# Mock stress command that simulates success without actual resource consumption
echo "Mock: stress $*"
# Simulate running for a short time then exiting
sleep 0.1
exit 0
EOF
    chmod +x "$MOCKS_DIR/stress"
}

# Mock date command - # Mock rationale: Simulates time changes without actual system time modification
create_mock_date() {
    cat > "$MOCKS_DIR/date" << 'EOF'
#!/bin/bash
# Mock date command that simulates time changes without actual modification
if [[ "$1" == "-s" ]]; then
    echo "Mock: Set time to $2"
    exit 0
else
    # Return current time
    /bin/date "$@"
    exit 0
fi
EOF
    chmod +x "$MOCKS_DIR/date"
}

# Mock timedatectl command - # Mock rationale: Simulates time synchronization without actual changes
create_mock_timedatectl() {
    cat > "$MOCKS_DIR/timedatectl" << 'EOF'
#!/bin/bash
# Mock timedatectl command
echo "Mock: timedatectl $*"
exit 0
EOF
    chmod +x "$MOCKS_DIR/timedatectl"
}

# Mock ntpdate command - # Mock rationale: Simulates NTP synchronization without actual network calls
create_mock_ntpdate() {
    cat > "$MOCKS_DIR/ntpdate" << 'EOF'
#!/bin/bash
# Mock ntpdate command
echo "Mock: ntpdate $*"
exit 0
EOF
    chmod +x "$MOCKS_DIR/ntpdate"
}

# Mock pkill command - # Mock rationale: Simulates process killing without actual process termination
create_mock_pkill() {
    cat > "$MOCKS_DIR/pkill" << 'EOF'
#!/bin/bash
# Mock pkill command
echo "Mock: pkill $*"
exit 0
EOF
    chmod +x "$MOCKS_DIR/pkill"
}

# Load the main script functions for testing
load_main_script() {
    # Source the main script but disable execution
    export TEST_MODE=1
    # Mock sudo/root check
    check_root() { return 0; }
    # Source the script
    source "$(dirname "$0")/../src/main.sh"
}

# Test helper functions
run_test() {
    local test_name="$1"
    local test_func="$2"
    
    echo -n "Running $test_name... "
    if $test_func; then
        echo "✓ PASS"
        return 0
    else
        echo "✗ FAIL"
        return 1
    fi
}

# Test functions
test_network_chaos() {
    apply_network_chaos "eth0" 100 5 100
    return 0
}

test_service_chaos_restart() {
    apply_service_chaos "restart" "mock-service"
    return 0
}

test_service_chaos_random() {
    apply_service_chaos "restart"
    return 0
}

test_resource_chaos() {
    apply_resource_chaos 2 1 5
    return 0
}

test_time_chaos() {
    apply_time_chaos -1
    return 0
}

test_random_chaos() {
    apply_random_chaos
    return 0
}

test_cleanup_network() {
    cleanup_network "eth0"
    return 0
}

test_cleanup_services() {
    cleanup_services
    return 0
}

test_cleanup_resources() {
    cleanup_resources
    return 0
}

test_cleanup_time() {
    cleanup_time
    return 0
}

test_cleanup_all() {
    cleanup_all
    return 0
}

test_help() {
    show_help > /dev/null
    return 0
}

test_argument_parsing() {
    # Test that argument parsing doesn't crash
    parse_args --help > /dev/null
    parse_args --network --interface eth0 --latency 50 > /dev/null
    parse_args --services --action restart --service test > /dev/null
    parse_args --resources --cpu 2 --memory 1 --timeout 30 > /dev/null
    parse_args --time --offset -1 > /dev/null
    parse_args --random > /dev/null
    parse_args --cleanup > /dev/null
    return 0
}

# Setup and run tests
setup() {
    create_mock_tc
    create_mock_systemctl
    create_mock_stress
    create_mock_date
    create_mock_timedatectl
    create_mock_ntpdate
    create_mock_pkill
    load_main_script
}

cleanup() {
    rm -rf "$MOCKS_DIR"
}

# Run all tests
main() {
    echo "Setting up test environment..."
    setup
    
    echo "Running tests..."
    local failed=0
    
    run_test "Network Chaos" test_network_chaos || failed=$((failed + 1))
    run_test "Service Chaos (Restart)" test_service_chaos_restart || failed=$((failed + 1))
    run_test "Service Chaos (Random)" test_service_chaos_random || failed=$((failed + 1))
    run_test "Resource Chaos" test_resource_chaos || failed=$((failed + 1))
    run_test "Time Chaos" test_time_chaos || failed=$((failed + 1))
    run_test "Random Chaos" test_random_chaos || failed=$((failed + 1))
    run_test "Cleanup Network" test_cleanup_network || failed=$((failed + 1))
    run_test "Cleanup Services" test_cleanup_services || failed=$((failed + 1))
    run_test "Cleanup Resources" test_cleanup_resources || failed=$((failed + 1))
    run_test "Cleanup Time" test_cleanup_time || failed=$((failed + 1))
    run_test "Cleanup All" test_cleanup_all || failed=$((failed + 1))
    run_test "Help" test_help || failed=$((failed + 1))
    run_test "Argument Parsing" test_argument_parsing || failed=$((failed + 1))
    
    cleanup
    
    echo ""
    if [[ $failed -eq 0 ]]; then
        echo "All tests passed! ✓"
        exit 0
    else
        echo "$failed test(s) failed ✗"
        exit 1
    fi
}

# Run tests if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
