#!/bin/bash

# Mock rationale: These tests mock the output of system commands like 'top', 'free', and 'df' to simulate different resource usage scenarios without actually affecting the system.

# Source the script to be tested
# Assuming the script is in the parent directory's src folder
SCRIPT_PATH="../src/monitor_resources.sh"

# --- Mocking Functions ---

# Mock 'top' command
mock_top() {
    local cpu_idle="$1"
    echo "top - 10:00:00 up,  1:00,  2 users,  load average: 0.10, 0.15, 0.20"
    echo "Tasks: 100 total,   1 running,  99 sleeping,   0 stopped,   0 zombie"
    echo "%Cpu(s): $cpu_idle us,  0.0 sy,  0.0 ni, 99.9 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st"
    echo "MiB Mem :  10240 total,   2048 free,   6144 used,   2048 buff/cache"
    echo "MiB Swap:   2048 total,   2048 free,      0 used.   8192 avail Mem"
}

# Mock 'free' command
mock_free() {
    local mem_used_percent="$1"
    local total_mem="10240"
    local used_mem=$(echo "$total_mem * $mem_used_percent / 100" | bc)
    local free_mem=$(echo "$total_mem - $used_mem" | bc)
    echo "              total        used        free     shared    buffers     cached"
    echo "Mem:       $total_mem    $used_mem    $free_mem         0         0         0"
    echo "Swap:       2048           0        2048"
}

# Mock 'df -h /' command
mock_df() {
    local disk_used_percent="$1"
    echo "Filesystem      Size  Used Avail Use% Mounted on"
    echo "/dev/sda1        50G   $disk_used_percentG  20G ${disk_used_percent}% /"
}

# Mock 'sendmail' command
mock_sendmail() {
    echo "Mock sendmail called with subject: $1, body: $2"
    return 0 # Simulate successful sending
}

# --- Test Cases ---

run_test() {
    local test_name="$1"
    local cpu_idle="$2"
    local mem_used_percent="$3"
    local disk_used_percent="$4"
    local expected_output_pattern="$5"
    local expected_alert_subject="$6"
    local expected_alert_body_pattern="$7"

    echo "--- Running Test: $test_name ---"

    # Set up mocks
    TOP_MOCK="$(mock_top $cpu_idle)"
    FREE_MOCK="$(mock_free $mem_used_percent)"
    DF_MOCK="$(mock_df $disk_used_percent)"
    ALERT_EMAIL="test@example.com"

    # Override commands with mocks
    TOP_CMD() { echo "$TOP_MOCK"; }
    FREE_CMD() { echo "$FREE_MOCK"; }
    DF_CMD() { echo "$DF_MOCK"; }
    SENDMAIL_CMD() { mock_sendmail "$@"; }

    # Export mock functions and variables for the script to use
    export -f TOP_CMD
    export -f FREE_CMD
    export -f DF_CMD
    export -f SENDMAIL_CMD
    export ALERT_EMAIL

    # Execute the script and capture output
    TEST_OUTPUT=$(bash -c "source $SCRIPT_PATH && monitor_resources.sh")

    # Check for expected output patterns
    if [[ "$TEST_OUTPUT" =~ $expected_output_pattern ]]; then
        echo "PASS: Output matches expected pattern."
    else
        echo "FAIL: Output does not match expected pattern."
        echo "Expected pattern: $expected_output_pattern"
        echo "Actual output:"
        echo "$TEST_OUTPUT"
        return 1
    fi

    # Check for expected alerts (if any)
    if [ -n "$expected_alert_subject" ]; then
        if echo "$TEST_OUTPUT" | grep -q "Alert email sent to $ALERT_EMAIL: $expected_alert_subject"; then
            echo "PASS: Alert subject '$expected_alert_subject' found."
        else
            echo "FAIL: Alert subject '$expected_alert_subject' not found."
            echo "Actual output:"
            echo "$TEST_OUTPUT"
            return 1
        fi
        if [[ "$TEST_OUTPUT" =~ $expected_alert_body_pattern ]]; then
            echo "PASS: Alert body matches expected pattern."
        else
            echo "FAIL: Alert body does not match expected pattern."
            echo "Expected pattern: $expected_alert_body_pattern"
            echo "Actual output:"
            echo "$TEST_OUTPUT"
            return 1
        fi
    else
        if echo "$TEST_OUTPUT" | grep -q "Alert email sent"; then
            echo "FAIL: Unexpected alert email sent."
            echo "Actual output:"
            echo "$TEST_OUTPUT"
            return 1
        else
            echo "PASS: No unexpected alerts sent."
        fi
    fi

    echo "-------------------------"
    return 0
}

# --- Test Execution ---

# Mocking the actual commands to be used by the script
# We need to redefine these within the test script's scope
TOP() { TOP_CMD "$@"; }
export -f TOP
FREE() { FREE_CMD "$@"; }
export -f FREE
DF() { DF_CMD "$@"; }
export -f DF
SENDMAIL() { SENDMAIL_CMD "$@"; }
export -f SENDMAIL

# Test 1: All resources within normal limits
run_test "Normal Usage" 90 20 50 "INFO.*CPU usage: 10.0%" "" ""

# Test 2: High CPU usage
run_test "High CPU" 10 20 50 "WARN.*CPU usage is critically high: 90.0%" "High CPU Usage" "CPU usage is critically high: 90.0%"

# Test 3: High Memory usage
run_test "High Memory" 90 85 50 "WARN.*Memory usage is critically high: 85.0%" "High Memory Usage" "Memory usage is critically high: 85.0%"

# Test 4: High Disk usage
run_test "High Disk" 90 20 95 "WARN.*Disk usage is critically high on /: 95%" "High Disk Usage" "Disk usage is critically high on /: 95%"

# Test 5: All resources high
run_test "All High" 10 85 95 "WARN.*CPU usage is critically high: 90.0%" "High CPU Usage" "CPU usage is critically high: 90.0%"

# Test 6: No email configured, should just log
ALERT_EMAIL=""
export ALERT_EMAIL
run_test "No Email Configured" 10 20 50 "INFO.*CPU usage: 10.0%" "" ""

# Test 7: High CPU with no email configured
run_test "High CPU No Email" 10 20 50 "WARN.*CPU usage is critically high: 90.0%" "" ""

# Clean up exported functions and variables
unset -f TOP_CMD FREE_CMD DF_CMD SENDMAIL_CMD TOP FREE DF SENDMAIL
unset ALERT_EMAIL

echo "All tests completed."
exit 0
