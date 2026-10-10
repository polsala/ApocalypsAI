#!/bin/bash
set -euo pipefail

TEST_DIR=$(mktemp -d)
SCRIPT_PATH="../src/dust-bunny-sweeper.sh"

echo "Running tests in temporary directory: $TEST_DIR"

cleanup() {
    echo "Cleaning up test directory: $TEST_DIR"
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

# Mock rationale: Using `touch -d` to set specific modification times allows for deterministic testing of file age,
# independent of the actual current date, making tests reliable and offline. This ensures that files created with
# a past date are consistently identified as 'old' by the script's `-mtime` logic.

# Test 1: Report old files and empty directories
echo "--- Test 1: Report mode ---"
mkdir -p "$TEST_DIR/old_dir" "$TEST_DIR/new_dir" "$TEST_DIR/empty_dir" "$TEST_DIR/nested_empty_dir/sub_empty"
touch -d "2023-01-01" "$TEST_DIR/old_file.txt"
touch -d "2023-01-01" "$TEST_DIR/old_dir/another_old_file.log"
touch "$TEST_DIR/new_file.txt" # Current date
echo "content" > "$TEST_DIR/new_dir/content_file.txt"

# Run in report mode with age 1 day (so 2023-01-01 files are old relative to any current date)
REPORT_OUTPUT=$("$SCRIPT_PATH" -d "$TEST_DIR" -a 1 -c report)

echo "$REPORT_OUTPUT"

if echo "$REPORT_OUTPUT" | grep -q "$TEST_DIR/old_file.txt" && \
   echo "$REPORT_OUTPUT" | grep -q "$TEST_DIR/old_dir/another_old_file.log" && \
   ! echo "$REPORT_OUTPUT" | grep -q "$TEST_DIR/new_file.txt" && \
   echo "$REPORT_OUTPUT" | grep -q "$TEST_DIR/empty_dir" && \
   echo "$REPORT_OUTPUT" | grep -q "$TEST_DIR/nested_empty_dir/sub_empty" && \
   ! echo "$REPORT_OUTPUT" | grep -q "$TEST_DIR/new_dir"; then
    echo "Test 1 PASSED: Correctly reported old files and empty directories."
else
    echo "Test 1 FAILED: Report output incorrect."
    exit 1
fi

# Test 2: Delete old files and empty directories
echo -e "\n--- Test 2: Delete mode ---"
# Recreate test environment for deletion
rm -rf "$TEST_DIR"/*
mkdir -p "$TEST_DIR/old_dir" "$TEST_DIR/new_dir" "$TEST_DIR/empty_dir" "$TEST_DIR/nested_empty_dir/sub_empty"
touch -d "2023-01-01" "$TEST_DIR/old_file_to_delete.txt"
touch -d "2023-01-01" "$TEST_DIR/old_dir/another_old_file_to_delete.log"
touch "$TEST_DIR/new_file_to_keep.txt"
echo "content" > "$TEST_DIR/new_dir/content_file_to_keep.txt"

# Run in delete mode with age 1 day
DELETE_OUTPUT=$("$SCRIPT_PATH" -d "$TEST_DIR" -a 1 -c delete)

echo "$DELETE_OUTPUT"

if [[ ! -f "$TEST_DIR/old_file_to_delete.txt" ]] && \
   [[ ! -f "$TEST_DIR/old_dir/another_old_file_to_delete.log" ]] && \
   [[ -f "$TEST_DIR/new_file_to_keep.txt" ]] && \
   [[ ! -d "$TEST_DIR/empty_dir" ]] && \
   [[ ! -d "$TEST_DIR/nested_empty_dir/sub_empty" ]] && \
   [[ -d "$TEST_DIR/new_dir" ]]; then
    echo "Test 2 PASSED: Correctly deleted old files and empty directories."
else
    echo "Test 2 FAILED: Deletion outcome incorrect."
    ls -R "$TEST_DIR"
    exit 1
fi

# Test 3: No dust bunnies found
echo -e "\n--- Test 3: No dust bunnies found ---"
rm -rf "$TEST_DIR"/*
mkdir -p "$TEST_DIR/only_new_dir"
touch "$TEST_DIR/only_new_file.txt"
echo "content" > "$TEST_DIR/only_new_dir/file.txt"

NO_DUST_OUTPUT=$("$SCRIPT_PATH" -d "$TEST_DIR" -a 1 -c report)

echo "$NO_DUST_OUTPUT"

if echo "$NO_DUST_OUTPUT" | grep -q "No ancient data fragments found" && \
   echo "$NO_DUST_OUTPUT" | grep -q "No echoing voids found"; then
    echo "Test 3 PASSED: Correctly reported no dust bunnies."
else
    echo "Test 3 FAILED: Incorrect output when no dust bunnies."
    exit 1
fi

echo -e "\nAll tests passed!"
