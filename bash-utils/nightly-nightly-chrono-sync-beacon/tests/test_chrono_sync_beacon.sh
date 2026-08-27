#!/bin/bash

# Test script for nightly-chrono-sync-beacon

# Source the main script to make its functions available for testing
# We'll redefine commands used by it for mocking
SCRIPT_PATH="$(dirname "$0")"/../src/chrono_sync_beacon.sh

# --- Test Utilities ---

# Function to assert a string is present in the log output
assert_contains() {
    local expected_string="$1"
    local log_output="$2"
    if ! echo "$log_output" | grep -qF "$expected_string"; then
        echo "FAIL: Expected log output to contain \"$expected_string\""
        echo "Actual log output:\n$log_output"
        exit 1
    fi
}

# Function to assert a string is NOT present in the log output
assert_not_contains() {
    local unexpected_string="$1"
    local log_output="$2"
    if echo "$log_output" | grep -qF "$unexpected_string"; then
        echo "FAIL: Expected log output NOT to contain \"$unexpected_string\""
        echo "Actual log output:\n$log_output"
        exit 1
    fi
}

# Function to assert the script exited with a specific code
assert_exit_code() {
    local expected_code="$1"
    local actual_code="$2"
    if [ "$expected_code" -ne "$actual_code" ]; then
        echo "FAIL: Expected exit code $expected_code, but got $actual_code"
        exit 1
    fi
}

# --- Mocking Setup ---

# Mock rationale: Simulate sntp command behavior for offset detection and synchronization.
# This allows testing different time drift scenarios and sync outcomes without
# requiring actual network calls or root privileges.
mock_sntp_output=""
mock_sntp_exit_code=0
mock_sntp_sync_attempted=false

sntp() {
    if [[ "$1" == "-d" ]]; then
        echo "$mock_sntp_output"
        return "$mock_sntp_exit_code"
    elif [[ "$1" == "-s" ]]; then
        mock_sntp_sync_attempted=true
        if [[ "$mock_sntp_exit_code" -eq 0 ]]; then
            echo "Simulated sntp -s success"
            return 0
        else
            echo "Simulated sntp -s failure" >&2
            return 1
        fi
    else
        echo "MOCK ERROR: Unexpected sntp call: $*" >&2
        return 1
    fi
}

# Mock rationale: Bypass actual sudo command for testing purposes.
# This allows the script's logic for calling 'sudo sntp -s' to be tested
# without requiring root privileges or actual sudo configuration.
sudo() {
    # Assume sudo is always for sntp in this context for simplicity in testing
    shift # Remove 'sudo'
    sntp "$@" # Call the mocked sntp function
}

# Mock rationale: Control the outcome of 'command -v' for sntp and ensure 'bc' is always found.
# This allows testing scenarios where sntp is missing and prevents test failures if 'bc' is not installed.
_mock_sntp_command_found=true
command() {
    if [[ "$1" == "-v" ]]; then
        if [[ "$2" == "sntp" ]]; then
            if $_mock_sntp_command_found; then
                return 0
            else
                return 1
            fi
        elif [[ "$2" == "bc" ]]; then
            return 0 # bc is always found for tests
        fi
    fi
    # For any other 'command' calls, use the actual builtin command
    builtin command "$@"
}

# --- Test Cases ---

run_test() {
    local test_name="$1"
    local setup_commands="$2"
    local expected_exit_code="$3"
    local expected_log_contains="$4"
    local expected_log_not_contains="$5"
    local sync_expected="$6"

    echo "Running test: $test_name"

    # Reset mocks to default state for each test
    mock_sntp_output=""
    mock_sntp_exit_code=0
    mock_sntp_sync_attempted=false
    _mock_sntp_command_found=true # Reset sntp command found status

    # Setup test specific environment variables and mocks
    eval "$setup_commands"

    # Run the script and capture output
    # Temporarily redirect LOG_FILE to /dev/null for tests to avoid polluting actual filesystem
    # We capture stdout which includes tee'd output
    LOG_FILE="/dev/null" SCRIPT_OUTPUT=$(bash "$SCRIPT_PATH" 2>&1)
    SCRIPT_EXIT_CODE=$?

    assert_exit_code "$expected_exit_code" "$SCRIPT_EXIT_CODE"
    assert_contains "$expected_log_contains" "$SCRIPT_OUTPUT"
    if [ -n "$expected_log_not_contains" ]; then
        assert_not_contains "$expected_log_not_contains" "$SCRIPT_OUTPUT"
    fi

    if [ "$sync_expected" = true ]; then
        if [ "$mock_sntp_sync_attempted" != true ]; then
            echo "FAIL: Expected sntp -s to be called, but it was not."
            exit 1
        fi
    else
        if [ "$mock_sntp_sync_attempted" = true ]; then
            echo "FAIL: Expected sntp -s NOT to be called, but it was."
            exit 1
        fi
    fi

    echo "PASS: $test_name"
    echo "--------------------------------------------------"
}

