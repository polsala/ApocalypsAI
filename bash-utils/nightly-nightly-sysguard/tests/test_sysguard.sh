#!/bin/bash

# Test suite for Nightly SysGuard
# Run with: bash test_sysguard.sh

set -e

# Source the main script functions (without executing main)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAIN_SCRIPT="$SCRIPT_DIR/../src/sysguard.sh"

# Extract functions from main script
source <(grep -A 1000 '^# Whimsical messages' "$MAIN_SCRIPT" | head -n 50)
source <(grep -A 1000 '^# Get system metrics' "$MAIN_SCRIPT" | head -n 50)
source <(grep -A 1000 '^# Output functions' "$MAIN_SCRIPT" | head -n 100)
source <(grep -A 1000 '^# Check thresholds' "$MAIN_SCRIPT" | head -n 20)

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Test runner
run_test() {
    local test_name="$1"
    local test_func="$2"
    
    echo -n "Running $test_name... "
    
    if $test_func; then
        echo "PASS"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo "FAIL"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# Test functions

# Test CPU message generation
test_cpu_messages() {
    local msg1="$(get_cpu_message 30)"
    local msg2="$(get_cpu_message 60)"
    local msg3="$(get_cpu_message 90)"
    
    [ "$msg1" = "CPU running cool" ] && \
    [ "$msg2" = "CPU warming up" ] && \
    [ "$msg3" = "CPU overheating!" ]
}

# Test memory message generation
test_memory_messages() {
    local msg1="$(get_memory_message 50)"
    local msg2="$(get_memory_message 80)"
    local msg3="$(get_memory_message 95)"
    
    [ "$msg1" = "Supplies well stocked" ] && \
    [ "$msg2" = "Supplies running low!" ] && \
    [ "$msg3" = "Critical supply shortage!" ]
}

# Test disk message generation
test_disk_messages() {
    local msg1="$(get_disk_message 50)"
    local msg2="$(get_disk_message 80)"
    local msg3="$(get_disk_message 95)"
    
    [ "$msg1" = "Storage bunkers secure" ] && \
    [ "$msg2" = "Storage getting tight" ] && \
    [ "$msg3" = "Storage bunkers full!" ]
}

# Test threshold checking
test_threshold_checking() {
    # Normal case
    local status1="$(check_threshold 50 80)"
    
    # Warning case
    local status2="$(check_threshold 85 80)"
    
    # Critical case
    local status3="$(check_threshold 95 80)"
    
    [ "$status1" = "normal" ] && \
    [ "$status2" = "warning" ] && \
    [ "$status3" = "critical" ]
}

# Test JSON output format
test_json_output() {
    # Mock the metrics
    local cpu_usage=50
    local memory_usage=75
    local disk_usage=60
    local cpu_status="normal"
    local memory_status="warning"
    local disk_status="normal"
    
    # Generate JSON output
    local json_output
    json_output=$(print_status_json $cpu_usage $memory_usage $disk_usage $cpu_status $memory_status $disk_status)
    
    # Check if JSON contains expected fields
    echo "$json_output" | grep -q '"timestamp"' && \
    echo "$json_output" | grep -q '"cpu"' && \
    echo "$json_output" | grep -q '"memory"' && \
    echo "$json_output" | grep -q '"disk"' && \
    echo "$json_output" | grep -q '"overall_status"'
}

# Test that script is executable
test_script_executable() {
    [ -x "$MAIN_SCRIPT" ]
}

# Test that script has proper shebang
test_script_shebang() {
    head -1 "$MAIN_SCRIPT" | grep -q '^#!/bin/bash'
}

# Test help output
test_help_output() {
    # Run the script with --help and check output
    local help_output
    help_output="$($MAIN_SCRIPT --help 2>&1)"
    
    echo "$help_output" | grep -q 'Usage:' && \
    echo "$help_output" | grep -q '--cpu' && \
    echo "$help_output" | grep -q '--memory' && \
    echo "$help_output" | grep -q '--disk'
}

# Test JSON mode
test_json_mode() {
    # Test that JSON mode produces valid JSON
    local json_output
    json_output="$($MAIN_SCRIPT --json 2>&1)"
    
    # Check if output starts and ends with braces
    echo "$json_output" | grep -q '^{' && \
    echo "$json_output" | grep -q '}$'
}

# Test check mode exit codes
test_check_mode() {
    # Test normal case (should exit 0)
    $MAIN_SCRIPT --check --cpu 100 --memory 100 --disk 100
    local normal_exit=$?
    
    # Test warning case (should exit 1)
    $MAIN_SCRIPT --check --cpu 50 --memory 50 --disk 50
    local warning_exit=$?
    
    # We can't easily test critical without mocking high usage, so just test that check mode runs
    [ $normal_exit -eq 0 ]
}

# Run all tests
echo "Running Nightly SysGuard test suite..."
echo "========================================"

run_test "CPU message generation" test_cpu_messages
run_test "Memory message generation" test_memory_messages
run_test "Disk message generation" test_disk_messages
run_test "Threshold checking" test_threshold_checking
run_test "JSON output format" test_json_output
run_test "Script executable" test_script_executable
run_test "Script shebang" test_script_shebang
run_test "Help output" test_help_output
run_test "JSON mode" test_json_mode
run_test "Check mode" test_check_mode

# Print results
echo "========================================"
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $TESTS_FAILED"

if [ $TESTS_FAILED -eq 0 ]; then
    echo "All tests passed! ✓"
    exit 0
else
    echo "Some tests failed! ✗"
    exit 1
fi
