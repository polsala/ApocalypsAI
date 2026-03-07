#!/bin/bash

# Source the main script to make its functions available
# This will define generate_report, check_journalctl, check_dmesg
. src/main.sh

# Mock functions for journalctl and dmesg
# These will replace the actual check_journalctl and check_dmesg functions
# defined in src/main.sh after sourcing.
mock_journalctl_output() {
    # Mock rationale: Simulate journalctl output for testing purposes.
    # This avoids actual system calls and ensures deterministic test results.
    if [ "$1" == "no_anomalies" ]; then
        echo ""
    elif [ "$1" == "with_anomalies" ]; then
        echo "Jul 26 00:00:01 host systemd-timesyncd[123]: Timed out waiting for reply from 1.2.3.4:NTP"
        echo "Jul 26 00:00:02 host systemd-timesyncd[123]: NTP client failed to set time: Connection refused"
    else
        # Default case for systems where journalctl might not be present or for specific test scenarios
        echo "journalctl not found. Skipping journalctl check."
    fi
}

mock_dmesg_output() {
    # Mock rationale: Simulate dmesg output for testing purposes.
    # This avoids actual system calls and ensures deterministic test results.
    if [ "$1" == "no_anomalies" ]; then
        echo "Kernel command line: BOOT_IMAGE=/boot/vmlinuz-5.15.0-84-generic root=UUID=... ro quiet splash"
        echo "Clock: TSC detected, running at 2400.000 MHz"
    elif [ "$1" == "with_anomalies" ]; then
        echo "Clock: TSC detected, running at 2400.000 MHz"
        echo "NTP: clock_was_set_by_ntp: 1"
        echo "kernel: clocksource: timekeeping watchdog: Marking clocksource 'tsc' as unstable because it ran backwards."
    else
        # Default case for systems where dmesg might not be present or for specific test scenarios
        echo "dmesg not found. Skipping dmesg check."
    fi
}

# Override the functions from src/main.sh with our mocks
check_journalctl() {
    mock_journalctl_output "$MOCK_SCENARIO_JOURNALCTL"
}

check_dmesg() {
    mock_dmesg_output "$MOCK_SCENARIO_DMESG"
}

# Test cases
test_no_anomalies() {
    echo "Running test_no_anomalies..."
    MOCK_SCENARIO_JOURNALCTL="no_anomalies"
    MOCK_SCENARIO_DMESG="no_anomalies"
    output=$(generate_report)

    if echo "$output" | grep -q "All clear! The temporal fabric appears stable."; then
        echo "✅ Test 'no anomalies' passed."
    else
        echo "❌ Test 'no anomalies' failed. Output:"
        echo "$output"
        exit 1
    fi
}

test_with_journalctl_anomalies() {
    echo "Running test_with_journalctl_anomalies..."
    MOCK_SCENARIO_JOURNALCTL="with_anomalies"
    MOCK_SCENARIO_DMESG="no_anomalies" # Ensure dmesg is clean for this specific test
    output=$(generate_report)

    if echo "$output" | grep -q "Journalctl Whispers" && \
       echo "$output" | grep -q "Timed out waiting for reply from" && \
       echo "$output" | grep -q "Warning: Potential temporal distortions detected!"; then
        echo "✅ Test 'with journalctl anomalies' passed."
    else
        echo "❌ Test 'with journalctl anomalies' failed. Output:"
        echo "$output"
        exit 1
    fi
}

test_with_dmesg_anomalies() {
    echo "Running test_with_dmesg_anomalies..."
    MOCK_SCENARIO_JOURNALCTL="no_anomalies" # Ensure journalctl is clean for this specific test
    MOCK_SCENARIO_DMESG="with_anomalies"
    output=$(generate_report)

    if echo "$output" | grep -q "Dmesg Echoes" && \
       echo "$output" | grep -q "clocksource: timekeeping watchdog: Marking clocksource 'tsc' as unstable" && \
       echo "$output" | grep -q "Warning: Potential temporal distortions detected!"; then
        echo "✅ Test 'with dmesg anomalies' passed."
    else
        echo "❌ Test 'with dmesg anomalies' failed. Output:"
        echo "$output"
        exit 1
    fi
}

test_with_both_anomalies() {
    echo "Running test_with_both_anomalies..."
    MOCK_SCENARIO_JOURNALCTL="with_anomalies"
    MOCK_SCENARIO_DMESG="with_anomalies"
    output=$(generate_report)

    if echo "$output" | grep -q "Journalctl Whispers" && \
       echo "$output" | grep -q "Dmesg Echoes" && \
       echo "$output" | grep -q "Warning: Potential temporal distortions detected!"; then
        echo "✅ Test 'with both anomalies' passed."
    else
        echo "❌ Test 'with both anomalies' failed. Output:"
        echo "$output"
        exit 1
    fi
}

# Run all tests
test_no_anomalies
test_with_journalctl_anomalies
test_with_dmesg_anomalies
test_with_both_anomalies

echo "All tests completed."
