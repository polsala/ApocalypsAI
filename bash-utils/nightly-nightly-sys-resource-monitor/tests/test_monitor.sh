#!/bin/bash

# Source the script to be tested
# Mock rationale: Sourcing the script allows us to override functions for testing.
. src/monitor.sh

# --- Test Functions ---

# Mock get_cpu_usage for testing high CPU alert
test_high_cpu() {
    echo "Testing High CPU Alert..."
    # Mock rationale: Override get_cpu_usage to return a value above the threshold.
    get_cpu_usage() { echo "90"; }
    local output=$(./src/monitor.sh)
    if echo "$output" | grep -q "ALERT: High CPU Usage detected! Current: 90%, Threshold: 80%"; then
        echo "  PASS: High CPU alert triggered correctly."
    else
        echo "  FAIL: High CPU alert not triggered."
        echo "    Output: $output"
    fi
}

# Mock get_cpu_usage for testing normal CPU
test_normal_cpu() {
    echo "Testing Normal CPU Usage..."
    # Mock rationale: Override get_cpu_usage to return a value below the threshold.
    get_cpu_usage() { echo "40"; }
    local output=$(./src/monitor.sh)
    if ! echo "$output" | grep -q "ALERT: High CPU Usage detected!"; then
        echo "  PASS: No CPU alert triggered for normal usage."
    else
        echo "  FAIL: Unexpected CPU alert triggered."
        echo "    Output: $output"
    fi
}

# Mock get_ram_usage for testing high RAM alert
test_high_ram() {
    echo "Testing High RAM Alert..."
    # Mock rationale: Override get_ram_usage to return a value above the threshold.
    get_ram_usage() { echo "95"; }
    local output=$(./src/monitor.sh)
    if echo "$output" | grep -q "ALERT: High RAM Usage detected! Current: 95%, Threshold: 85%"; then
        echo "  PASS: High RAM alert triggered correctly."
    else
        echo "  FAIL: High RAM alert not triggered."
        echo "    Output: $output"
    fi
}

# Mock get_ram_usage for testing normal RAM
test_normal_ram() {
    echo "Testing Normal RAM Usage..."
    # Mock rationale: Override get_ram_usage to return a value below the threshold.
    get_ram_usage() { echo "50"; }
    local output=$(./src/monitor.sh)
    if ! echo "$output" | grep -q "ALERT: High RAM Usage detected!"; then
        echo "  PASS: No RAM alert triggered for normal usage."
    else
        echo "  FAIL: Unexpected RAM alert triggered."
        echo "    Output: $output"
    fi
}

# Mock get_disk_usage for testing high Disk alert
test_high_disk() {
    echo "Testing High Disk Alert..."
    # Mock rationale: Override get_disk_usage to return a value above the threshold.
    get_disk_usage() { echo "98"; }
    local output=$(./src/monitor.sh)
    if echo "$output" | grep -q "ALERT: High Disk Usage detected! Current: 98%, Threshold: 90% on /"; then
        echo "  PASS: High Disk alert triggered correctly."
    else
        echo "  FAIL: High Disk alert not triggered."
        echo "    Output: $output"
    fi
}

# Mock get_disk_usage for testing normal Disk
test_normal_disk() {
    echo "Testing Normal Disk Usage..."
    # Mock rationale: Override get_disk_usage to return a value below the threshold.
    get_disk_usage() { echo "60"; }
    local output=$(./src/monitor.sh)
    if ! echo "$output" | grep -q "ALERT: High Disk Usage detected!"; then
        echo "  PASS: No Disk alert triggered for normal usage."
    else
        echo "  FAIL: Unexpected Disk alert triggered."
        echo "    Output: $output"
    fi
}

# Mock get_disk_usage for testing multiple disks (only one monitored here for simplicity)
test_multiple_disks_monitored() {
    echo "Testing Multiple Disks Monitored (only '/' is configured)...".
    # Mock rationale: Ensure only configured disks are checked.
    # The script's MONITORED_DISKS variable is set to "/" in src/monitor.sh.
    # We'll mock get_disk_usage to return different values to ensure it's called for '/'.
    get_disk_usage() {
        local mount_point="$1"
        if [ "$mount_point" == "/" ]; then
            echo "88"
        else
            echo "99"
        fi
    }
    local output=$(./src/monitor.sh)
    if ! echo "$output" | grep -q "ALERT: High Disk Usage detected! Current: 99%"; then
        echo "  PASS: Only configured disk '/' was checked for alerts."
    else
        echo "  FAIL: Unexpected alert for unmonitored disk."
        echo "    Output: $output"
    fi
}

# --- Test Runner ---

run_tests() {
    test_high_cpu
    test_normal_cpu
    test_high_ram
    test_normal_ram
    test_high_disk
    test_normal_disk
    test_multiple_disks_monitored
}

run_tests
