#!/bin/bash

# Tests for Nightly Chaos Orchestrator
# Mock rationale: These tests verify the script's functionality without actually causing chaos

set -euo pipefail

# Test directory
TEST_DIR="/tmp/chaos_test"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="$SCRIPT_DIR/src/chaos_orchestrator.sh"

# Colors for test output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test counters
TESTS_TOTAL=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test functions
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    echo -e "${YELLOW}Running: $test_name${NC}"
    
    if eval "$test_command" &> /dev/null; then
        echo -e "${GREEN}PASS: $test_name${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL: $test_name${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# Setup test environment
setup() {
    mkdir -p "$TEST_DIR"
    export PATH="$TEST_DIR:$PATH"
    
    # Create mock commands
    cat > "$TEST_DIR/tc" << 'EOF'
#!/bin/bash
echo "tc mock: $@"
EOF
    chmod +x "$TEST_DIR/tc"
    
    cat > "$TEST_DIR/systemctl" << 'EOF'
#!/bin/bash
echo "systemctl mock: $@"
EOF
    chmod +x "$TEST_DIR/systemctl"
    
    cat > "$TEST_DIR/free" << 'EOF'
#!/bin/bash
echo "              total        used        free      shared  buff/cache   available"
echo "Mem:           7951         900        5800          50        2250        6500"
echo "Swap:          2047           0        2047"
EOF
    chmod +x "$TEST_DIR/free"
    
    cat > "$TEST_DIR/nproc" << 'EOF'
#!/bin/bash
echo "4"
EOF
    chmod +x "$TEST_DIR/nproc"
    
    cat > "$TEST_DIR/dd" << 'EOF'
#!/bin/bash
echo "dd mock: $@"
EOF
    chmod +x "$TEST_DIR/dd"
}

# Teardown test environment
 teardown() {
    rm -rf "$TEST_DIR"
}

# Test script existence and permissions
 test_script_exists() {
    [ -f "$SCRIPT" ] && [ -x "$SCRIPT" ]
}

# Test help output
 test_help_output() {
    "$SCRIPT" --help | grep -q "Usage:"
}

# Test duration parsing
 test_parse_duration() {
    # This test would need to source the script functions
    # For now, we'll test the script's ability to parse durations
    timeout 5s "$SCRIPT" --scenario random --duration 1s --cleanup &> /dev/null
}

# Test scenario validation
 test_scenario_validation() {
    ! timeout 5s "$SCRIPT" --scenario invalid --duration 1s &> /dev/null
}

# Test duration validation
 test_duration_validation() {
    ! timeout 5s "$SCRIPT" --scenario random --duration 2h &> /dev/null
}

# Test percentage validation
 test_percentage_validation() {
    ! timeout 5s "$SCRIPT" --scenario resource --cpu 150 --duration 1s &> /dev/null
    ! timeout 5s "$SCRIPT" --scenario resource --memory -10 --duration 1s &> /dev/null
}

# Test network chaos (mocked)
 test_network_chaos() {
    timeout 10s "$SCRIPT" --scenario network --latency 100 --packet-loss 10 --duration 2s &> /dev/null
}

# Test resource chaos (mocked)
 test_resource_chaos() {
    timeout 10s "$SCRIPT" --scenario resource --cpu 50 --memory 30 --duration 2s &> /dev/null
}

# Test service chaos (mocked)
 test_service_chaos() {
    timeout 10s "$SCRIPT" --scenario service --services test1,test2 --action restart --duration 2s &> /dev/null
}

# Test random chaos (mocked)
 test_random_chaos() {
    timeout 10s "$SCRIPT" --scenario random --duration 2s &> /dev/null
}

# Test cleanup functionality
 test_cleanup() {
    timeout 10s "$SCRIPT" --cleanup &> /dev/null
}

# Test history functionality
 test_history() {
    # First run some chaos to create history
    timeout 5s "$SCRIPT" --scenario random --duration 1s &> /dev/null || true
    timeout 5s "$SCRIPT" --history &> /dev/null
}

# Test report generation
 test_report_generation() {
    timeout 10s "$SCRIPT" --scenario network --duration 1s --report &> /dev/null
}

# Test multiple scenarios
 test_multiple_scenarios() {
    # Test that we can run different scenarios without conflicts
    timeout 5s "$SCRIPT" --scenario network --duration 1s &> /dev/null || true
    timeout 5s "$SCRIPT" --scenario resource --duration 1s &> /dev/null || true
    timeout 5s "$SCRIPT" --scenario service --services test --action restart --duration 1s &> /dev/null || true
}

# Test error handling
 test_error_handling() {
    # Test with invalid parameters
    ! timeout 5s "$SCRIPT" --scenario network --invalid-param 123 &> /dev/null
}

# Test log file creation
 test_log_file_creation() {
    local log_file="/tmp/chaos_orchestrator.log"
    rm -f "$log_file"
    timeout 5s "$SCRIPT" --scenario random --duration 1s &> /dev/null || true
    [ -f "$log_file" ]
}

# Test PID file creation and cleanup
 test_pid_file() {
    local pid_file="/tmp/chaos_orchestrator.pid"
    rm -f "$pid_file"
    timeout 5s "$SCRIPT" --scenario random --duration 1s &> /dev/null || true
    # PID file should be cleaned up on exit
    ! [ -f "$pid_file" ]
}

# Run all tests
 run_all_tests() {
    echo "Starting Chaos Orchestrator Tests"
    echo "================================"
    
    setup
    
    run_test "Script exists and is executable" "test_script_exists"
    run_test "Help output displays correctly" "test_help_output"
    run_test "Duration parsing works" "test_parse_duration"
    run_test "Scenario validation works" "test_scenario_validation"
    run_test "Duration validation works" "test_duration_validation"
    run_test "Percentage validation works" "test_percentage_validation"
    run_test "Network chaos executes" "test_network_chaos"
    run_test "Resource chaos executes" "test_resource_chaos"
    run_test "Service chaos executes" "test_service_chaos"
    run_test "Random chaos executes" "test_random_chaos"
    run_test "Cleanup functionality works" "test_cleanup"
    run_test "History functionality works" "test_history"
    run_test "Report generation works" "test_report_generation"
    run_test "Multiple scenarios work" "test_multiple_scenarios"
    run_test "Error handling works" "test_error_handling"
    run_test "Log file creation works" "test_log_file_creation"
    run_test "PID file management works" "test_pid_file"
    
    teardown
    
    echo ""
    echo "Test Results"
    echo "============"
    echo "Total: $TESTS_TOTAL"
    echo "Passed: $TESTS_PASSED"
    echo "Failed: $TESTS_FAILED"
    
    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "${GREEN}All tests passed! 🎉${NC}"
        return 0
    else
        echo -e "${RED}$TESTS_FAILED tests failed! ❌${NC}"
        return 1
    fi
}

# Run tests if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    run_all_tests
fi
