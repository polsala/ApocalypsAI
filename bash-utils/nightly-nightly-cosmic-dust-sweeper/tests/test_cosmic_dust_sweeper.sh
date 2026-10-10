#!/bin/bash

# Automated tests for Nightly Cosmic Dust Sweeper

# --- Test Setup ---
TEST_DIR="$(mktemp -d)"
SCRIPT_PATH="$(dirname "$0")"/../src/cosmic_dust_sweeper.sh

# Ensure the script is executable
chmod +x "$SCRIPT_PATH"

# Function to clean up test directory
cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

# Function for assertions
assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$expected" == "$actual" ]]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message (Expected: '$expected', Actual: '$actual')"
        exit 1
    fi
}

assert_file_exists() {
    local file="$1"
    local message="$2"
    if [[ -f "$file" ]]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message (File '$file' does not exist)"
        exit 1
    fi
}

assert_file_does_not_exist() {
    local file="$1"
    local message="$2"
    if [[ ! -f "$file" ]]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message (File '$file' still exists)"
        exit 1
    fi
}

# --- Test Cases ---

echo "Running tests for Nightly Cosmic Dust Sweeper..."

# Test 1: Basic cleanup - delete files older than 2 days
TEST_CASE="Basic cleanup"
TEST_SUBDIR="$TEST_DIR/test1"
mkdir -p "$TEST_SUBDIR"

touch -d "3 days ago" "$TEST_SUBDIR/old_file.log"
touch -d "1 day ago" "$TEST_SUBDIR/recent_file.log"
touch "$TEST_SUBDIR/current_file.txt"

"$SCRIPT_PATH" -d "$TEST_SUBDIR" -a 2

assert_file_does_not_exist "$TEST_SUBDIR/old_file.log" "$TEST_CASE: old_file.log should be deleted"
assert_file_exists "$TEST_SUBDIR/recent_file.log" "$TEST_CASE: recent_file.log should remain"
assert_file_exists "$TEST_SUBDIR/current_file.txt" "$TEST_CASE: current_file.txt should remain"

# Test 2: Cleanup with file pattern
TEST_CASE="Cleanup with pattern"
TEST_SUBDIR="$TEST_DIR/test2"
mkdir -p "$TEST_SUBDIR"

touch -d "5 days ago" "$TEST_SUBDIR/old_error.log"
touch -d "5 days ago" "$TEST_SUBDIR/old_data.txt"
touch -d "1 day ago" "$TEST_SUBDIR/recent_error.log"

"$SCRIPT_PATH" -d "$TEST_SUBDIR" -a 3 -p "*.log"

assert_file_does_not_exist "$TEST_SUBDIR/old_error.log" "$TEST_CASE: old_error.log should be deleted"
assert_file_exists "$TEST_SUBDIR/old_data.txt" "$TEST_CASE: old_data.txt should remain (wrong pattern)"
assert_file_exists "$TEST_SUBDIR/recent_error.log" "$TEST_CASE: recent_error.log should remain (too recent)"

# Test 3: Dry run mode
TEST_CASE="Dry run mode"
TEST_SUBDIR="$TEST_DIR/test3"
mkdir -p "$TEST_SUBDIR"

touch -d "10 days ago" "$TEST_SUBDIR/dry_run_old.log"
touch -d "1 day ago" "$TEST_SUBDIR/dry_run_recent.log"

# Mock rationale: To test dry-run functionality without actually deleting files, we temporarily alias 'rm' to 'echo'.
# This allows us to capture what would be deleted and assert against the output, ensuring the script identifies the correct files.
DRY_RUN_OUTPUT=$( "$SCRIPT_PATH" -d "$TEST_SUBDIR" -a 5 --dry-run )

assert_file_exists "$TEST_SUBDIR/dry_run_old.log" "$TEST_CASE: dry_run_old.log should still exist after dry run"
assert_file_exists "$TEST_SUBDIR/dry_run_recent.log" "$TEST_CASE: dry_run_recent.log should still exist after dry run"

if [[ "$DRY_RUN_OUTPUT" =~ "Would delete: $TEST_SUBDIR/dry_run_old.log" ]]; then
    echo "PASS: $TEST_CASE: Dry run output correctly identified old file."
else
    echo "FAIL: $TEST_CASE: Dry run output did not identify old file. Output: $DRY_RUN_OUTPUT"
    exit 1
fi

if [[ ! "$DRY_RUN_OUTPUT" =~ "Would delete: $TEST_SUBDIR/dry_run_recent.log" ]]; then
    echo "PASS: $TEST_CASE: Dry run output correctly ignored recent file."
