#!/bin/bash

# Tests for Nightly Nightly Chaos Chaos Chaos
# These tests use mocked dependencies to ensure they run deterministically

set -euo pipefail

# Test directory
TEST_DIR="/tmp/chaos_test"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/src/main.sh"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_test() {
    echo -e "${YELLOW}[TEST]${NC} $1"
}

print_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

print_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
}

# Setup test environment with mocks
setup_test_env() {
    print_test "Setting up test environment..."
    
    # Create test directory
    mkdir -p "$TEST_DIR"
    mkdir -p "$TEST_DIR/bin"
    mkdir -p "$TEST_DIR/etc"
    
    # Create mock systemctl
    cat > "$TEST_DIR/bin/systemctl" << 'EOF'
#!/bin/bash
# Mock systemctl for testing

# Mock available services
AVAILABLE_SERVICES="nginx.service\nssh.service\napache2.service\nmysql.service\nredis.service"

if [[ "$1" == "list-unit-files" && "$2" == "--type=service" ]]; then
    if [[ "$3" == "--state=enabled" ]]; then
        echo "UNIT FILE         STATE"
        echo "$AVAILABLE_SERVICES"
    else
        echo "UNIT FILE         STATE"
        echo "$AVAILABLE_SERVICES"
    fi
elif [[ "$1" == "list-units" && "$2" == "--type=service" ]]; then
    if [[ "$3" == "--state=failed" ]]; then
        echo "UNIT         LOAD   ACTIVE SUB    DESCRIPTION"
        echo "0 loaded units listed."
    fi
elif [[ "$1" == "restart" || "$1" == "stop" || "$1" == "start" || "$1" == "reload" ]]; then
    echo "$1 $2"
    exit 0
fi
EOF
    chmod +x "$TEST_DIR/bin/systemctl"
    
    # Create mock tc
    cat > "$TEST_DIR/bin/tc" << 'EOF'
#!/bin/bash
# Mock tc for testing

if [[ "$1" == "qdisc" ]]; then
    if [[ "$2" == "show" ]]; then
        echo "qdisc noqueue 0: root refcnt 2"
    elif [[ "$2" == "del" ]]; then
        echo "Success"
    elif [[ "$2" == "add" ]]; then
        echo "Success"
    fi
fi
exit 0
EOF
    chmod +x "$TEST_DIR/bin/tc"
    
    # Create mock stress
    cat > "$TEST_DIR/bin/stress" << 'EOF'
#!/bin/bash
# Mock stress for testing

# Parse arguments
CPU_CORES=0
MEMORY_MB=0
TIMEOUT=0

while [[ $# -gt 0 ]]; do
    case $1 in
        --cpu)
            CPU_CORES="$2"
            shift 2
            ;;
        --vm)
            VM_PROCESSES="$2"
            shift 2
            ;;
        --vm-bytes)
            MEMORY_MB="$2"
            shift 2
            ;;
        --timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        --verbose)
            shift
            ;;
        *)
            shift
            ;;
esac
done

# Simulate stress by sleeping
sleep ${TIMEOUT:-1} &
STRESS_PID=$!
echo "Stress PID: $STRESS_PID" >&2
wait $STRESS_PID
EOF
    chmod +x "$TEST_DIR/bin/stress"
    
    # Backup PATH and add test bin to front
    export ORIGINAL_PATH="$PATH"
    export PATH="$TEST_DIR/bin:$PATH"
    
    print_pass "Test environment setup complete"
}

# Cleanup test environment
cleanup_test_env() {
    print_test "Cleaning up test environment..."
    
    # Kill any background processes
    pkill -f "sleep" 2>/dev/null || true
    
    # Restore PATH
    export PATH="$ORIGINAL_PATH"
    
    # Remove test directory
    rm -rf "$TEST_DIR"
    
    print_pass "Test environment cleaned up"
}

# Test script execution
test_script_exists() {
    print_test "Testing script exists..."
    if [[ -f "$SCRIPT_PATH" ]]; then
        print_pass "Script exists at $SCRIPT_PATH"
    else
        print_fail "Script not found at $SCRIPT_PATH"
        exit 1
    fi
}

test_help_output() {
    print_test "Testing help output..."
    local help_output
    help_output=$(bash "$SCRIPT_PATH" --help 2>&1)
    
    if echo "$help_output" | grep -q "Usage:"; then
        print_pass "Help output contains usage information"
    else
        print_fail "Help output missing usage information"
        echo "Help output: $help_output"
        return 1
    fi
}

