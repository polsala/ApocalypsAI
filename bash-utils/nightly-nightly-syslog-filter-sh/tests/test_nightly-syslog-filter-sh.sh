#!/bin/bash

# Mock rationale: We are mocking the tail command and its output to simulate log file content.
# This allows for deterministic testing without needing actual log files or running processes.

# Source the script to be tested
# Assuming the script is in the same directory as the tests folder
SCRIPT_PATH="../src/nightly-syslog-filter-sh"

# --- Mocking Functions ---

# Mock tail command
# This function will echo predefined log lines to stdout, simulating tail -f output.
mock_tail() {
    local log_content="$1"
    echo -e "$log_content"
}

# --- Test Cases ---

run_test() {
    local test_name="$1"
    local mock_log_content="$2"
    local script_args="$3"
    local expected_output="$4"
    local actual_output

    echo "Running test: $test_name..."

    # Execute the script with mocked tail output
    # We pipe the mock_tail output to the script's while loop
    actual_output=$(echo -e "$mock_log_content" | bash "$SCRIPT_PATH" $script_args)

    # Compare actual output with expected output
    if [[ "$actual_output" == "$expected_output" ]]; then
        echo "  PASSED"
    else
        echo "  FAILED"
        echo "    Expected:"
        echo "$expected_output"
        echo "    Actual:"
        echo "$actual_output"
        return 1 # Indicate failure
    fi
    return 0 # Indicate success
}

# --- Test Setup ---

# Create a temporary log file for testing (though we'll mock tail)
# This is more for conceptual clarity and if the script were to directly read the file.
# For this mock, we're piping into the script.

# Define mock log content
MOCK_LOG_CONTENT_BASIC="
Oct 26 10:00:00 server kernel: [ 123.456] Some informational message.
Oct 26 10:01:00 server systemd[1]: Starting Some Service...
Oct 26 10:02:00 server kernel: [ 125.789] An error occurred: disk full.
Oct 26 10:03:00 server authpriv: debug: User logged in.
Oct 26 10:04:00 server kernel: [ 128.111] Another informational message.
Oct 26 10:05:00 server systemd[1]: Some Service stopped.
Oct 26 10:06:00 server kernel: [ 130.222] Critical error: network down.
Oct 26 10:07:00 server authpriv: debug: User logged out.
"

# ANSI color codes for expected output
RED="\033[0;31m"
BLUE="\033[0;34m"
RESET="\033[0m"

# --- Running Tests ---

TEST_COUNT=0
PASSED_COUNT=0

# Test 1: Default behavior (include error, exclude debug)
TEST_COUNT=$((TEST_COUNT + 1))
DEFAULT_EXPECTED_OUTPUT="
Oct 26 10:00:00 server kernel: [ 123.456] Some informational message.
Oct 26 10:01:00 server systemd[1]: Starting Some Service...
${RED}Oct 26 10:02:00 server kernel: [ 125.789] An error occurred: disk full.${RESET}
Oct 26 10:03:00 server authpriv: debug: User logged in.
Oct 26 10:04:00 server kernel: [ 128.111] Another informational message.
Oct 26 10:05:00 server systemd[1]: Some Service stopped.
${RED}Oct 26 10:06:00 server kernel: [ 130.222] Critical error: network down.${RESET}
Oct 26 10:07:00 server authpriv: debug: User logged in.
"
if run_test "Default behavior" "$MOCK_LOG_CONTENT_BASIC" "" "$DEFAULT_EXPECTED_OUTPUT"; then
    PASSED_COUNT=$((PASSED_COUNT + 1))
fi

