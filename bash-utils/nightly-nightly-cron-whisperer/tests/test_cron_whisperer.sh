#!/bin/bash

# Source the script to be tested
# Mock rationale: We source the script to make its functions available for testing.
# We will override the 'crontab' command for deterministic testing.
SCRIPT_TO_TEST="../src/cron_whisperer.sh"

# Helper function for assertions
assert_contains() {
    local output="$1"
    local expected="$2"
    if ! echo "$output" | grep -q "$expected"; then
        echo "FAIL: Expected output to contain \"$expected\""
        echo "Actual output:"
        echo "$output"
        exit 1
    fi
}

assert_not_contains() {
    local output="$1"
    local unexpected="$2"
    if echo "$output" | grep -q "$unexpected"; then
        echo "FAIL: Expected output NOT to contain \"$unexpected\""
        echo "Actual output:"
        echo "$output"
        exit 1
    fi
}

# --- Test Cases ---

# Test 1: No cron jobs
test_no_cron_jobs() {
    echo "Running Test 1: No cron jobs"
    # Mock rationale: Override 'crontab' to return an empty string.
    crontab() { echo ""; }
    export -f crontab # Export function for subshells

    local output=$(bash "$SCRIPT_TO_TEST")
    assert_contains "$output" "No cron jobs detected. The temporal fabric is calm."
    assert_not_contains "$output" "Schedule:"
    echo "Test 1 Passed."
}

# Test 2: Basic cron jobs
test_basic_cron_jobs() {
    echo "Running Test 2: Basic cron jobs"
    # Mock rationale: Override 'crontab' to return a predefined set of cron jobs.
    crontab() {
        echo "# My important cron jobs"
        echo "0 0 * * * /usr/local/bin/backup_data.sh"
        echo "30 2 * * 1 /usr/bin/cleanup_logs.sh"
        echo "*/10 * * * * /usr/bin/monitor_service.sh"
        echo "0 0 1 * * /usr/bin/apt update && apt upgrade -y"
    }
    export -f crontab

    local output=$(bash "$SCRIPT_TO_TEST")
    assert_contains "$output" "Guardian of the Archives"
    assert_contains "$output" "Wasteland Scavenger"
    assert_contains "$output" "Silent Observer"
    assert_contains "$output" "Temporal Harmonizer"
    assert_contains "$output" "Total active cron jobs analyzed: 4"
    assert_not_contains "$output" "Hyper-Vigilant Sentinel" # Not a * * * * * job
    echo "Test 2 Passed."
}

# Test 3: Hyper-Vigilant Sentinel (frequent job)
test_frequent_cron_job() {
    echo "Running Test 3: Frequent cron job"
    # Mock rationale: Override 'crontab' to return a very frequent cron job.
    crontab() {
        echo "* * * * * /usr/bin/check_heartbeat.sh"
    }
    export -f crontab

    local output=$(bash "$SCRIPT_TO_TEST")
    assert_contains "$output" "Hyper-Vigilant Sentinel (Mysterious Routine)"
    assert_contains "$output" "Total active cron jobs analyzed: 1"
    echo "Test 3 Passed."
}

# Test 4: Mixed cron jobs with comments and empty lines
test_mixed_cron_jobs() {
    echo "Running Test 4: Mixed cron jobs"
    # Mock rationale: Override 'crontab' to return a mix of valid, commented, and empty lines.
    crontab() {
        echo "# This is a comment"
        echo ""
        echo "15 3 * * * /opt/app/daily_report.sh"
        echo "# Another comment"
        echo "0 0 * * * /usr/local/bin/backup_critical.sh"
    }
    export -f crontab

    local output=$(bash "$SCRIPT_TO_TEST")
    assert_contains "$output" "Mysterious Routine" # for daily_report.sh
    assert_contains "$output" "Guardian of the Archives" # for backup_critical.sh
    assert_contains "$output" "Total active cron jobs analyzed: 2"
    echo "Test 4 Passed."
}

# Test 5: Cron job with 'reboot'
test_reboot_cron_job() {
    echo "Running Test 5: Reboot cron job"
    crontab() {
        echo "0 5 * * * /sbin/reboot"
    }
    export -f crontab

    local output=$(bash "$SCRIPT_TO_TEST")
    assert_contains "$output" "System's Slumber"
    assert_contains "$output" "Total active cron jobs analyzed: 1"
    echo "Test 5 Passed."
}

# Run all tests
test_no_cron_jobs
test_basic_cron_jobs
test_frequent_cron_job
test_mixed_cron_jobs
test_reboot_cron_job

echo "All tests passed for Nightly Cron Whisperer!"
