#!/bin/bash

# Mock rationale: We create a controlled temporary file system environment
# to simulate various "dust bunny" scenarios without touching the actual system.
# This ensures deterministic and offline testing.

# Source the script to be tested (or run it directly)
SCRIPT_TO_TEST="../src/dust_sweeper.sh"

# --- Test Setup ---

# Setup a temporary directory for testing
TEST_DIR=$(mktemp -d -t dust_sweeper_test_XXXXXX)
if [[ ! "$TEST_DIR" || ! -d "$TEST_DIR" ]]; then
  echo "FAIL: Failed to create temp dir"
  exit 1
fi

# Ensure cleanup on exit
cleanup() {
  rm -rf "$TEST_DIR"
  echo "Cleanup: Removed temporary directory $TEST_DIR"
}
trap cleanup EXIT

echo "Test environment created at: $TEST_DIR"

# Create test files and directories

# 1. Empty directory
mkdir "$TEST_DIR/empty_dir"

# 2. Old file (older than 30 days, default threshold)
touch -d "2 months ago" "$TEST_DIR/old_file.txt"

# 3. Newer file (should not be found by -mtime +30)
touch "$TEST_DIR/new_file.txt"

# 4. Temporary files
touch "$TEST_DIR/temp_file.tmp"
touch "$TEST_DIR/backup_file.bak"
touch "$TEST_DIR/emacs_backup~"
touch "$TEST_DIR/log_file.log"
touch "$TEST_DIR/old_config.old"

# 5. File in a subdirectory (also old)
mkdir "$TEST_DIR/subdir"
touch -d "40 days ago" "$TEST_DIR/subdir/old_sub_file.txt"

# 6. Another empty subdirectory
mkdir "$TEST_DIR/subdir/another_empty_dir"

# --- Run the script and capture output ---

echo "\n--- Running $SCRIPT_TO_TEST -p $TEST_DIR -d 30 ---"
OUTPUT=$(bash "$SCRIPT_TO_TEST" -p "$TEST_DIR" -d 30)
EXIT_CODE=$?

echo "\n--- Script Output ---"
echo "$OUTPUT"
echo "---------------------"

# --- Assertions ---

if [[ $EXIT_CODE -ne 0 ]]; then
    echo "FAIL: Script exited with non-zero status code: $EXIT_CODE"
    exit 1
fi

TEST_COUNT=0
PASS_COUNT=0

assert_contains() {
    TEST_COUNT=$((TEST_COUNT + 1))
    if echo "$OUTPUT" | grep -qF "$1"; then
        echo "PASS: Found expected item: $1"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "FAIL: Did not find expected item: $1"
    fi
}

assert_not_contains() {
    TEST_COUNT=$((TEST_COUNT + 1))
    if echo "$OUTPUT" | grep -qF "$1"; then
        echo "FAIL: Found unexpected item: $1"
    else
        echo "PASS: Did not find unexpected item: $1"
        PASS_COUNT=$((PASS_COUNT + 1))
    fi
}

# Check for empty directories
assert_contains "$TEST_DIR/empty_dir"
assert_contains "$TEST_DIR/subdir/another_empty_dir"

# Check for old files
assert_contains "$TEST_DIR/old_file.txt"
assert_contains "$TEST_DIR/subdir/old_sub_file.txt"

# Check for temporary files
assert_contains "$TEST_DIR/temp_file.tmp"
assert_contains "$TEST_DIR/backup_file.bak"
assert_contains "$TEST_DIR/emacs_backup~"
assert_contains "$TEST_DIR/log_file.log"
assert_contains "$TEST_DIR/old_config.old"

# Ensure new file is NOT found
assert_not_contains "$TEST_DIR/new_file.txt"

# --- Summary ---

echo "\n--- Test Summary ---"
if [[ $PASS_COUNT -eq $TEST_COUNT ]]; then
    echo "All $PASS_COUNT/$TEST_COUNT tests passed!"
    exit 0
else
    echo "$PASS_COUNT/$TEST_COUNT tests passed. Some tests failed."
    exit 1
fi