# Test 2: Custom include and exclude keywords with colors
TEST_COUNT=$((TEST_COUNT + 1))
CUSTOM_LOG_CONTENT="
Oct 26 11:00:00 server kernel: [ 123.456] System is running fine.
Oct 26 11:01:00 server systemd[1]: Starting Another Service...
Oct 26 11:02:00 server kernel: [ 125.789] Warning: low disk space.
Oct 26 11:03:00 server authpriv: verbose: User activity detected.
Oct 26 11:04:00 server kernel: [ 128.111] Another informational message.
Oct 26 11:05:00 server systemd[1]: Another Service stopped.
Oct 26 11:06:00 server kernel: [ 130.222] Critical alert: power failure.
Oct 26 11:07:00 server authpriv: verbose: User activity confirmed.
"
CUSTOM_EXPECTED_OUTPUT="
Oct 26 11:00:00 server kernel: [ 123.456] System is running fine.
Oct 26 11:01:00 server systemd[1]: Starting Another Service...
Oct 26 11:02:00 server kernel: [ 125.789] Warning: low disk space.
Oct 26 11:03:00 server authpriv: verbose: User activity detected.
Oct 26 11:04:00 server kernel: [ 128.111] Another informational message.
Oct 26 11:05:00 server systemd[1]: Another Service stopped.
${RED}Oct 26 11:06:00 server kernel: [ 130.222] Critical alert: power failure.${RESET}
Oct 26 11:07:00 server authpriv: verbose: User activity confirmed.
"
if run_test "Custom keywords and colors" "$CUSTOM_LOG_CONTENT" "--include 'alert' --color-include 'red' --exclude 'verbose' --color-exclude 'blue'" "$CUSTOM_EXPECTED_OUTPUT"; then
    PASSED_COUNT=$((PASSED_COUNT + 1))
fi

# Test 3: Only include, no exclude
TEST_COUNT=$((TEST_COUNT + 1))
ONLY_INCLUDE_EXPECTED_OUTPUT="
Oct 26 10:00:00 server kernel: [ 123.456] Some informational message.
${RED}Oct 26 10:02:00 server kernel: [ 125.789] An error occurred: disk full.${RESET}
Oct 26 10:04:00 server kernel: [ 128.111] Another informational message.
${RED}Oct 26 10:06:00 server kernel: [ 130.222] Critical error: network down.${RESET}
"
if run_test "Only include" "$MOCK_LOG_CONTENT_BASIC" "--include 'error' --color-include 'red' --exclude ''" "$ONLY_INCLUDE_EXPECTED_OUTPUT"; then
    PASSED_COUNT=$((PASSED_COUNT + 1))
fi

# Test 4: Only exclude, no include
TEST_COUNT=$((TEST_COUNT + 1))
ONLY_EXCLUDE_EXPECTED_OUTPUT="
Oct 26 10:00:00 server kernel: [ 123.456] Some informational message.
Oct 26 10:01:00 server systemd[1]: Starting Some Service...
Oct 26 10:02:00 server kernel: [ 125.789] An error occurred: disk full.
Oct 26 10:04:00 server kernel: [ 128.111] Another informational message.
Oct 26 10:05:00 server systemd[1]: Some Service stopped.
Oct 26 10:06:00 server kernel: [ 130.222] Critical error: network down.
"
if run_test "Only exclude" "$MOCK_LOG_CONTENT_BASIC" "--exclude 'debug' --color-exclude 'blue' --include ''" "$ONLY_EXCLUDE_EXPECTED_OUTPUT"; then
    PASSED_COUNT=$((PASSED_COUNT + 1))
fi

# Test 5: Case-insensitivity
TEST_COUNT=$((TEST_COUNT + 1))
CASE_INSENSITIVE_EXPECTED_OUTPUT="
Oct 26 10:00:00 server kernel: [ 123.456] Some informational message.
Oct 26 10:01:00 server systemd[1]: Starting Some Service...
${RED}Oct 26 10:02:00 server kernel: [ 125.789] An error occurred: disk full.${RESET}
Oct 26 10:03:00 server authpriv: debug: User logged in.
Oct 26 10:04:00 server kernel: [ 128.111] Another informational message.
Oct 26 10:05:00 server systemd[1]: Some Service stopped.
${RED}Oct 26 10:06:00 server kernel: [ 130.222] Critical error: network down.${RESET}
Oct 26 10:07:00 server authpriv: debug: User logged in.
"
if run_test "Case-insensitivity" "$MOCK_LOG_CONTENT_BASIC" "--include 'ERROR' --color-include 'red' --exclude 'DEBUG' --color-exclude 'blue'" "$CASE_INSENSITIVE_EXPECTED_OUTPUT"; then
    PASSED_COUNT=$((PASSED_COUNT + 1))
fi

# --- Summary ---

echo "---------------------"
echo "Test Summary:"
echo "Total tests: $TEST_COUNT"
echo "Passed: $PASSED_COUNT"
echo "Failed: $((TEST_COUNT - PASSED_COUNT))"
echo "---------------------"

if [ "$PASSED_COUNT" -eq "$TEST_COUNT" ]; then
    exit 0 # All tests passed
else
    exit 1 # Some tests failed
fi
