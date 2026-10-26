#!/bin/bash

# Mock rationale: These tests mock the output of system commands like 'top', 'free', and 'df' to ensure the script correctly parses and compares values against thresholds without requiring actual system load.

# --- Mock Functions ---

# Mock 'top' command output
mock_top() {
    echo "top - 10:00:00 up 1 day,  2:30,  2 users,  load average: 0.10, 0.15, 0.20"
    echo "Tasks: 200 total,   1 running, 199 sleeping,   0 stopped,   0 zombie"
    echo "%Cpu(s):  5.0 us,  1.0 sy,  0.0 ni, 94.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st"
    echo "MiB Mem :  16000 total,   2000 free,  10000 used,   4000 buff/cache"
    echo "MiB Swap:   8000 total,   8000 free,     0 used.  12000 avail Mem"
}

# Mock 'free' command output
mock_free() {
    echo "              total        used        free     shared    buffers     cached"
    echo "Mem:           16000        10000        2000         100         500        3500"
    echo "Swap:           8000           0          8000"
}

# Mock 'df -h' command output for root partition
mock_df_root() {
    echo "Filesystem      Size  Used Avail Use% Mounted on"
    echo "/dev/sda1        50G   40G   10G  80% /"
}

# Mock 'df -h' command output for another partition
mock_df_other() {
    echo "Filesystem      Size  Used Avail Use% Mounted on"
    echo "/dev/sdb1       100G   95G    5G  95% /data"
}

# --- Test Setup ---

# Override actual commands with mocks
_original_top=top
_original_free=free
_original_df=df

stub_command() {
    local cmd="$1"
    local mock_func="$2"
    eval "$cmd() { $mock_func; }"
}

# --- Test Cases ---

run_test() {
    local test_name="$1"
    local expected_output="$2"
    local actual_output=$(eval "$3")

    echo "Running test: $test_name"
    if [[ "$actual_output" == *"$expected_output"* ]]; then
        echo "  PASS"
    else
        echo "  FAIL"
        echo "    Expected: $expected_output"
        echo "    Got:      $actual_output"
        return 1
    fi
    return 0
}

# --- Main Test Execution ---

# Test 1: Default thresholds, no alerts
stub_command top mock_top
stub_command free mock_free
stub_command df mock_df_root

# Temporarily set environment variables for this test to ensure they are used
export CPU_THRESHOLD=95
export RAM_THRESHOLD=90
export DISK_THRESHOLD=90
export DISK_PARTITION="/"

# Capture output of the script
script_output=$(./src/monitor.sh)

# Check for expected output (no alerts)
if run_test "Default thresholds, no alerts" "CPU Usage: 95.0%\nRAM Usage: 62.50% (Total: 16000MB, Used: 10000MB)\nDisk Usage (/): 80%" "echo \"$script_output\""; then
    echo "Test 1 Passed."
else
    echo "Test 1 Failed."
    exit 1
fi

# Test 2: CPU alert
stub_command top mock_top
stub_command free mock_free
stub_command df mock_df_root

export CPU_THRESHOLD=70
export RAM_THRESHOLD=90
export DISK_THRESHOLD=90
export DISK_PARTITION="/"

script_output=$(./src/monitor.sh)

if run_test "CPU alert" "ALERT: CPU usage (95.0%) exceeds threshold (70%)" "echo \"$script_output\""; then
    echo "Test 2 Passed."
else
    echo "Test 2 Failed."
    exit 1
fi

# Test 3: RAM alert
stub_command top mock_top
stub_command free mock_free
stub_command df mock_df_root

export CPU_THRESHOLD=95
export RAM_THRESHOLD=60
export DISK_THRESHOLD=90
export DISK_PARTITION="/"

script_output=$(./src/monitor.sh)

if run_test "RAM alert" "ALERT: RAM usage (62.50%) exceeds threshold (60%)" "echo \"$script_output\""; then
    echo "Test 3 Passed."
else
    echo "Test 3 Failed."
    exit 1
fi

# Test 4: Disk alert
stub_command top mock_top
stub_command free mock_free
stub_command df mock_df_other

export CPU_THRESHOLD=95
export RAM_THRESHOLD=90
export DISK_THRESHOLD=90
export DISK_PARTITION="/data"

script_output=$(./src/monitor.sh)

if run_test "Disk alert" "ALERT: Disk usage (95%) on /data exceeds threshold (90%)" "echo \"$script_output\""; then
    echo "Test 4 Passed."
else
    echo "Test 4 Failed."
    exit 1
fi

# Test 5: All thresholds met, no alerts
stub_command top mock_top
stub_command free mock_free
stub_command df mock_df_root

export CPU_THRESHOLD=96
export RAM_THRESHOLD=63
export DISK_THRESHOLD=81
export DISK_PARTITION="/"

script_output=$(./src/monitor.sh)

if run_test "All thresholds met, no alerts" "CPU Usage: 95.0%\nRAM Usage: 62.50% (Total: 16000MB, Used: 10000MB)\nDisk Usage (/): 80%" "echo \"$script_output\""; then
    echo "Test 5 Passed."
else
    echo "Test 5 Failed."
    exit 1
fi

# --- Cleanup ---

# Restore original commands
_original_top
_original_free
_original_df

# Unset exported variables
unset CPU_THRESHOLD
unset RAM_THRESHOLD
unset DISK_THRESHOLD
unset DISK_PARTITION

echo "All tests completed."
exit 0
