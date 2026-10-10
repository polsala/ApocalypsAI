#!/bin/bash

# Test script for Nightly Digital Dust Bunny Sweeper

# Define the script to test
SCRIPT_TO_TEST="../src/dust_bunny_sweeper.sh"

# Setup a temporary directory for tests
TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXXX)
if [ ! -d "$TEST_DIR" ]; then
    echo "Failed to create test directory."
    exit 1
fi

# Ensure cleanup on exit
cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

echo "Running tests in: $TEST_DIR"

# --- Test Case 1: No dust bunnies found ---
echo "--- Test Case 1: No dust bunnies found (all files recent) ---"
mkdir -p "$TEST_DIR/recent_dir"
touch "$TEST_DIR/recent_file.txt"
touch "$TEST_DIR/recent_dir/another_recent.log"

OUTPUT=$(cd "$TEST_DIR" && "$SCRIPT_TO_TEST" -d . -a 1 2>&1) # Age 1 day, so everything is recent
if echo "$OUTPUT" | grep -q "No digital dust bunnies found"; then
    echo "PASS: Test Case 1"
else
    echo "FAIL: Test Case 1 - Expected 'No digital dust bunnies found', got:"
    echo "$OUTPUT"
    exit 1
fi

# --- Test Case 2: Dust bunnies found (old files/dirs) ---
echo "--- Test Case 2: Dust bunnies found (old files/dirs) ---"
mkdir -p "$TEST_DIR/old_dir"
touch -t 202001010000 "$TEST_DIR/old_file.txt" # Set timestamp to Jan 1, 2020
touch -t 202001010000 "$TEST_DIR/old_dir" # Set timestamp for directory

# Mock rationale: We are using `touch -t` to create files with specific modification times.
# This makes the `find` command (used by the utility) deterministic, as its output
# depends solely on these controlled timestamps and not the current system time.

OUTPUT=$(cd "$TEST_DIR" && "$SCRIPT_TO_TEST" -d . -a 1 2>&1) # Age 1 day, so old files should be found

if echo "$OUTPUT" | grep -q "old_file.txt" && echo "$OUTPUT" | grep -q "old_dir"; then
    echo "PASS: Test Case 2"
else
    echo "FAIL: Test Case 2 - Expected 'old_file.txt' and 'old_dir' to be found, got:"
    echo "$OUTPUT"
    exit 1
fi

# --- Test Case 3: Invalid age argument ---
echo "--- Test Case 3: Invalid age argument ---"
OUTPUT=$("$SCRIPT_TO_TEST" -a "not_a_number" 2>&1)
if echo "$OUTPUT" | grep -q "Error: Age must be a positive integer"; then
    echo "PASS: Test Case 3"
else
    echo "FAIL: Test Case 3 - Expected error for invalid age, got:"
    echo "$OUTPUT"
    exit 1
fi

# --- Test Case 4: Non-existent directory ---
echo "--- Test Case 4: Non-existent directory ---"
OUTPUT=$("$SCRIPT_TO_TEST" -d "/non/existent/path/12345" 2>&1)
if echo "$OUTPUT" | grep -q "Error: Directory '/non/existent/path/12345' not found"; then
    echo "PASS: Test Case 4"
else
    echo "FAIL: Test Case 4 - Expected error for non-existent directory, got:"
    echo "$OUTPUT"
    exit 1
fi

echo "All tests completed."
