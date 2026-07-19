#!/bin/bash

# Test suite for nightly-scavenge-log.sh

# --- Test Setup ---

# Mock rationale: Sets a unique temporary HOME directory for tests to isolate log files.
# This ensures that tests do not interfere with actual user logs or other test runs.
export HOME="/tmp/test_home_scavenge_log_$(date +%s%N)"
mkdir -p "$HOME"

# Mock rationale: Sets a fixed date for testing to ensure deterministic log file names.
# This allows tests to predict and verify file paths and contents reliably.
export _TEST_DATE="2077-10-23"

# Define the path to the script under test
SCRIPT_PATH="$(dirname "$0")"/../src/scavenge-log.sh

# Ensure the script is executable
chmod +x "$SCRIPT_PATH"

# Create the base log directory within the mocked HOME
mkdir -p "${HOME}/.apocalypsai_scavenge_logs"

# --- Helper Functions for Tests ---

# Function to run the script with specific arguments and capture output
run_script() {
    # Mock rationale: Pass _TEST_DATE to the script to ensure deterministic date-based file operations.
    # The script uses this environment variable to override the current date.
    _TEST_DATE="$_TEST_DATE" "$SCRIPT_PATH" "$@"
}

# Function to assert that a string is present in the output
assert_contains() {
    local expected="$1"
    local actual="$2"
    local test_name="$3"
    if echo "$actual" | grep -qF "$expected"; then
        echo "PASS: $test_name"
    else
        echo "FAIL: $test_name"
        echo "  Expected to contain: '$expected'"
        echo "  Actual output: '$actual'"
        exit 1
    fi
}

# Function to assert that a string is NOT present in the output
assert_not_contains() {
    local unexpected="$1"
    local actual="$2"
    local test_name="$3"
    if echo "$actual" | grep -qF "$unexpected"; then
        echo "FAIL: $test_name"
        echo "  Expected NOT to contain: '$unexpected'"
        echo "  Actual output: '$actual'"
        exit 1
    else
        echo "PASS: $test_name"
    fi
}

# Function to assert equality of two strings
assert_equals() {
    local expected="$1"
    local actual="$2"
    local test_name="$3"
    if [[ "$expected" == "$actual" ]]; then
        echo "PASS: $test_name"
    else
        echo "FAIL: $test_name"
        echo "  Expected: '$expected'"
        echo "  Actual:   '$actual'"
        exit 1
    fi
}

# --- Test Cases ---

test_add_item_success() {
    local log_file="${HOME}/.apocalypsai_scavenge_logs/${_TEST_DATE}.log"
    rm -f "$log_file" # Clean state for this test

    local output=$(run_script add "Rusty Spoon" "Utensils" 2)
    assert_contains "Logged: Rusty Spoon (2) in category 'Utensils' for ${_TEST_DATE}." "$output" "Add item success message"

    assert_contains "Rusty Spoon | Utensils | 2" "$(cat "$log_file")" "Log file content after add"
}

test_add_item_invalid_quantity() {
    local output=$(run_script add "Broken Radio" "Electronics" "zero")
    local exit_code=$?
    assert_contains "Error: Quantity must be a positive integer." "$output" "Add item invalid quantity error"
    assert_not_contains "Logged:" "$output" "Add item invalid quantity should not log"
    assert_equals "1" "$exit_code" "Add item invalid quantity exits with error"
}

test_add_item_missing_args() {
    local output=$(run_script add "Empty Can" "Food")
    local exit_code=$?
    assert_contains "Usage: scavenge-log.sh add \"<item_name>\" \"<category>\" <quantity>" "$output" "Add item missing args error"
    assert_not_contains "Logged:" "$output" "Add item missing args should not log"
    assert_equals "1" "$exit_code" "Add item missing args exits with error"
}

test_view_log_empty() {
    local log_file="${HOME}/.apocalypsai_scavenge_logs/${_TEST_DATE}.log"
    rm -f "$log_file" # Ensure log file for _TEST_DATE is clean before this test

    local output=$(run_script view)
    local exit_code=$?
    assert_contains "No scavenged items logged for today." "$output" "View empty log message"
    assert_equals "0" "$exit_code" "View empty log exits successfully"
}

test_view_log_with_items() {
    local log_file="${HOME}/.apocalypsai_scavenge_logs/${_TEST_DATE}.log"
    rm -f "$log_file" # Clean state for this test

    # Add items first
    run_script add "Mutant Berry" "Food" 5 > /dev/null
    run_script add "Tattered Map" "Info" 1 > /dev/null

    local output=$(run_script view)
    local exit_code=$?
    assert_contains "Mutant Berry | Food | 5" "$output" "View log contains Mutant Berry"
    assert_contains "Tattered Map | Info | 1" "$output" "View log contains Tattered Map"
    assert_contains "Scavenge Log for ${_TEST_DATE}" "$output" "View log header"
    assert_equals "0" "$exit_code" "View log with items exits successfully"
}

test_manifest_specific_date() {
    local specific_date="2077-10-22"
    local specific_log_file="${HOME}/.apocalypsai_scavenge_logs/${specific_date}.log"
    rm -f "$specific_log_file" # Clean state for this test

    # Create a log file for the specific date using a temporary _TEST_DATE override
    _TEST_DATE="$specific_date" run_script add "Old Bottle Cap" "Currency" 10 > /dev/null
    _TEST_DATE="$specific_date" run_script add "Broken Goggles" "Apparel" 1 > /dev/null

    local output=$(run_script manifest "$specific_date")
    local exit_code=$?
    assert_contains "Scavenge Manifest for ${specific_date}" "$output" "Manifest header"
    assert_contains "Old Bottle Cap | Currency | 10" "$output" "Manifest contains Bottle Cap"
    assert_contains "Broken Goggles | Apparel | 1" "$output" "Manifest contains Goggles"
    assert_equals "0" "$exit_code" "Manifest specific date exits successfully"
}

test_manifest_empty_date() {
    local non_existent_date="2077-01-01"
    local non_existent_log_file="${HOME}/.apocalypsai_scavenge_logs/${non_existent_date}.log"
    rm -f "$non_existent_log_file" # Ensure no log file for this date

    local output=$(run_script manifest "$non_existent_date")
    local exit_code=$?
    assert_contains "No scavenged items logged for ${non_existent_date}." "$output" "Manifest empty date message"
    assert_equals "0" "$exit_code" "Manifest empty date exits successfully"
}

test_manifest_invalid_date_format() {
    local output=$(run_script manifest "2077/10/23")
    local exit_code=$?
    assert_contains "Error: Invalid date format. Please use YYYY-MM-DD." "$output" "Manifest invalid date format error"
    assert_equals "1" "$exit_code" "Manifest invalid date format exits with error"
}

test_unknown_command() {
    local output=$(run_script unknown_cmd)
    local exit_code=$?
    assert_contains "Usage: scavenge-log.sh {add|view|manifest}" "$output" "Unknown command usage message"
    assert_equals "1" "$exit_code" "Unknown command exits with error"
}

# --- Run Tests ---
echo "Running tests for nightly-scavenge-log.sh"

test_add_item_success
test_add_item_invalid_quantity
test_add_item_missing_args
test_view_log_empty
test_view_log_with_items
test_manifest_specific_date
test_manifest_empty_date
test_manifest_invalid_date_format
test_unknown_command

echo "All tests passed!"

# --- Teardown ---
rm -rf "$HOME" # Clean up the temporary home directory and its logs
