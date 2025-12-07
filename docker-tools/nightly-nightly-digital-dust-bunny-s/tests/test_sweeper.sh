#!/bin/bash

# Test suite for Nightly Digital Dust Bunny Sweeper

# Mock rationale:
# For this utility, mocking system commands like 'find' or 'rm' is less effective
# than creating a controlled temporary file system environment. By creating
# temporary directories and files with specific modification times, we can
# directly test the 'sweeper.sh' script's interaction with the file system
# as it would in a real scenario, ensuring it correctly identifies and deletes
# files based on age and directory paths. This approach provides a more
# robust and realistic test of the script's core functionality.

set -euo pipefail

SCRIPT_PATH="./src/sweeper.sh"
TEST_DIR=$(mktemp -d)
EXIT_CODE=0

# Helper function to create a file with a specific modification time
create_old_file() {
    local path="$1"
    local days_ago="$2"
    mkdir -p "$(dirname "$path")"
    touch -t "$(date -d "$days_ago days ago" +%Y%m%d%H%M.%S)" "$path"
}

# Helper function to create a file with current modification time
create_new_file() {
    local path="$1"
    mkdir -p "$(dirname "$path")"
    touch "$path"
}

# Cleanup function
cleanup() {
    echo "Cleaning up test directory: $TEST_DIR"
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

echo "Starting tests for sweeper.sh"

# Test 1: No directories specified (should fail if not dry-run)
echo "Test 1: No directories specified (should fail)"
if ! "$SCRIPT_PATH" > /dev/null 2>&1; then
    echo "  PASS: Script failed as expected when no directories are specified."
else
    echo "  FAIL: Script did not fail when no directories are specified." >&2
    EXIT_CODE=1
fi

# Test 2: Invalid --age argument
echo "Test 2: Invalid --age argument (should fail)"
if ! "$SCRIPT_PATH" /tmp --age invalid > /dev/null 2>&1; then
    echo "  PASS: Script failed as expected with invalid --age argument."
else
    echo "  FAIL: Script did not fail with invalid --age argument." >&2
    EXIT_CODE=1
fi

# Test 3: Basic cleaning - files older than 7 days
echo "Test 3: Basic cleaning - files older than 7 days"
TEST_SUBDIR="$TEST_DIR/test3"
create_old_file "$TEST_SUBDIR/old_file_1.log" 10
create_old_file "$TEST_SUBDIR/old_file_2.txt" 8
create_new_file "$TEST_SUBDIR/new_file_1.log"
create_old_file "$TEST_SUBDIR/subdir/old_file_3.log" 12
create_new_file "$TEST_SUBDIR/subdir/new_file_2.txt"

"$SCRIPT_PATH" "$TEST_SUBDIR" --age 7 > /dev/null

if [ ! -f "$TEST_SUBDIR/old_file_1.log" ] && \
   [ ! -f "$TEST_SUBDIR/old_file_2.txt" ] && \
   [ ! -f "$TEST_SUBDIR/subdir/old_file_3.log" ] && \
   [ -f "$TEST_SUBDIR/new_file_1.log" ] && \
   [ -f "$TEST_SUBDIR/subdir/new_file_2.txt" ]; then
    echo "  PASS: Correctly deleted old files and kept new ones."
else
    echo "  FAIL: Incorrect file deletion/retention." >&2
    ls -lR "$TEST_SUBDIR" >&2
    EXIT_CODE=1
fi

# Test 4: Dry run - files older than 7 days
echo "Test 4: Dry run - files older than 7 days"
TEST_SUBDIR="$TEST_DIR/test4"
create_old_file "$TEST_SUBDIR/old_file_1.log" 10
create_old_file "$TEST_SUBDIR/old_file_2.txt" 8
create_new_file "$TEST_SUBDIR/new_file_1.log"

DRY_RUN_OUTPUT=$("$SCRIPT_PATH" "$TEST_SUBDIR" --age 7 --dry-run)

if echo "$DRY_RUN_OUTPUT" | grep -q "old_file_1.log" && \
   echo "$DRY_RUN_OUTPUT" | grep -q "old_file_2.txt" && \
   ! echo "$DRY_RUN_OUTPUT" | grep -q "new_file_1.log" && \
   [ -f "$TEST_SUBDIR/old_file_1.log" ] && \
   [ -f "$TEST_SUBDIR/old_file_2.txt" ] && \
   [ -f "$TEST_SUBDIR/new_file_1.log" ]; then
    echo "  PASS: Dry run correctly identified files and did not delete them."
else
    echo "  FAIL: Dry run output or file retention incorrect." >&2
    echo "Dry run output:" >&2
    echo "$DRY_RUN_OUTPUT" >&2
    ls -lR "$TEST_SUBDIR" >&2
    EXIT_CODE=1
fi

# Test 5: Multiple directories
echo "Test 5: Multiple directories"
TEST_SUBDIR_A="$TEST_DIR/test5a"
TEST_SUBDIR_B="$TEST_DIR/test5b"
create_old_file "$TEST_SUBDIR_A/old_a.log" 10
create_new_file "$TEST_SUBDIR_A/new_a.txt"
create_old_file "$TEST_SUBDIR_B/old_b.log" 10
create_new_file "$TEST_SUBDIR_B/new_b.txt"

"$SCRIPT_PATH" "$TEST_SUBDIR_A" "$TEST_SUBDIR_B" --age 7 > /dev/null

if [ ! -f "$TEST_SUBDIR_A/old_a.log" ] && \
   [ -f "$TEST_SUBDIR_A/new_a.txt" ] && \
   [ ! -f "$TEST_SUBDIR_B/old_b.log" ] && \
   [ -f "$TEST_SUBDIR_B/new_b.txt" ]; then
    echo "  PASS: Correctly cleaned multiple directories."
else
    echo "  FAIL: Incorrect cleaning across multiple directories." >&2
    ls -lR "$TEST_SUBDIR_A" >&2
    ls -lR "$TEST_SUBDIR_B" >&2
    EXIT_CODE=1
fi

# Test 6: Directory does not exist (should warn and continue)
echo "Test 6: Non-existent directory (should warn and continue)"
TEST_SUBDIR_EXIST="$TEST_DIR/test6_exist"
TEST_SUBDIR_NONEXIST="$TEST_DIR/test6_nonexist"
create_old_file "$TEST_SUBDIR_EXIST/old.log" 10
create_new_file "$TEST_SUBDIR_EXIST/new.txt"

OUTPUT=$("$SCRIPT_PATH" "$TEST_SUBDIR_EXIST" "$TEST_SUBDIR_NONEXIST" --age 7 2>&1)

if echo "$OUTPUT" | grep -q "Warning: Directory '$TEST_SUBDIR_NONEXIST' does not exist" && \
   [ ! -f "$TEST_SUBDIR_EXIST/old.log" ] && \
   [ -f "$TEST_SUBDIR_EXIST/new.txt" ]; then
    echo "  PASS: Warned about non-existent directory and continued cleaning existing one."
else
    echo "  FAIL: Did not handle non-existent directory correctly." >&2
    echo "Output:" >&2
    echo "$OUTPUT" >&2
    ls -lR "$TEST_SUBDIR_EXIST" >&2
    EXIT_CODE=1
fi

# Test 7: Default age (30 days)
echo "Test 7: Default age (30 days)"
TEST_SUBDIR="$TEST_DIR/test7"
create_old_file "$TEST_SUBDIR/old_35_days.log" 35
create_old_file "$TEST_SUBDIR/old_20_days.log" 20
create_new_file "$TEST_SUBDIR/new_file.log"

"$SCRIPT_PATH" "$TEST_SUBDIR" > /dev/null

if [ ! -f "$TEST_SUBDIR/old_35_days.log" ] && \
   [ -f "$TEST_SUBDIR/old_20_days.log" ] && \
   [ -f "$TEST_SUBDIR/new_file.log" ]; then
    echo "  PASS: Correctly used default age of 30 days."
else
    echo "  FAIL: Default age logic incorrect." >&2
    ls -lR "$TEST_SUBDIR" >&2
    EXIT_CODE=1
fi

echo "All tests complete. Exiting with code $EXIT_CODE"
exit "$EXIT_CODE"
