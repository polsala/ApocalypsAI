#!/bin/bash

# tests/test_sys_health_check.sh
# Automated tests for the nightly-sys-health-check.sh script.

# --- Mock Functions ---

# Mock for df command
mock_df() {
    echo "Filesystem Size Used Avail Use% Mounted on"
    echo "/dev/sda1 100G 50G 50G 50% /"
}

# Mock for free command
mock_free() {
    echo "              total        used        free     shared    buff/cache   available"
    echo "Mem:           7.7Gi       3.0Gi       1.5Gi       200Mi       3.2Gi       4.3Gi"
    echo "Swap:          2.0Gi         0B        2.0Gi"
}

# Mock for ps command
mock_ps() {
    echo "USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND"
    echo "root 1 0.5 0.1 10000 5000 ? Ss 00:00 0:05 /sbin/init"
    echo "user 123 0.2 0.5 20000 10000 pts/0 S+ 10:00 0:10 bash"
    echo "root 456 0.1 0.2 15000 7000 ? Ss 09:00 0:02 /usr/lib/systemd/systemd-journald"
    echo "user 789 0.0 0.3 18000 9000 pts/1 S+ 10:05 0:01 vim"
    echo "root 101 0.0 0.1 12000 6000 ? Ss 08:00 0:01 /usr/lib/systemd/systemd-udevd"
    echo "user 112 0.0 0.2 16000 8000 pts/2 S+ 10:10 0:00 nano"
}

# --- Test Runner ---

run_test() {
    local test_name="$1"
    local expected_output="$2"
    local actual_output="$3"

    echo "Running test: $test_name"
    if [[ "$actual_output" == *"$expected_output"* ]]; then
        echo "  ✅ PASSED"
    else
        echo "  ❌ FAILED"
        echo "    Expected (partial): $expected_output"
        echo "    Actual (partial): $actual_output"
        return 1
    fi
    return 0
}

# --- Test Cases ---

# Test Disk Usage
TEST_DISK_USAGE_EXPECTED="Use%: 50%"
TEST_DISK_USAGE_ACTUAL=$(mock_df | ./src/nightly-sys-health-check.sh | grep "Disk Usage")
run_test "Disk Usage Check" "$TEST_DISK_USAGE_EXPECTED" "$TEST_DISK_USAGE_ACTUAL"
if [ $? -ne 0 ]; then exit 1; fi

# Test Memory Usage
TEST_MEMORY_USAGE_EXPECTED="Use%: 4.3Gi"
TEST_MEMORY_USAGE_ACTUAL=$(mock_free | ./src/nightly-sys-health-check.sh | grep "Memory Usage")
run_test "Memory Usage Check" "$TEST_MEMORY_USAGE_EXPECTED" "$TEST_MEMORY_USAGE_ACTUAL"
if [ $? -ne 0 ]; then exit 1; fi

# Test Running Processes (check for presence of specific command)
TEST_PROCESS_CHECK_EXPECTED="bash"
TEST_PROCESS_CHECK_ACTUAL=$(mock_ps | ./src/nightly-sys-health-check.sh | grep "Running Processes")
run_test "Running Processes Check (bash present)" "$TEST_PROCESS_CHECK_EXPECTED" "$TEST_PROCESS_CHECK_ACTUAL"
if [ $? -ne 0 ]; then exit 1; fi

# Test Running Processes (check for correct number of lines for processes)
# We expect 1 header line + TOP_PROCESS_COUNT lines for processes
TEST_PROCESS_COUNT_EXPECTED=$(expr 1 + 5)
TEST_PROCESS_COUNT_ACTUAL=$(mock_ps | ./src/nightly-sys-health-check.sh | grep "Running Processes" | wc -l)
# Adjusting for the header line in the actual output of the script
TEST_PROCESS_COUNT_ACTUAL=$(echo "$TEST_PROCESS_COUNT_ACTUAL" | awk '{print $1 - 1}') # Subtract header line

run_test "Running Processes Count Check" "5" "$TEST_PROCESS_COUNT_ACTUAL"
if [ $? -ne 0 ]; then exit 1; fi


echo "\nAll tests passed! The system health check is functioning as expected."
exit 0
