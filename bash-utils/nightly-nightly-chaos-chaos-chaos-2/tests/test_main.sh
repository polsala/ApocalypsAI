#!/bin/bash

# Test script for Nightly Chaos Chaos Chaos
# This script tests the main functionality of the chaos engineering tool

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test results
TESTS_PASSED=0
TESTS_FAILED=0

# Print colored output
print_color() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Run a test
run_test() {
    local test_name=$1
    local test_command=$2
    local expected_result=${3:-0}
    
    print_color "$BLUE" "Running test: $test_name"
    
    # Set up mock environment
    export PATH="$(pwd)/tests/mocks:$PATH"
    
    # Run the test command
    if eval "$test_command"; then
        if [[ $expected_result -eq 0 ]]; then
            print_color "$GREEN" "✓ PASS: $test_name"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            print_color "$RED" "✗ FAIL: $test_name (expected failure but got success)"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    else
        if [[ $expected_result -ne 0 ]]; then
            print_color "$GREEN" "✓ PASS: $test_name (expected failure)"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            print_color "$RED" "✗ FAIL: $test_name (expected success but got failure)"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    fi
    
    echo
}

# Test help functionality
test_help() {
    run_test "Help display" "./src/main.sh help" 0
    run_test "Help with -h" "./src/main.sh -h" 0
    run_test "Help with --help" "./src/main.sh --help" 0
}

# Test argument validation
test_argument_validation() {
    run_test "Insufficient arguments" "./src/main.sh" 1
    run_test "Unknown chaos type" "./src/main.sh unknown subtype param" 1
    run_test "Unknown network subtype" "./src/main.sh network unknown param" 1
    run_test "Unknown resource subtype" "./src/main.sh resource unknown param" 1
    run_test "Unknown service subtype" "./src/main.sh service unknown param" 1
    run_test "Unknown time subtype" "./src/main.sh time unknown param" 1
}

# Test network chaos
test_network_chaos() {
    # Note: These tests will fail without root privileges, but we can test the validation
    run_test "Network latency validation" "timeout 2 ./src/main.sh network latency 100ms" 1
    run_test "Network packet loss validation" "timeout 2 ./src/main.sh network packet-loss 10%" 1
    run_test "Network bandwidth validation" "timeout 2 ./src/main.sh network bandwidth 1Mbps" 1
}

# Test resource chaos
test_resource_chaos() {
    # Note: These tests will fail without root privileges, but we can test the validation
    run_test "Resource CPU validation" "timeout 2 ./src/main.sh resource cpu 80" 1
    run_test "Resource memory validation" "timeout 2 ./src/main.sh resource memory 50" 1
}

# Test service chaos
test_service_chaos() {
    # Note: These tests will fail without root privileges, but we can test the validation
    run_test "Service restart validation" "timeout 2 ./src/main.sh service restart apache2" 1
    run_test "Service stop validation" "timeout 2 ./src/main.sh service stop nginx" 1
    run_test "Unknown service" "timeout 2 ./src/main.sh service restart nonexistent" 1
}

# Test time chaos
test_time_chaos() {
    run_test "Time shift forward" "./src/main.sh time shift +1h" 0
    run_test "Time shift backward" "./src/main.sh time shift -30m" 0
    run_test "Time shift seconds" "./src/main.sh time shift +120s" 0
    run_test "Invalid time format" "./src/main.sh time shift invalid" 1
}

# Test cleanup
test_cleanup() {
    run_test "Cleanup network" "./src/main.sh cleanup network" 0
    run_test "Cleanup resource" "./src/main.sh cleanup resource" 0
    run_test "Cleanup service" "./src/main.sh cleanup service" 0
    run_test "Cleanup time" "./src/main.sh cleanup time" 0
    run_test "Cleanup all" "./src/main.sh cleanup all" 0
    run_test "Unknown cleanup type" "./src/main.sh cleanup unknown" 1
}

