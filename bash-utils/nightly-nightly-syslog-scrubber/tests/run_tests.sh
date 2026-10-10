#!/bin/bash

set -e # Exit immediately if a command exits with a non-zero status.

# Define test cases
TEST_CASES=(
    "Test 1: Basic IP and keyword scrubbing"
    "Test 2: IPv6 scrubbing and user redaction"
    "Test 3: Timestamp reformatting"
    "Test 4: Mixed sensitive data and keywords"
    "Test 5: No sensitive data, just keywords"
    "Test 6: Empty input"
    "Test 7: Custom keywords and masks"
    "Test 8: Compressed IPv6"
)

# Define expected outputs for each test case
EXPECTED_OUTPUTS=(
    "INFO: User \"[USER_REDACTED]\" logged in from \"[IP_REDACTED]\" on 2023-10-27 10:30:00. An \x1b[1;31mERROR\x1b[0m occurred."
    "WARN: Connection from \"[IP_REDACTED]\" to \"[IP_REDACTED]\" failed. User \"[USER_REDACTED]\" reported issue."
    "2023-10-27 10:30:00 INFO: System status OK. No \x1b[1;33mWARNING\x1b[0m detected."
    "DEBUG: Request from \"[IP_REDACTED]\" by \"[USER_REDACTED]\" for resource X. \x1b[1;31mCRITICAL\x1b[0m failure in service Y. \x1b[1;33mALERT\x1b[0m raised."
    "INFO: All systems nominal. No \x1b[1;31mERROR\x1b[0m or \x1b[1;33mWARNING\x1b[0m found."
    ""
    "CUSTOM_INFO: User \"[MY_USER]\" from \"[MY_IP]\" triggered \x1b[1;31mURGENT\x1b[0m event."
    "WARN: Connection from \"[IP_REDACTED]\" to \"[IP_REDACTED]\" failed. User \"[USER_REDACTED]\" reported issue."
)

# Define input logs for each test case
INPUT_LOGS=(
    "INFO: User \"alice\" logged in from \"192.168.1.100\" on 2023-10-27 10:30:00. An ERROR occurred."
    "WARN: Connection from \"10.0.0.5\" to \"172.16.0.1\" failed. User \"bob\" reported issue."
    "2023/10/27 10:30:00 INFO: System status OK. No WARNING detected."
    "DEBUG: Request from 192.168.1.100 by user alice for resource X. CRITICAL failure in service Y. ALERT raised."
    "INFO: All systems nominal. No errors or warnings found."
    ""
    "CUSTOM_INFO: User \"admin\" from \"192.168.1.1\" triggered URGENT event."
    "WARN: Connection from 2001:0db8:85a3:0000:0000:8a2e:0370:7334 to 2001:db8::1 failed. User \"guest\" reported issue."
)

# Source the script to be tested
SCRIPT_PATH="./src/nightly-syslog-scrubber.sh"

# --- Test Runner Function ---
run_test() {
    local test_name="$1"
    local input_log="$2"
    local expected_output="$3"
    local test_index=$(( $4 - 1 ))

    echo "Running $test_name..."

    # Mock: Simulate running the script with specific inputs and environment variables
    # The actual script will be executed, and its output captured.
    local actual_output
    if [[ "$test_name" == "Test 3: Timestamp reformatting" ]]; then
        SYSLOG_SCRUBBER_TIMESTAMP_FORMAT="+%Y-%m-%d %H:%M:%S"
        actual_output=$(echo -e "$input_log" | bash "$SCRIPT_PATH")
        unset SYSLOG_SCRUBBER_TIMESTAMP_FORMAT # Clean up env var
    elif [[ "$test_name" == "Test 7: Custom keywords and masks" ]]; then
        SYSLOG_SCRUBBER_KEYWORDS="URGENT"
        SYSLOG_SCRUBBER_IP_MASK="[MY_IP]"
        SYSLOG_SCRUBBER_USER_MASK="[MY_USER]"
        actual_output=$(echo -e "$input_log" | bash "$SCRIPT_PATH")
        unset SYSLOG_SCRUBBER_KEYWORDS SYSLOG_SCRUBBER_IP_MASK SYSLOG_SCRUBBER_USER_MASK # Clean up env vars
    else
        actual_output=$(echo -e "$input_log" | bash "$SCRIPT_PATH")
    fi

    # Normalize outputs for comparison (remove trailing newlines)
    actual_output=$(echo -e "$actual_output")
    expected_output=$(echo -e "$expected_output")

    if [[ "$actual_output" == "$expected_output" ]]; then
        echo "  ✅ PASSED"
    else
        echo "  ❌ FAILED"
        echo "    Expected: '$expected_output'"
        echo "    Actual:   '$actual_output'"
        return 1 # Indicate failure
    fi
    return 0 # Indicate success
}

# --- Execute Tests ---

all_passed=true

# Test 1: Basic IP and keyword scrubbing
if ! run_test "${TEST_CASES[0]}" "${INPUT_LOGS[0]}" "${EXPECTED_OUTPUTS[0]}" 1; then all_passed=false; fi

# Test 2: IPv6 scrubbing and user redaction
if ! run_test "${TEST_CASES[1]}" "${INPUT_LOGS[1]}" "${EXPECTED_OUTPUTS[1]}" 2; then all_passed=false; fi

# Test 3: Timestamp reformatting
if ! run_test "${TEST_CASES[2]}" "${INPUT_LOGS[2]}" "${EXPECTED_OUTPUTS[2]}" 3; then all_passed=false; fi

# Test 4: Mixed sensitive data and keywords
if ! run_test "${TEST_CASES[3]}" "${INPUT_LOGS[3]}" "${EXPECTED_OUTPUTS[3]}" 4; then all_passed=false; fi

# Test 5: No sensitive data, just keywords
if ! run_test "${TEST_CASES[4]}" "${INPUT_LOGS[4]}" "${EXPECTED_OUTPUTS[4]}" 5; then all_passed=false; fi

# Test 6: Empty input
if ! run_test "${TEST_CASES[5]}" "${INPUT_LOGS[5]}" "${EXPECTED_OUTPUTS[5]}" 6; then all_passed=false; fi

# Test 7: Custom keywords and masks
if ! run_test "${TEST_CASES[6]}" "${INPUT_LOGS[6]}" "${EXPECTED_OUTPUTS[6]}" 7; then all_passed=false; fi

# Test 8: Compressed IPv6
if ! run_test "${TEST_CASES[7]}" "${INPUT_LOGS[7]}" "${EXPECTED_OUTPUTS[7]}" 8; then all_passed=false; fi

# --- Summary ---

if $all_passed; then
    echo "\nAll tests passed! 🎉"
    exit 0
else
    echo "\nSome tests failed. 😞"
    exit 1
fi
