#!/bin/bash

# This script runs the automated tests for the system health reporter.

# --- Mock Functions ---

# Mock for mpstat command
mock_mpstat() {
    echo "Linux 5.15.0-76-generic (ubuntu)       08/15/23  _x86_64_    (4 CPU)"
    echo ""
    echo "09:00:01     CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle"
    echo "09:00:02     all   15.20    0.00    5.80    0.00    0.00    0.00    0.00    0.00    0.00   79.00"
    echo ""
    echo "Average:     all   15.20    0.00    5.80    0.00    0.00    0.00    0.00    0.00    0.00   79.00"
}

# Mock for free command
mock_free() {
    echo "              total        used        free     shared    buff/cache   available"
    echo "Mem:        16000000     8000000     4000000      500000     4000000     7500000"
    echo "Swap:        2000000           0     2000000"
}

# Mock for df command
mock_df() {
    echo "Filesystem     Size  Used Avail Use% Mounted on"
    echo "/dev/sda1       50G   40G   10G  80% /"
}

# Mock for ip command
mock_ip() {
    echo "1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000"
    echo "    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00"
    echo "    inet 127.0.0.1/8 scope host lo"
    echo "       valid_lft forever preferred_lft forever"
    echo "2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000"
    echo "    link/ether 08:00:27:a1:b2:c3 brd ff:ff:ff:ff:ff:ff"
    echo "    inet 192.168.1.100/24 brd 192.168.1.255 scope global dynamic eth0"
    echo "       valid_lft 86308sec preferred_lft 75508sec"
    echo "3: wlan0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000"
    echo "    link/ether 00:11:22:33:44:55 brd ff:ff:ff:ff:ff:ff"
}

# --- Test Execution ---

TEST_COUNT=0
PASS_COUNT=0

run_test() {
    local test_name="$1"
    shift
    local cmd="$@"

    TEST_COUNT=$((TEST_COUNT + 1))
    echo "Running test: $test_name..."

    # Capture output and exit status
    output=$(eval "$cmd" 2>&1)
    exit_status=$?

    if [ "$exit_status" -eq 0 ]; then
        echo "  ✅ PASS"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "  ❌ FAIL (Exit Code: $exit_status)"
        echo "  Output:"
        echo "  $output" | sed 's/^/    /'
    fi
}

# --- Test Cases ---

# Test 1: Basic functionality with mocked commands
run_test "Basic health report"
(
    # Mocking commands for this test scope
    alias mpstat='mock_mpstat'
    alias free='mock_free'
    alias df='mock_df'
    alias ip='mock_ip'
    # Execute the script and check for expected output patterns
    ./src/nightly-sys-health-reporter.sh | grep -q "CPU Load: 79%"
    [ $? -eq 0 ] && grep -q "Memory Usage: 50%" "$(mktemp)" # Mocking grep for this test
    [ $? -eq 0 ] && grep -q "Root Disk Usage: 80%" "$(mktemp)"
    [ $? -eq 0 ] && grep -q "Active interfaces: eth0" "$(mktemp)"
    [ $? -eq 0 ] && grep -q "System is showing significant strain. Immediate attention required!" "$(mktemp)"
)

# Test 2: Network down scenario
run_test "Network down scenario"
(
    alias mpstat='mock_mpstat'
    alias free='mock_free'
    alias df='mock_df'
    # Mock ip to show no active interfaces
    mock_ip_down() {
        echo "1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000"
        echo "    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00"
        echo "    inet 127.0.0.1/8 scope host lo"
        echo "       valid_lft forever preferred_lft forever"
    }
    alias ip='mock_ip_down'
    ./src/nightly-sys-health-reporter.sh | grep -q "No active network interfaces detected (excluding loopback)."
)

# Test 3: High resource usage scenario
run_test "High resource usage scenario"
(
    # Mocking commands for high usage
    mock_mpstat_high() {
        echo "Linux 5.15.0-76-generic (ubuntu)       08/15/23  _x86_64_    (4 CPU)"
        echo ""
        echo "09:00:01     CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle"
        echo "09:00:02     all   95.20    0.00    4.80    0.00    0.00    0.00    0.00    0.00    0.00    0.00"
        echo ""
        echo "Average:     all   95.20    0.00    4.80    0.00    0.00    0.00    0.00    0.00    0.00    0.00"
    }
    mock_free_high() {
        echo "              total        used        free     shared    buff/cache   available"
        echo "Mem:        16000000    15000000     1000000      500000     1000000      500000"
        echo "Swap:        2000000           0     2000000"
    }
    mock_df_high() {
        echo "Filesystem     Size  Used Avail Use% Mounted on"
        echo "/dev/sda1       50G   45G    5G  90% /"
    }
    alias mpstat='mock_mpstat_high'
    alias free='mock_free_high'
    alias df='mock_df_high'
    alias ip='mock_ip'
    ./src/nightly-sys-health-reporter.sh | grep -q "CPU Load: 95%"
    [ $? -eq 0 ] && grep -q "Memory Usage: 94%" "$(mktemp)"
    [ $? -eq 0 ] && grep -q "Root Disk Usage: 90%" "$(mktemp)"
    [ $? -eq 0 ] && grep -q "System is on the brink! Evacuate immediately!" "$(mktemp)"
)

# --- Summary ---

echo "---------------------"
echo "Test Summary:"
echo "Total Tests: $TEST_COUNT"
echo "Passed: $PASS_COUNT"
echo "Failed: $((TEST_COUNT - PASS_COUNT))"
echo "---------------------"

if [ "$PASS_COUNT" -eq "$TEST_COUNT" ]; then
    exit 0
else
    exit 1
fi
