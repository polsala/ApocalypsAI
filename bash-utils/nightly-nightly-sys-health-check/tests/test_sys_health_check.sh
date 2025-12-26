#!/bin/bash

# ApocalypsAI - Tests for Nightly System Health Check

# Mock rationale: These tests mock the output of system commands to ensure the script's logic
# correctly interprets different scenarios without relying on actual system state.

# Source the script to be tested
. "$(dirname "$0")"/../src/nightly-sys-health-check.sh

# --- Mock Functions ---

# Mock df command
_mock_df() {
    local path="$1"
    if [[ "$path" == "/" ]]; then
        echo "Filesystem     1K-blocks     Used Available Use% Mounted on"
        echo "/dev/sda1      10000000   900000   8000000  85% /"
    fi
}

# Mock ps command
_mock_ps() {
    echo "USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND"
    for i in $(seq 1 210); do
        echo "user      $i   0.0  0.0 12345  6789 pts/0    S+   10:00   0:00 sleep 1000"
    done
}

# Mock ping command
_mock_ping() {
    local target="$1"
    if [[ "$target" == "8.8.8.8" ]]; then
        # Simulate successful ping
        return 0
    else
        # Simulate failed ping
        return 1
    fi
}

# Mock uptime command
_mock_uptime() {
    echo " 10:00:00 up 1 day,  2:30,  1 user,  load average: 2.50, 2.10, 1.90"
}

# --- Test Cases ---

run_test() {
    local test_name="$1"
    local expected_output="$2"
    local actual_output=$(eval "$3" 2>&1)

    echo "Running test: $test_name"
    if [[ "$actual_output" == *"$expected_output"* ]]; then
        echo "  ✅ PASSED"
    else
        echo "  ❌ FAILED"
        echo "    Expected: $expected_output"
        echo "    Actual:   $actual_output"
        return 1
    fi
    return 0
}

# Test 1: High disk usage

# Override original functions with mocks
_original_df="df"
df() { _mock_df "$@"; }

run_test "High Disk Usage"
    "[WARN] The hoard is getting full! Usage: 85%"
    "check_disk_space"

# Restore original df function
df() { "$_original_df" "$@"; }

# Test 2: High process count

# Override original functions with mocks
_original_ps="ps"
ps() { _mock_ps "$@"; }

run_test "High Process Count"
    "[WARN] A veritable stampede of critters! Count: 210"
    "check_processes"

# Restore original ps function
ps() { "$_original_ps" "$@"; }

# Test 3: Network connectivity lost

# Override original functions with mocks
_original_ping="ping"
ping() { _mock_ping "$@"; }

run_test "Network Lost"
    "[WARN] Signal is weak or lost! Cannot reach 8.8.8.8."
    "check_network"

# Restore original ping function
ping() { "$_original_ping" "$@"; }

# Test 4: High system load

# Override original functions with mocks
_original_uptime="uptime"
uptime() { _mock_uptime "$@"; }

run_test "High System Load"
    "[WARN] The steed is feeling the burden! Load average: 2.50"
    "check_load"

# Restore original uptime function
uptime() { "$_original_uptime" "$@"; }

# Test 5: All systems nominal

# Mock for nominal conditions
_mock_df_nominal() { echo "Filesystem     1K-blocks     Used Available Use% Mounted on"
    echo "/dev/sda1      10000000   500000   9000000  5% /"
}
_mock_ps_nominal() { echo "USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND"
    for i in $(seq 1 50); do
        echo "user      $i   0.0  0.0 12345  6789 pts/0    S+   10:00   0:00 sleep 1000"
    done
}
_mock_ping_nominal() { return 0; }
_mock_uptime_nominal() { echo " 10:00:00 up 1 day,  2:30,  1 user,  load average: 0.50, 0.60, 0.70"
}

df() { _mock_df_nominal "$@"; }
ps() { _mock_ps_nominal "$@"; }
ping() { _mock_ping_nominal "$@"; }
uptime() { _mock_uptime_nominal "$@"; }

run_test "All Systems Nominal"
    "[INFO] Hoard levels are acceptable. Usage: 5%"
    "check_disk_space"

run_test "All Systems Nominal"
    "[INFO] A peaceful gathering of critters. Count: 50"
    "check_processes"

run_test "All Systems Nominal"
    "[INFO] Signal strength is strong! We can reach 8.8.8.8."
    "check_network"

run_test "All Systems Nominal"
    "[INFO] The steed carries its load with grace. Load average: 0.50"
    "check_load"

# Restore original functions
df() { "$_original_df" "$@"; }
ps() { "$_original_ps" "$@"; }
ping() { "$_original_ping" "$@"; }
uptime() { "$_original_uptime" "$@"; }

exit 0
