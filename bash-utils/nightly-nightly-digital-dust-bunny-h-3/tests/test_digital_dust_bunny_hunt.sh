#!/bin/bash

# Test script for nightly-digital-dust-bunny-hunt

SCRIPT_PATH="$(dirname "$0")"/../src/digital_dust_bunny_hunt.sh
TEST_DIR="$(mktemp -d)"

# Mock rationale: We use 'touch -d' to create files with specific modification dates.
# This ensures deterministic test results for 'find -mtime' regardless of the current system date,
# effectively mocking the passage of time for the files.

# Function to run a test case
run_test() {
    local test_name="$1"
    local command="$2"
    local expected_output_regex="$3"
    local expected_exit_code="$4"

    echo "Running test: $test_name"
    output=$(eval "$command" 2>&1)
    exit_code=$?

    if [[ $exit_code -ne $expected_exit_code ]]; then
        echo "FAIL: $test_name - Unexpected exit code. Expected $expected_exit_code, got $exit_code."
        echo "Output: $output"
        return 1
    fi

    if [[ ! "$output" =~ $expected_output_regex ]]; then
        echo "FAIL: $test_name - Output mismatch."
        echo "Expected regex: $expected_output_regex"
        echo "Actual output: $output"
        return 1
    fi

    echo "PASS: $test_name"
    return 0
}

# Setup: Create test files
setup_test_files() {
    mkdir -p "$TEST_DIR/subdir"

    # File 1: Very old (e.g., 100 days old)
    touch -d "$(date -d '100 days ago' +'%Y-%m-%d')" "$TEST_DIR/old_file_1.txt"

    # File 2: Moderately old (e.g., 60 days old)
    touch -d "$(date -d '60 days ago' +'%Y-%m-%d')" "$TEST_DIR/subdir/old_file_2.log"

    # File 3: Recently modified (e.g., 5 days ago)
    touch -d "$(date -d '5 days ago' +'%Y-%m-%d')" "$TEST_DIR/recent_file.md"

    # File 4: Current file
    touch "$TEST_DIR/current_file.json"
}

# Cleanup function
cleanup() {
    rm -rf "$TEST_DIR"
}

# Ensure cleanup runs on exit
trap cleanup EXIT

# Make the script executable
chmod +x "$SCRIPT_PATH"

# --- Test Cases ---

# Test 1: Default scan (90 days) - should find only old_file_1.txt
setup_test_files
run_test \
    "Default scan (90 days)" \
    "$SCRIPT_PATH -d $TEST_DIR" \
    "old_file_1.txt" \
    0

# Test 2: Scan for 30 days - should find old_file_1.txt and old_file_2.log
cleanup && setup_test_files # Reset files for next test
run_test \
    "Scan for 30 days" \
    "$SCRIPT_PATH -d $TEST_DIR -a 30" \
    "old_file_1.txt.*old_file_2.log" \
    0

# Test 3: Scan for 5 days - should find old_file_1.txt, old_file_2.log, and recent_file.md
cleanup && setup_test_files # Reset files for next test
run_test \
    "Scan for 5 days" \
    "$SCRIPT_PATH -d $TEST_DIR -a 5" \
    "old_file_1.txt.*old_file_2.log.*recent_file.md" \
    0

# Test 4: No dust bunnies found (scan for 1 day, all files are older than 1 day relative to their touch date)
# This test needs careful setup to ensure no files are found. Let's make all files very recent.
cleanup
mkdir -p "$TEST_DIR"
touch -d "$(date -d '1 hour ago' +'%Y-%m-%d %H:%M')" "$TEST_DIR/very_recent.txt"
run_test \
    "No dust bunnies found (very recent files)" \
    "$SCRIPT_PATH -d $TEST_DIR -a 0" \
    "No digital dust bunnies found! Your temporal storage is sparkling clean." \
    0

# Test 5: Invalid directory
run_test \
    "Invalid directory" \
    "$SCRIPT_PATH -d /nonexistent/path" \
    "Error: Directory '/nonexistent/path' not found." \
    1

# Test 6: Invalid age threshold (non-numeric)
run_test \
    "Invalid age threshold (non-numeric)" \
    "$SCRIPT_PATH -a abc" \
    "Error: Age threshold must be a positive integer." \
    1

# Test 7: Invalid age threshold (zero)
run_test \
    "Invalid age threshold (zero)" \
    "$SCRIPT_PATH -a 0" \
    "Error: Age threshold must be a positive integer." \
    1

# Test 8: Invalid age threshold (negative)
run_test \
    "Invalid age threshold (negative)" \
    "$SCRIPT_PATH -a -10" \
    "Error: Age threshold must be a positive integer." \
    1

echo "\nAll tests completed."
