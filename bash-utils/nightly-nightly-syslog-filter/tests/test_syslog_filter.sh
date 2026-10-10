#!/bin/bash

# Nightly Syslog Filter - Unit Tests

# Mocking functions for testing

# Mock rationale: This function simulates sending an alert. In a real scenario, it might send an email or trigger an external system. For testing, we capture its output.
alert_message() {
    local level="$1"
    local message="$2"
    echo "MOCK_ALERT:$level:$message" >&2
}

# Mock rationale: This function simulates logging a message. For testing, we capture its output.
log_message() {
    local prefix="$1"
    local message="$2"
    echo "MOCK_LOG:$prefix:$message"
}

# --- Test Setup ---

# Source the main script to use its functions and variables (but override mocked ones)
# Mock rationale: Sourcing the script allows us to test its logic without executing it directly in a live environment. We've already mocked critical functions.
. "src/syslog_filter.sh"

# Create a temporary directory for test configurations
TEST_DIR=$(mktemp -d)

# Function to clean up temporary files
cleanup() {
    rm -rf "$TEST_DIR"
}

# Register cleanup function to run on exit
trap cleanup EXIT

# --- Test Cases ---

run_test() {
    local test_name="$1"
    local input_log="$2"
    local config_content="$3"
    local expected_output="$4"
    local expected_stderr="$5"

    echo "Running test: $test_name"

    # Create a temporary config file
    local config_file="$TEST_DIR/${test_name}_config.txt"
    echo -e "$config_content" > "$config_file"

    # Execute the script with mocked functions and capture stdout/stderr
    # Mock rationale: Using process substitution and pipes allows us to feed input and capture output of the script being tested.
    local actual_output=$(echo -e "$input_log" | ./src/syslog_filter.sh "$config_file" 2> "$TEST_DIR/stderr.log")
    local actual_stderr=$(cat "$TEST_DIR/stderr.log")

    # Compare outputs
    if [ "$actual_output" = "$expected_output" ] && [ "$actual_stderr" = "$expected_stderr" ]; then
        echo "  PASS"
    else
        echo "  FAIL"
        echo "    Expected Output: '$expected_output'"
        echo "    Actual Output:   '$actual_output'"
        echo "    Expected Stderr: '$expected_stderr'"
        echo "    Actual Stderr:   '$actual_stderr'"
        return 1 # Indicate failure
    fi
    return 0 # Indicate success
}

# Test 1: Basic filtering - drop debug, log warning, alert critical
input_log_1="DEBUG:This is a debug message\nWARNING:This is a warning message\nCRITICAL:This is a critical error"
config_1="DEBUG:.*:DROP\nWARNING:.*:LOG\nCRITICAL:.*:ALERT"
expected_output_1="MOCK_LOG:WARNING:This is a warning message"
expected_stderr_1="MOCK_ALERT:CRITICAL:This is a critical error\nALERT: Critical event detected - This is a critical error"
run_test "basic_filter" "$input_log_1" "$config_1" "$expected_output_1" "$expected_stderr_1"

# Test 2: No matching rules - should pass all through (default LOG action)
input_log_2="INFO:Some info\nERROR:Another error"
config_2="DEBUG:.*:DROP"
expected_output_2="MOCK_LOG:INFO:Some info\nMOCK_LOG:ERROR:Another error"
expected_stderr_2=""
run_test "no_matching_rules" "$input_log_2" "$config_2" "$expected_output_2" "$expected_stderr_2"

# Test 3: Drop all messages
input_log_3="INFO:Message 1\nINFO:Message 2"
config_3="INFO:.*:DROP"
expected_output_3=""
expected_stderr_3=""
run_test "drop_all" "$input_log_3" "$config_3" "$expected_output_3" "$expected_stderr_3"

# Test 4: Alert all messages
input_log_4="INFO:Message A\nWARNING:Message B"
config_4="INFO:.*:ALERT\nWARNING:.*:ALERT"
expected_output_4=""
expected_stderr_4="MOCK_ALERT:INFO:Message A\nALERT: Critical event detected - Message A\nMOCK_ALERT:WARNING:Message B\nALERT: Critical event detected - Message B"
run_test "alert_all" "$input_log_4" "$config_4" "$expected_output_4" "$expected_stderr_4"

# Test 5: Specific pattern matching
input_log_5="INFO:app1:request received\nINFO:app2:request processed\nWARNING:app1:low memory"
config_5="INFO:app1:.*:LOG\nWARNING:app1:.*:ALERT"
expected_output_5="MOCK_LOG:INFO:app1:request received"
expected_stderr_5="MOCK_ALERT:WARNING:app1:low memory\nALERT: Critical event detected - app1:low memory"
run_test "specific_pattern" "$input_log_5" "$config_5" "$expected_output_5" "$expected_stderr_5"

# Test 6: Configuration with comments and empty lines
input_log_6="INFO:Normal message\nDEBUG:Ignored debug"
config_6="# This is a comment\nINFO:.*:LOG\n\nDEBUG:.*:DROP"
expected_output_6="MOCK_LOG:INFO:Normal message"
expected_stderr_6=""
run_test "comments_and_empty_lines" "$input_log_6" "$config_6" "$expected_output_6" "$expected_stderr_6"

# Test 7: Missing configuration file (should exit with error)
# Mock rationale: We simulate a missing file by not creating it and checking the script's error output.
echo "Running test: missing_config_file"
# Mock rationale: We redirect stderr to a temporary file to capture the error message.
./src/syslog_filter.sh "non_existent_config.txt" 2> "$TEST_DIR/stderr.log"
if grep -q "Error: Configuration file 'non_existent_config.txt' not found." "$TEST_DIR/stderr.log"; then
    echo "  PASS"
else
    echo "  FAIL"
    echo "    Expected error message not found in stderr."
    echo "    Actual Stderr: $(cat "$TEST_DIR/stderr.log")"
    return 1
fi

exit 0