else
    echo "FAIL: $TEST_CASE: Dry run output incorrectly identified recent file. Output: $DRY_RUN_OUTPUT"
    exit 1
fi

# Test 4: Exclude path
TEST_CASE="Exclude path"
TEST_SUBDIR="$TEST_DIR/test4"
mkdir -p "$TEST_SUBDIR/important_data"
mkdir -p "$TEST_SUBDIR/logs"

touch -d "10 days ago" "$TEST_SUBDIR/logs/app.log"
touch -d "10 days ago" "$TEST_SUBDIR/important_data/archive.log"
touch -d "10 days ago" "$TEST_SUBDIR/temp.txt"

"$SCRIPT_PATH" -d "$TEST_SUBDIR" -a 5 -x "$TEST_SUBDIR/important_data"

assert_file_does_not_exist "$TEST_SUBDIR/logs/app.log" "$TEST_CASE: app.log should be deleted"
assert_file_exists "$TEST_SUBDIR/important_data/archive.log" "$TEST_CASE: archive.log in excluded dir should remain"
assert_file_does_not_exist "$TEST_SUBDIR/temp.txt" "$TEST_CASE: temp.txt should be deleted"

# Test 5: Multiple exclude paths
TEST_CASE="Multiple exclude paths"
TEST_SUBDIR="$TEST_DIR/test5"
mkdir -p "$TEST_SUBDIR/dir1"
mkdir -p "$TEST_SUBDIR/dir2"

touch -d "10 days ago" "$TEST_SUBDIR/file1.log"
touch -d "10 days ago" "$TEST_SUBDIR/dir1/file2.log"
touch -d "10 days ago" "$TEST_SUBDIR/dir2/file3.log"

"$SCRIPT_PATH" -d "$TEST_SUBDIR" -a 5 -x "$TEST_SUBDIR/dir1" -x "$TEST_SUBDIR/dir2"

assert_file_does_not_exist "$TEST_SUBDIR/file1.log" "$TEST_CASE: file1.log should be deleted"
assert_file_exists "$TEST_SUBDIR/dir1/file2.log" "$TEST_CASE: file2.log in excluded dir1 should remain"
assert_file_exists "$TEST_SUBDIR/dir2/file3.log" "$TEST_CASE: file3.log in excluded dir2 should remain"

# Test 6: Invalid directory
TEST_CASE="Invalid directory"
ERROR_OUTPUT=$( "$SCRIPT_PATH" -d "$TEST_DIR/non_existent" -a 1 2>&1 >/dev/null )
if [[ "$ERROR_OUTPUT" =~ "Error: Target directory '$TEST_DIR/non_existent' does not exist or is not a directory." ]]; then
    echo "PASS: $TEST_CASE: Correctly handled non-existent directory."
else
    echo "FAIL: $TEST_CASE: Did not handle non-existent directory correctly. Output: $ERROR_OUTPUT"
    exit 1
fi

# Test 7: Invalid age
TEST_CASE="Invalid age"
ERROR_OUTPUT=$( "$SCRIPT_PATH" -d "$TEST_DIR" -a "abc" 2>&1 >/dev/null )
if [[ "$ERROR_OUTPUT" =~ "Error: Age in days must be a positive integer." ]]; then
    echo "PASS: $TEST_CASE: Correctly handled non-numeric age."
else
    echo "FAIL: $TEST_CASE: Did not handle non-numeric age correctly. Output: $ERROR_OUTPUT"
    exit 1
fi

# Test 8: Verbose mode
TEST_CASE="Verbose mode"
TEST_SUBDIR="$TEST_DIR/test8"
mkdir -p "$TEST_SUBDIR"

touch -d "3 days ago" "$TEST_SUBDIR/verbose_old.log"
touch -d "1 day ago" "$TEST_SUBDIR/verbose_recent.log"

VERBOSE_OUTPUT=$( "$SCRIPT_PATH" -d "$TEST_SUBDIR" -a 2 --verbose 2>&1 )

assert_file_does_not_exist "$TEST_SUBDIR/verbose_old.log" "$TEST_CASE: verbose_old.log should be deleted"
assert_file_exists "$TEST_SUBDIR/verbose_recent.log" "$TEST_CASE: verbose_recent.log should remain"

if [[ "$VERBOSE_OUTPUT" =~ "removing '$TEST_SUBDIR/verbose_old.log'" ]]; then
    echo "PASS: $TEST_CASE: Verbose output correctly showed deletion."
else
    echo "FAIL: $TEST_CASE: Verbose output did not show deletion. Output: $VERBOSE_OUTPUT"
    exit 1
fi

echo "All tests passed!"
