#!/bin/bash

# Tests for nightly-sys-health-check

# Source the script to be tested (assuming it's in the same directory or a known path)
# In a real scenario, you might use a more robust way to source or execute.
SCRIPT_DIR=$(dirname "$0")
SOURCE_SCRIPT="$SCRIPT_DIR/../src/main.sh"

# Mock rationale: We are mocking environment variables and command outputs to ensure deterministic tests.

# Function to run a test case
run_test() {
    local test_name="$1"
    local expected_output="$2"
    local script_to_run="$3"
    local mock_vars="$4"

    echo "Running test: $test_name"

    # Execute the script with mocked variables
    # The eval is used to correctly set multiple mock variables
    eval "$mock_vars $script_to_run" > test_output.txt 2>&1

    # Check if the output matches the expected output
    if grep -qF "$expected_output" test_output.txt; then
        echo "  PASSED"
    else
        echo "  FAILED"
        echo "    Expected to find: '$expected_output'"
        echo "    Actual output:"
        cat test_output.txt
        return 1 # Indicate failure
    fi
    rm test_output.txt
    return 0 # Indicate success
}

# --- Test Cases ---

all_tests_passed=true

# Test Case 1: All systems nominal (low disk, low memory, normal processes)

# Mock rationale: Simulate low disk usage (e.g., 30%), low memory usage (e.g., 40%), and a normal process count (e.g., 150).
# The `df` and `free` commands are mocked by setting environment variables.
# The `ps aux | wc -l` command is mocked by setting MOCK_PROCESS_COUNT.
MOCK_VARS_CASE1="MOCK_DISK_USAGE=30 MOCK_MEMORY_USAGE=40 MOCK_PROCESS_COUNT=150"
run_test "All Systems Nominal" "[SURVIVAL CONFIRMED] Disk space is sufficient for the last stand!" "bash $SOURCE_SCRIPT" "$MOCK_VARS_CASE1" || all_tests_passed=false
run_test "All Systems Nominal" "[SURVIVAL CONFIRMED] Memory usage is nominal. Plenty of RAM for your escape pod!" "bash $SOURCE_SCRIPT" "$MOCK_VARS_CASE1" || all_tests_passed=false
run_test "All Systems Nominal" "[INFO] Process count is within expected limits (150). All systems nominal." "bash $SOURCE_SCRIPT" "$MOCK_VARS_CASE1" || all_tests_passed=false

# Test Case 2: High disk usage

# Mock rationale: Simulate high disk usage (e.g., 90%).
MOCK_VARS_CASE2="MOCK_DISK_USAGE=90 MOCK_MEMORY_USAGE=50 MOCK_PROCESS_COUNT=100"
run_test "High Disk Usage" "[IMMINENT DOOM] Disk space is critically low! Prepare for resource rationing! (90% used)" "bash $SOURCE_SCRIPT" "$MOCK_VARS_CASE2" || all_tests_passed=false

# Test Case 3: High memory usage

# Mock rationale: Simulate high memory usage (e.g., 85%).
MOCK_VARS_CASE3="MOCK_DISK_USAGE=50 MOCK_MEMORY_USAGE=85 MOCK_PROCESS_COUNT=120"
run_test "High Memory Usage" "[IMMINENT DOOM] Memory usage is critical! Your system is struggling to keep up with the apocalypse! (85% used)" "bash $SOURCE_SCRIPT" "$MOCK_VARS_CASE3" || all_tests_passed=false

# Test Case 4: Warning disk usage

# Mock rationale: Simulate warning disk usage (e.g., 80%).
MOCK_VARS_CASE4="MOCK_DISK_USAGE=80 MOCK_MEMORY_USAGE=60 MOCK_PROCESS_COUNT=130"
run_test "Warning Disk Usage" "[CAUTION ADVISED] Disk space is getting tight. Consider clearing out old bunkers. (80% used)" "bash $SOURCE_SCRIPT" "$MOCK_VARS_CASE4" || all_tests_passed=false

# Test Case 5: Warning memory usage

# Mock rationale: Simulate warning memory usage (e.g., 75%).
MOCK_VARS_CASE5="MOCK_DISK_USAGE=60 MOCK_MEMORY_USAGE=75 MOCK_PROCESS_COUNT=140"
run_test "Warning Memory Usage" "[CAUTION ADVISED] Memory usage is high. Consider shutting down non-essential operations. (75% used)" "bash $SOURCE_SCRIPT" "$MOCK_VARS_CASE5" || all_tests_passed=false

# Test Case 6: High process count

# Mock rationale: Simulate a high process count (e.g., 250).
MOCK_VARS_CASE6="MOCK_DISK_USAGE=40 MOCK_MEMORY_USAGE=50 MOCK_PROCESS_COUNT=250"
run_test "High Process Count" "[CAUTION ADVISED] High number of running processes detected (250). Potential resource drain or unexpected activity." "bash $SOURCE_SCRIPT" "$MOCK_VARS_CASE6" || all_tests_passed=false

# --- Summary ---

if [ "$all_tests_passed" = true ]; then
    echo "\nAll tests passed! The system is ready for the apocalypse (or at least a Tuesday)."
    exit 0
else
    echo "\nSome tests failed. The apocalypse might be a bit more chaotic than expected."
    exit 1
fi
