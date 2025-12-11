#!/bin/bash

# Tests for Apoc Log Scrubber

# Mock rationale: These tests simulate log files and expected outputs without relying on external files or actual log generation.

# Source the script to be tested
SCRIPT_DIR=$(dirname "$0")
SOURCE_SCRIPT="$SCRIPT_DIR/../src/scrub_log.sh"

# --- Helper Functions ---

# Function to create a temporary test file
create_test_file() {
    local filename="$1"
    local content="$2"
    echo "$content" > "$filename"
    echo "$filename"
}

# Function to clean up temporary files
cleanup_files() {
    rm -f /tmp/test_log_*.txt /tmp/custom_patterns_*.txt
}

# Function to run a test case
run_test() {
    local test_name="$1"
    local script_args="$2"
    local input_log="$3"
    local expected_output="$4"
    local expected_exit_code="$5"
    local test_file="/tmp/test_log_$(date +%s%N).txt"
    local custom_pattern_file="/tmp/custom_patterns_$(date +%s%N).txt"

    echo "Running test: $test_name"

    # Create the input log file
    echo "$input_log" > "$test_file"

    # Create custom pattern file if needed
    if [[ "$script_args" == *"-p"* ]]; then
        local custom_patterns_content="$6"
        echo "$custom_patterns_content" > "$custom_pattern_file"
        script_args="${script_args/custom_patterns_placeholder/$custom_pattern_file}"
    fi

    # Execute the script
    actual_output="$($SOURCE_SCRIPT $script_args "$test_file" 2>&1)"
    actual_exit_code=$?

    # Compare output
    if [ "$actual_exit_code" -eq "$expected_exit_code" ] && [ "$actual_output" == "$expected_output" ]; then
        echo "  PASS: $test_name"
    else
        echo "  FAIL: $test_name"
        echo "    Expected Exit Code: $expected_exit_code, Actual: $actual_exit_code"
        echo "    Expected Output:"
        echo "$expected_output"
        echo "    Actual Output:"
        echo "$actual_output"
    fi

    # Clean up the test log file and custom pattern file
    rm -f "$test_file"
    if [ -n "$custom_pattern_file" ] && [ -f "$custom_pattern_file" ]; then
        rm -f "$custom_pattern_file"
    fi
    echo "--------------------"
}

# --- Test Cases ---

# Test 1: Basic IP address scrubbing (dry run)
input_log_1="User logged in from 192.168.1.100. Another IP: 10.0.0.5."
expected_output_1="User logged in from REDACTED. Another IP: REDACTED."
run_test "IP Address Scrubbing (Dry Run)" "--dry-run" "$input_log_1" "$expected_output_1" 0

# Test 2: Email address scrubbing (in-place)
input_log_2="Contact support@example.com or admin@domain.org for help."
expected_output_2="Contact REDACTED or REDACTED for help."
# For in-place tests, we'll simulate by checking stdout and then verifying the file content separately if needed.
# Here, we'll just check the stdout as if it were the output.
run_test "Email Address Scrubbing (Simulated In-Place)" "-i" "$input_log_2" "$expected_output_2" 0

# Test 3: Mixed scrubbing (IP, Email, Token)
input_log_3="User 1.2.3.4 tried to access token=abcdef1234567890. Email: test@test.com."
expected_output_3="User REDACTED tried to access REDACTED. Email: REDACTED."
run_test "Mixed Scrubbing (IP, Email, Token)" "" "$input_log_3" "$expected_output_3" 0

# Test 4: Custom pattern scrubbing (API Key)
custom_patterns_4="^API_KEY_[A-Za-z0-9]+"
input_log_4="API_KEY_XYZ789 is invalid. Another key: SECRET_ABC."
expected_output_4="API_KEY_REDACTED is invalid. Another key: SECRET_ABC."
run_test "Custom Pattern (API Key)" "-p custom_patterns_placeholder" "$input_log_4" "$expected_output_4" 0 custom_patterns_4

# Test 5: Custom pattern with comments and empty lines
custom_patterns_5="# This is a comment\n\nMY_SECRET_CODE_123\nANOTHER_SECRET_456"
input_log_5="Found MY_SECRET_CODE_123 and ANOTHER_SECRET_456."
expected_output_5="Found REDACTED and REDACTED."
run_test "Custom Pattern with Comments/Empty Lines" "-p custom_patterns_placeholder" "$input_log_5" "$expected_output_5" 0 custom_patterns_5

# Test 6: No sensitive data found
input_log_6="This is a normal log message with no sensitive data."
expected_output_6="This is a normal log message with no sensitive data."
run_test "No Sensitive Data Found" "" "$input_log_6" "$expected_output_6" 0

# Test 7: Invalid log file path
expected_output_7="Error: Log file 'non_existent_log.txt' not found."
run_test "Invalid Log File Path" "" "" "$expected_output_7" 1

# Test 8: Invalid custom pattern file path
expected_output_8="Error: Custom patterns file 'non_existent_patterns.txt' not found."
run_test "Invalid Custom Pattern File Path" "-p non_existent_patterns.txt" "" "$expected_output_8" 1

# Test 9: Empty log file
input_log_9=""
expected_output_9=""
run_test "Empty Log File" "" "$input_log_9" "$expected_output_9" 0

# Test 10: Sensitive data at the beginning and end of the line
input_log_10="192.168.1.100 This is a test email@example.com"
expected_output_10="REDACTED This is a test REDACTED"
run_test "Sensitive Data at Start/End" "" "$input_log_10" "$expected_output_10" 0

# Test 11: Multiple occurrences of the same pattern
input_log_11="IP: 10.0.0.1, IP: 10.0.0.2, IP: 10.0.0.3"
expected_output_11="IP: REDACTED, IP: REDACTED, IP: REDACTED"
run_test "Multiple Occurrences of Same Pattern" "" "$input_log_11" "$expected_output_11" 0

# Test 12: Sensitive data with special characters in value (e.g., password=value with spaces)
input_log_12="password = 'my secret password with spaces'"
expected_output_12="password = 'REDACTED'"
run_test "Sensitive Data with Spaces in Value" "" "$input_log_12" "$expected_output_12" 0

# Test 13: Generic API Key pattern matching
input_log_13="My token is averylongstringofcharactersandnumbers1234567890abcdefghijklmnopqrstuvwxyz"
expected_output_13="My token is REDACTED"
run_test "Generic API Key Pattern Match" "" "$input_log_13" "$expected_output_13" 0

# Test 14: Ensure default patterns are used when no custom file is provided
# This test implicitly checks default patterns are active.
# We'll use a pattern that only exists in default patterns.
input_log_14="User from 172.16.0.1."
expected_output_14="User from REDACTED."
run_test "Default Patterns Active" "" "$input_log_14" "$expected_output_14" 0

# Test 15: Ensure custom patterns override or complement defaults (if they were to overlap, though not in this example)
# This test focuses on ensuring custom patterns are correctly integrated.
custom_patterns_15="^MY_CUSTOM_TOKEN_[a-z0-9]+"
input_log_15="MY_CUSTOM_TOKEN_foobar123 and email@domain.com"
expected_output_15="REDACTED and REDACTED"
run_test "Custom Patterns Integration" "-p custom_patterns_placeholder" "$input_log_15" "$expected_output_15" 0 custom_patterns_15


# --- Cleanup ---
cleanup_files

echo "All tests completed."
exit 0