# Test dry run mode
test_dry_run() {
    run_test "Dry run network" "./src/main.sh network latency 100ms --dry-run" 0
    run_test "Dry run resource" "./src/main.sh resource cpu 80 --dry-run" 0
    run_test "Dry run service" "./src/main.sh service restart apache2 --dry-run" 0
    run_test "Dry run time" "./src/main.sh time shift +1h --dry-run" 0
}

# Test file permissions and executability
test_file_permissions() {
    if [[ -x ./src/main.sh ]]; then
        print_color "$GREEN" "✓ PASS: main.sh is executable"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        print_color "$RED" "✗ FAIL: main.sh is not executable"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    
    if [[ -x ./tests/mocks/stress ]]; then
        print_color "$GREEN" "✓ PASS: mock stress is executable"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        print_color "$RED" "✗ FAIL: mock stress is not executable"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    
    if [[ -x ./tests/mocks/systemctl ]]; then
        print_color "$GREEN" "✓ PASS: mock systemctl is executable"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        print_color "$RED" "✗ FAIL: mock systemctl is not executable"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    
    if [[ -x ./tests/mocks/tc ]]; then
        print_color "$GREEN" "✓ PASS: mock tc is executable"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        print_color "$RED" "✗ FAIL: mock tc is not executable"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# Test log file creation
test_log_creation() {
    # Clean up any existing log
    rm -f /tmp/chaos_chaos_chaos.log
    rm -f /tmp/chaos_state.json
    
    # Run a simple command that should create logs
    ./src/main.sh help > /dev/null 2>&1 || true
    
    if [[ -f /tmp/chaos_chaos_chaos.log ]]; then
        print_color "$GREEN" "✓ PASS: Log file created"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        print_color "$RED" "✗ FAIL: Log file not created"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    
    if [[ -f /tmp/chaos_state.json ]]; then
        print_color "$GREEN" "✓ PASS: State file created"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        print_color "$RED" "✗ FAIL: State file not created"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# Test dependency checking (mocked)
test_dependency_checking() {
    # Test that the script can find mocked dependencies
    if command -v stress &> /dev/null; then
        print_color "$GREEN" "✓ PASS: Mock stress found"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        print_color "$RED" "✗ FAIL: Mock stress not found"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    
    if command -v systemctl &> /dev/null; then
        print_color "$GREEN" "✓ PASS: Mock systemctl found"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        print_color "$RED" "✗ FAIL: Mock systemctl not found"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    
    if command -v tc &> /dev/null; then
        print_color "$GREEN" "✓ PASS: Mock tc found"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        print_color "$RED" "✗ FAIL: Mock tc not found"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# Main test execution
main() {
    print_color "$YELLOW" "======================================="
    print_color "$YELLOW" "Nightly Chaos Chaos Chaos Test Suite"
    print_color "$YELLOW" "======================================="
    echo
    
    # Make scripts executable
    chmod +x ./src/main.sh
    chmod +x ./tests/mocks/stress
    chmod +x ./tests/mocks/systemctl
    chmod +x ./tests/mocks/tc
    
    # Set up mock PATH
    export PATH="$(pwd)/tests/mocks:$PATH"
    
    # Run all tests
    test_help
    test_argument_validation
    test_network_chaos
    test_resource_chaos
    test_service_chaos
    test_time_chaos
    test_cleanup
    test_dry_run
    test_file_permissions
    test_log_creation
    test_dependency_checking
    
    # Print results
    print_color "$YELLOW" "======================================="
    print_color "$YELLOW" "Test Results"
    print_color "$YELLOW" "======================================="
    print_color "$GREEN" "Tests Passed: $TESTS_PASSED"
    print_color "$RED" "Tests Failed: $TESTS_FAILED"
    print_color "$YELLOW" "Total Tests: $((TESTS_PASSED + TESTS_FAILED))"
    echo
    
    if [[ $TESTS_FAILED -eq 0 ]]; then
        print_color "$GREEN" "🎉 All tests passed!"
        exit 0
    else
        print_color "$RED" "❌ Some tests failed!"
        exit 1
    fi
}

# Run the test suite
main
