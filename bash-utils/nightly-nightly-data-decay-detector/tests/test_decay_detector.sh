#!/bin/bash

# Mock rationale:
# We need to simulate file system states and modification times deterministically.
# Instead of mocking 'find' directly, we create a controlled temporary directory
# and use 'touch -d' to set specific modification dates for files and directories.
# This allows 'find' to operate on a real, but controlled, filesystem, making the
# tests deterministic and offline without complex mocking frameworks.

# Set -e to exit immediately if a command exits with a non-zero status.
set -e

# Define the path to the script under test
SCRIPT_PATH="../src/decay_detector.sh"

# --- Test Setup ---
TEST_DIR=$(mktemp -d -t decay_detector_test_XXXXXX)
QUARANTINE_TEST_DIR=$(mktemp -d -t quarantine_test_XXXXXX)

cleanup() {
    echo "Cleaning up test directories..."
    rm -rf "$TEST_DIR" "$QUARANTINE_TEST_DIR"
}

# Register the cleanup function to be called on EXIT
trap cleanup EXIT

echo "Test directory: $TEST_DIR"
echo "Quarantine directory: $QUARANTINE_TEST_DIR"

# --- Test Cases ---

# Test 1: No decaying files
echo "\nRunning Test 1: No decaying files..."
# Create files/dirs that are recent (less than 1 day old)
touch "$TEST_DIR/recent_file.txt"
mkdir "$TEST_DIR/recent_dir"

OUTPUT=$("$SCRIPT_PATH" -a 1 "$TEST_DIR")
if echo "$OUTPUT" | grep -q "No decaying items found"; then
    echo "Test 1 Passed."
else
    echo "Test 1 Failed: Expected 'No decaying items found', got:\n$OUTPUT"
    exit 1
fi

# Test 2: Decaying files found
echo "\nRunning Test 2: Decaying files found..."
# Clean up previous test files for isolation
rm -rf "$TEST_DIR"/*

# Create files/dirs that are older than 1 day
touch -d "2 days ago" "$TEST_DIR/old_file.txt"
mkdir "$TEST_DIR/old_dir"
touch -d "3 days ago" "$TEST_DIR/old_dir"

OUTPUT=$("$SCRIPT_PATH" -a 1 "$TEST_DIR")
if echo "$OUTPUT" | grep -q "old_file.txt" && echo "$OUTPUT" | grep -q "old_dir"; then
    echo "Test 2 Passed."
else
    echo "Test 2 Failed: Expected 'old_file.txt' and 'old_dir', got:\n$OUTPUT"
    exit 1
fi

# Test 3: Quarantine mode - files moved
echo "\nRunning Test 3: Quarantine mode - files moved..."
# Clean up previous test files for isolation
rm -rf "$TEST_DIR"/*
rm -rf "$QUARANTINE_TEST_DIR"/*

touch -d "100 days ago" "$TEST_DIR/very_old_file.log"
mkdir -p "$TEST_DIR/very_old_data"
touch -d "100 days ago" "$TEST_DIR/very_old_data"

# Run script in quarantine mode, suppressing stdout for cleaner test output
"$SCRIPT_PATH" -a 90 -q -d "$QUARANTINE_TEST_DIR" "$TEST_DIR" > /dev/null

if [[ -f "$QUARANTINE_TEST_DIR/very_old_file.log" ]] && [[ -d "$QUARANTINE_TEST_DIR/very_old_data" ]]; then
    # Check that items are no longer in the source directory
    if [[ ! -f "$TEST_DIR/very_old_file.log" ]] && [[ ! -d "$TEST_DIR/very_old_data" ]]; then
        echo "Test 3 Passed."
    else
        echo "Test 3 Failed: Items still present in source directory after quarantine."
        ls -l "$TEST_DIR"
        exit 1
    fi
else
    echo "Test 3 Failed: Expected files/dirs in quarantine directory."
    ls -l "$QUARANTINE_TEST_DIR"
    exit 1
fi

# Test 4: Target directory does not exist
echo "\nRunning Test 4: Target directory does not exist..."
OUTPUT=$("$SCRIPT_PATH" /non/existent/path 2>&1 || true) # Capture stderr and prevent script from exiting
if echo "$OUTPUT" | grep -q "Error: Target directory '/non/existent/path' does not exist"; then
    echo "Test 4 Passed."
else
    echo "Test 4 Failed: Expected error for non-existent directory, got:\n$OUTPUT"
    exit 1
fi

# Test 5: Quarantine mode without quarantine directory
echo "\nRunning Test 5: Quarantine mode without quarantine directory..."
OUTPUT=$("$SCRIPT_PATH" -q "$TEST_DIR" 2>&1 || true)
if echo "$OUTPUT" | grep -q "Error: Quarantine mode requires a quarantine directory"; then
    echo "Test 5 Passed."
else
    echo "Test 5 Failed: Expected error for missing quarantine directory, got:\n$OUTPUT"
    exit 1
fi

echo "\nAll tests passed!"
