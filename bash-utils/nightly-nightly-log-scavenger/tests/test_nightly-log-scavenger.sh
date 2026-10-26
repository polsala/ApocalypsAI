#!/bin/bash

# Mock rationale: We create temporary log files to simulate different scenarios
# without touching actual system logs or requiring network access.
# This makes tests deterministic and offline.

SCRIPT_PATH="../src/nightly-log-scavenger.sh"
TEST_DIR=$(mktemp -d)

# Cleanup function
cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

# Test function template
run_test() {
    local test_name="$1"
    local log_content="$2"
    local expected_exit_code="$3"
    local expected_output_contains="$4"
    local expected_output_not_contains="$5"

    local test_log_file="$TEST_DIR/test_log_${test_name}.log"
    echo -e "$log_content" > "$test_log_file"

    echo "--- Running Test: $test_name ---"
    output=$("$SCRIPT_PATH" "$test_log_file" 2>&1)
    exit_code=$?

    echo "Exit Code: $exit_code"
    echo "Output:"
    echo "$output"

    if [[ "$exit_code" -ne "$expected_exit_code" ]]; then
        echo "FAIL: $test_name - Expected exit code $expected_exit_code, got $exit_code"
        return 1
    fi

    if [[ -n "$expected_output_contains" && ! "$output" =~ "$expected_output_contains" ]]; then
        echo "FAIL: $test_name - Output missing expected content: '$expected_output_contains'"
        return 1
    fi

    if [[ -n "$expected_output_not_contains" && "$output" =~ "$expected_output_not_contains" ]]; then
        echo "FAIL: $test_name - Output contains unexpected content: '$expected_output_not_contains'"
        return 1
    fi

    echo "PASS: $test_name"
    return 0
}

# --- Test Cases ---

# Test 1: No issues found
run_test "No_Issues" "This is a normal log entry.\nAnother routine message." 0 "STATUS: All clear! The wasteland is quiet tonight." "Valuable Scraps|Questionable Finds" || exit 1

# Test 2: Valuable Scraps found
run_test "Valuable_Scraps" "This is a normal log.\nERROR: Something critical happened.\nAnother routine message.\nFATAL: System failure." 2 "Total Valuable Scraps Found: 2" "Total Questionable Finds: 0" || exit 1

# Test 3: Questionable Finds found
run_test "Questionable_Finds" "This is a normal log.\nWARNING: Disk space low.\nAnother routine message.\nNOTICE: User logged in." 1 "Total Questionable Finds: 2" "Total Valuable Scraps Found: 0" || exit 1

# Test 4: Both Valuable Scraps and Questionable Finds found
run_test "Both_Finds" "ERROR: Critical system error.\nWARNING: Low memory.\nNOTICE: Configuration changed.\nFATAL: Unrecoverable error." 2 "Total Valuable Scraps Found: 2" "Total Questionable Finds: 2" || exit 1

# Test 5: Empty log file
run_test "Empty_Log" "" 0 "STATUS: All clear! The wasteland is quiet tonight." "Valuable Scraps|Questionable Finds" || exit 1

# Test 6: Log file not found
echo "--- Running Test: Log_Not_Found ---"
output=$("$SCRIPT_PATH" "$TEST_DIR/non_existent.log" 2>&1)
exit_code=$?
if [[ "$exit_code" -ne 1 || ! "$output" =~ "ERROR: Log file '$TEST_DIR/non_existent.log' not found." ]]; then
    echo "FAIL: Log_Not_Found - Expected error for non-existent file."
    exit 1
else
    echo "PASS: Log_Not_Found"
fi

# Test 7: Log file not readable (mock permissions)
echo "--- Running Test: Log_Not_Readable ---"
test_unreadable_log="$TEST_DIR/unreadable.log"
echo "secret content" > "$test_unreadable_log"
chmod 000 "$test_unreadable_log" # Make it unreadable
output=$("$SCRIPT_PATH" "$test_unreadable_log" 2>&1)
exit_code=$?
chmod 644 "$test_unreadable_log" # Restore permissions for cleanup
if [[ "$exit_code" -ne 1 || ! "$output" =~ "ERROR: Log file '$test_unreadable_log' is not readable." ]]; then
    echo "FAIL: Log_Not_Readable - Expected error for unreadable file."
    exit 1
else
    echo "PASS: Log_Not_Readable"
fi

echo "All tests completed."