# Test 1: No significant drift, sync disabled
run_test \
    "No drift, sync disabled" \
    "NTP_SERVER='test.ntp.org' DRIFT_THRESHOLD_SECONDS='5' SYNC_ENABLED='false'; mock_sntp_output='sntp: offset -0.000000 sec'" \
    0 \
    "Temporal stability confirmed." \
    "Significant temporal anomaly detected" \
    false

# Test 2: Small drift, sync disabled
run_test \
    "Small drift, sync disabled" \
    "NTP_SERVER='test.ntp.org' DRIFT_THRESHOLD_SECONDS='5' SYNC_ENABLED='false'; mock_sntp_output='sntp: offset 1.234567 sec'" \
    0 \
    "Temporal stability confirmed." \
    "Significant temporal anomaly detected" \
    false

# Test 3: Large drift, sync disabled
run_test \
    "Large drift, sync disabled" \
    "NTP_SERVER='test.ntp.org' DRIFT_THRESHOLD_SECONDS='1'; mock_sntp_output='sntp: offset -5.432100 sec'" \
    0 \
    "Significant temporal anomaly detected! Offset: -5.432100s (Threshold: 1s)" \
    "System time synchronized" \
    false

# Test 4: Large drift, sync enabled, successful sync
run_test \
    "Large drift, sync enabled, successful sync" \
    "NTP_SERVER='test.ntp.org' DRIFT_THRESHOLD_SECONDS='1' SYNC_ENABLED='true'; mock_sntp_output='sntp: offset 10.000000 sec'; mock_sntp_exit_code=0" \
    0 \
    "System time synchronized." \
    "Failed to synchronize system time." \
    true

# Test 5: Large drift, sync enabled, failed sync
run_test \
    "Large drift, sync enabled, failed sync" \
    "NTP_SERVER='test.ntp.org' DRIFT_THRESHOLD_SECONDS='1' SYNC_ENABLED='true'; mock_sntp_output='sntp: offset -10.000000 sec'; mock_sntp_exit_code=1" \
    1 \
    "Failed to synchronize system time." \
    "System time synchronized." \
    true

# Test 6: sntp command not found
run_test \
    "sntp command not found" \
    "_mock_sntp_command_found=false; unset -f sntp;" \
    1 \
    "sntp command not found." \
    "Initiating temporal scan" \
    false

# Test 7: NTP server query fails
run_test \
    "NTP server query fails" \
    "NTP_SERVER='bad.ntp.org'; mock_sntp_output='sntp: Could not resolve host bad.ntp.org'; mock_sntp_exit_code=1" \
    1 \
    "Failed to query NTP server bad.ntp.org." \
    "Temporal stability confirmed." \
    false

# Test 8: Offset parsing fails
run_test \
    "Offset parsing fails" \
    "NTP_SERVER='test.ntp.org'; mock_sntp_output='sntp: malformed output'; mock_sntp_exit_code=0" \
    1 \
    "Could not parse offset from sntp output" \
    "Temporal stability confirmed." \
    false

# Test 9: Custom threshold and NTP server
run_test \
    "Custom threshold and NTP server" \
    "NTP_SERVER='custom.ntp.org' DRIFT_THRESHOLD_SECONDS='0.1'; mock_sntp_output='sntp: offset 0.500000 sec'" \
    0 \
    "Significant temporal anomaly detected! Offset: 0.500000s (Threshold: 0.1s)" \
    "Temporal stability confirmed." \
    false

echo "All tests passed!"
