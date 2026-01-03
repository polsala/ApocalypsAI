#!/bin/bash

# Tests for nightly-syslog-filter-funnel

# Mock rationale: We are mocking the input by providing predefined strings
# to the script's standard input, simulating syslog messages.

# Source the script to make its functions available for testing
# In a real scenario, you might source the script or call it directly
# and capture its output. For simplicity here, we'll simulate.

# Mock the add_tag function for isolated testing
add_tag() {
    local message="$1"
    local tag=""

    if [[ "$message" == *"error"* ]]; then
        tag="[🚨 ALERT!]";
    elif [[ "$message" == *"warning"* ]]; then
        tag="[⚠️ CAUTION]";
    elif [[ "$message" == *"info"* || "$message" == *"notice"* ]]; then
        tag="[✨ INFO]";
    elif [[ "$message" == *"debug"* ]]; then
        tag="[🔬 DEBUG]";
    elif [[ "$message" == *"critical"* || "$message" == *"emerg"* ]]; then
        tag="[💥 CRITICAL]";
    else
        tag="[❓ UNKNOWN]";
    fi

    echo "$tag $message"
}

# --- Test Cases ---

run_test() {
    local test_name="$1"
    local input_message="$2"
    local expected_output="$3"

    echo "Running test: $test_name"
    actual_output=$(add_tag "$input_message")

    if [ "$actual_output" == "$expected_output" ]; then
        echo "  ✅ PASSED"
    else
        echo "  ❌ FAILED"
        echo "    Expected: $expected_output"
        echo "    Actual:   $actual_output"
        return 1
    fi
    return 0
}

# Test 1: Error message
run_test "Error Message" "This is an error message." "[🚨 ALERT!] This is an error message."
if [ $? -ne 0 ]; then exit 1; fi

# Test 2: Warning message
run_test "Warning Message" "System is showing a warning." "[⚠️ CAUTION] System is showing a warning."
if [ $? -ne 0 ]; then exit 1; fi

# Test 3: Info message
run_test "Info Message" "User logged in successfully." "[✨ INFO] User logged in successfully."
if [ $? -ne 0 ]; then exit 1; fi

# Test 4: Debug message
run_test "Debug Message" "Debug: Variable x is 10." "[🔬 DEBUG] Debug: Variable x is 10."
if [ $? -ne 0 ]; then exit 1; fi

# Test 5: Critical message
run_test "Critical Message" "System failure imminent! Critical error." "[💥 CRITICAL] System failure imminent! Critical error."
if [ $? -ne 0 ]; then exit 1; fi

# Test 6: Unknown message
run_test "Unknown Message" "Just a random log entry." "[❓ UNKNOWN] Just a random log entry."
if [ $? -ne 0 ]; then exit 1; fi

# Test 7: Mixed case message
run_test "Mixed Case Message" "An ERROR occurred." "[🚨 ALERT!] An ERROR occurred."
if [ $? -ne 0 ]; then exit 1; fi

# Test 8: Multiple keywords (should pick the first match)
run_test "Multiple Keywords" "This is a critical error." "[💥 CRITICAL] This is a critical error."
if [ $? -ne 0 ]; then exit 1; fi

# Test 9: Empty message
run_test "Empty Message" "" "[❓ UNKNOWN] "
if [ $? -ne 0 ]; then exit 1; fi

# Test 10: Message with only a keyword
run_test "Keyword Only" "error" "[🚨 ALERT!] error"
if [ $? -ne 0 ]; then exit 1; fi

echo "All tests passed!"
exit 0
