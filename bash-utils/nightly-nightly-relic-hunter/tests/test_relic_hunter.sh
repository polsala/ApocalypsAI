#!/bin/bash

# Test script for relic_hunter.sh

SCRIPT_PATH="./src/relic_hunter.sh"
TEST_DIR="/tmp/relic_hunter_test_$(date +%s%N)"
EXIT_CODE=0

# Mock rationale: We need to control the filesystem state and file modification times
# to ensure deterministic test results without relying on the actual system's files.
# Creating temporary files and directories with specific 'touch -d' timestamps allows this.

setup_test_environment() {
    mkdir -p "$TEST_DIR/old_dir"
    mkdir -p "$TEST_DIR/recent_dir"
    mkdir -p "$TEST_DIR/dir with spaces"

    # Create an old file (e.g., 100 days old)
    touch -d "100 days ago" "$TEST_DIR/old_file.txt"
    touch -d "100 days ago" "$TEST_DIR/old_dir/another_old_file.log"
    touch -d "100 days ago" "$TEST_DIR/dir with spaces/old file with spaces.txt"

    # Create a recent file (e.g., 10 days old)
    touch -d "10 days ago" "$TEST_DIR/recent_file.txt"
    touch -d "10 days ago" "$TEST_DIR/recent_dir/another_recent_file.log"

    # Create an old directory (modification time of directory itself)
    touch -d "100 days ago" "$TEST_DIR/old_dir"

    # Create a recent directory
    touch -d "10 days ago" "$TEST_DIR/recent_dir"
}

cleanup_test_environment() {
    rm -rf "$TEST_DIR"
}

# Helper function to run a test case
# Arguments:
# 1: test_name (string)
# 2: command (string) - The command to execute
# 3: expected_items_regex_array (space-separated string of regex patterns for expected items)
# 4: unexpected_items_regex_array (space-separated string of regex patterns for unexpected items)
# 5: expected_exit_code (integer, default 0)
run_test() {
    local test_name="$1"
    local command="$2"
    local expected_items_regex_str="$3"
    local unexpected_items_regex_str="$4"
    local expected_exit_code="${5:-0}"

    # Convert space-separated strings to arrays
    local -a expected_items_regex_array=($expected_items_regex_str)
    local -a unexpected_items_regex_array=($unexpected_items_regex_str)

    echo "Running test: $test_name"
    output=$(eval "$command" 2>&1)
    actual_exit_code=$?

    if [[ $actual_exit_code -ne $expected_exit_code ]]; then
        echo "FAIL: $test_name - Expected exit code $expected_exit_code, got $actual_exit_code"
        echo "Output:\n$output"
        EXIT_CODE=1
        return
    fi

    # Check for expected items
    for item_regex in "${expected_items_regex_array[@]}"; do
        if [[ -n "$item_regex" && ! "$output" =~ $item_regex ]]; then
            echo "FAIL: $test_name - Expected item regex '$item_regex' not found."
            echo "Actual output:\n$output"
            EXIT_CODE=1
            return
        fi
    done

    # Check for unexpected items
    for item_regex in "${unexpected_items_regex_array[@]}"; do
        if [[ -n "$item_regex" && "$output" =~ $item_regex ]]; then
            echo "FAIL: $test_name - Unexpected item regex '$item_regex' found."
            echo "Actual output:\n$output"
            EXIT_CODE=1
            return
        fi
    done

    echo "PASS: $test_name"
}

# --- Main Test Execution ---
cleanup_test_environment # Ensure a clean start
setup_test_environment

# Test 1: No arguments - should show usage and exit with error
run_test "No arguments" "$SCRIPT_PATH" "Usage: .*<path> \[days_old\]" "" 1

# Test 2: Invalid path - should exit with error
run_test "Invalid path" "$SCRIPT_PATH /non/existent/path" "Error: Path '.*' is not a valid directory." "" 1

# Test 3: Invalid days_old - not a number
run_test "Invalid days_old (not number)" "$SCRIPT_PATH $TEST_DIR abc" "Error: Days old must be a positive integer." "" 1

# Test 4: Invalid days_old - zero
run_test "Invalid days_old (zero)" "$SCRIPT_PATH $TEST_DIR 0" "Error: Days old must be a positive integer." "" 1

# Test 5: Find relics older than 90 days (default)
# Should find old_file.txt, another_old_file.log, old_dir, dir with spaces, old file with spaces.txt
run_test "Find relics older than 90 days (default)" \
    "$SCRIPT_PATH $TEST_DIR" \
    ".*old_file.txt.* .*another_old_file.log.* .*old_dir.* .*dir with spaces.* .*old file with spaces.txt.*" \
    ".*recent_file.txt.* .*another_recent_file.log.* .*recent_dir.*" \
    0

# Test 6: Find relics older than 50 days
# Should find old_file.txt, another_old_file.log, old_dir, dir with spaces, old file with spaces.txt
run_test "Find relics older than 50 days" \
    "$SCRIPT_PATH $TEST_DIR 50" \
    ".*old_file.txt.* .*another_old_file.log.* .*old_dir.* .*dir with spaces.* .*old file with spaces.txt.*" \
    ".*recent_file.txt.* .*another_recent_file.log.* .*recent_dir.*" \
    0

# Test 7: Find relics older than 5 days (should find everything)
run_test "Find relics older than 5 days" \
    "$SCRIPT_PATH $TEST_DIR 5" \
    ".*old_file.txt.* .*another_old_file.log.* .*old_dir.* .*recent_file.txt.* .*another_recent_file.log.* .*recent_dir.* .*dir with spaces.* .*old file with spaces.txt.*" \
    "" \
    0

# Test 8: Find relics older than 150 days (should find nothing)
run_test "Find relics older than 150 days" \
    "$SCRIPT_PATH $TEST_DIR 150" \
    "Hunting for digital relics older than 150 days" \
    ".*old_file.txt.* .*recent_file.txt.*" \
    0

cleanup_test_environment

if [ $EXIT_CODE -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Some tests failed."
fi

exit $EXIT_CODE