test_network_chaos() {
    print_test "Testing network chaos..."
    
    # Test network chaos application
    local network_output
    network_output=$(bash "$SCRIPT_PATH" --chaos network --latency 50 --packet-loss 2 --duration 1 2>&1)
    
    if echo "$network_output" | grep -q "Network chaos applied"; then
        print_pass "Network chaos applied successfully"
    else
        print_fail "Network chaos failed to apply"
        echo "Network output: $network_output"
        return 1
    fi
}

test_service_chaos() {
    print_test "Testing service chaos..."
    
    # Test service chaos application
    local service_output
    service_output=$(bash "$SCRIPT_PATH" --chaos service --services nginx,ssh --duration 1 2>&1)
    
    if echo "$service_output" | grep -q "Service chaos applied"; then
        print_pass "Service chaos applied successfully"
    else
        print_fail "Service chaos failed to apply"
        echo "Service output: $service_output"
        return 1
    fi
}

test_resource_chaos() {
    print_test "Testing resource chaos..."
    
    # Test resource chaos application
    local resource_output
    resource_output=$(bash "$SCRIPT_PATH" --chaos resource --cpu 50 --memory 256 --duration 1 2>&1)
    
    if echo "$resource_output" | grep -q "Resource chaos applied"; then
        print_pass "Resource chaos applied successfully"
    else
        print_fail "Resource chaos failed to apply"
        echo "Resource output: $resource_output"
        return 1
    fi
}

test_time_chaos() {
    print_test "Testing time chaos..."
    
    # Test time chaos application
    local time_output
    time_output=$(bash "$SCRIPT_PATH" --chaos time --time-shift 60 --duration 1 2>&1)
    
    if echo "$time_output" | grep -q "Time chaos applied"; then
        print_pass "Time chaos applied successfully"
    else
        print_fail "Time chaos failed to apply"
        echo "Time output: $time_output"
        return 1
    fi
}

test_cleanup() {
    print_test "Testing cleanup..."
    
    # Test cleanup functionality
    local cleanup_output
    cleanup_output=$(bash "$SCRIPT_PATH" --cleanup 2>&1)
    
    if echo "$cleanup_output" | grep -q "All chaos cleaned up"; then
        print_pass "Cleanup executed successfully"
    else
        print_fail "Cleanup failed"
        echo "Cleanup output: $cleanup_output"
        return 1
    fi
}

test_list_services() {
    print_test "Testing list services..."
    
    # Test list services functionality
    local list_output
    list_output=$(bash "$SCRIPT_PATH" --list 2>&1)
    
    if echo "$list_output" | grep -q "Available services"; then
        print_pass "List services executed successfully"
    else
        print_fail "List services failed"
        echo "List output: $list_output"
        return 1
    fi
}

test_invalid_chaos_type() {
    print_test "Testing invalid chaos type..."
    
    # Test invalid chaos type
    local invalid_output
    invalid_output=$(bash "$SCRIPT_PATH" --chaos invalid 2>&1 || true)
    
    if echo "$invalid_output" | grep -q "Invalid chaos type"; then
        print_pass "Invalid chaos type handled correctly"
    else
        print_fail "Invalid chaos type not handled properly"
        echo "Invalid output: $invalid_output"
        return 1
    fi
}

test_missing_chaos_argument() {
    print_test "Testing missing chaos argument..."
    
    # Test missing chaos argument
    local missing_output
    missing_output=$(bash "$SCRIPT_PATH" 2>&1 || true)
    
    if echo "$missing_output" | grep -q "--chaos option is required"; then
        print_pass "Missing chaos argument handled correctly"
    else
        print_fail "Missing chaos argument not handled properly"
        echo "Missing output: $missing_output"
        return 1
    fi
}

# Run all tests
run_tests() {
    print_test "Running all tests..."
    
    test_script_exists
    test_help_output
    test_network_chaos
    test_service_chaos
    test_resource_chaos
    test_time_chaos
    test_cleanup
    test_list_services
    test_invalid_chaos_type
    test_missing_chaos_argument
    
    print_pass "All tests completed successfully!"
}

# Main execution
main() {
    print_test "Starting Chaos Chaos Chaos test suite..."
    
    setup_test_env
    
    # Run tests and capture result
    local test_result=0
    run_tests || test_result=$?
    
    cleanup_test_env
    
    if [[ $test_result -eq 0 ]]; then
        print_pass "All tests passed!"
        exit 0
    else
        print_fail "Some tests failed!"
        exit 1
    fi
}

# Execute main
main "$@"
