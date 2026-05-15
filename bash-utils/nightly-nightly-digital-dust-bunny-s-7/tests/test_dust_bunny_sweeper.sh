#!/bin/bash

# Test script for nightly-digital-dust-bunny-sweeper

# --- Test Setup ---
TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXXX)
SCRIPT_PATH="$(dirname "$0")"/../src/dust_bunny_sweeper.sh

# Mock rationale: Prevent actual file deletion during tests.
# Instead, capture what would have been deleted.
MOCKED_RM_CALLS=""
rm() {
    MOCKED_RM_CALLS+="rm $*\n"
    # Simulate success
    echo "removed '$*'"
    return 0
}

# Mock rationale: Prevent actual directory deletion during tests.
# Instead, capture what would have been deleted.
MOCKED_RMDIR_CALLS=""
rmdir() {
    MOCKED_RMDIR_CALLS+="rmdir $*\n"
    # Simulate success
    echo "removed directory '$*'"
    return 0
}

# Mock rationale: Simulate user input for confirmation prompts.
# Default to 'y' for tests that expect deletion, 'n' for tests that expect no deletion.
MOCKED_READ_REPLY="y"
read() {
    # Check if it's the confirmation prompt
    if [[ "$*" == *$'Ready to unleash the sweeping magic? (y/N) '* ]]; then
        echo "$MOCKED_READ_REPLY"
        REPLY="$MOCKED_READ_REPLY"
        return 0
    fi
    # Fallback for other read calls if any
    command read "$@"
}

cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

# --- Helper Functions ---
assert_contains() {
    local haystack="$1"
    local needle="$2"
    if ! echo "$haystack" | grep -qF "$needle"; then
        echo "FAIL: Expected '$haystack' to contain '$needle'"
        exit 1
    fi
}

assert_not_contains() {
    local haystack="$1"
    local needle="$2"
    if echo "$haystack" | grep -qF "$needle"; then
        echo "FAIL: Expected '$haystack' not to contain '$needle'"
        exit 1
    fi
}

assert_equals() {
    local actual="$1"
    local expected="$2"
    if [ "$actual" != "$expected" ]; then
        echo "FAIL: Expected '$expected', got '$actual'"
        exit 1
    fi
}

# Function to get an old date string for touch, cross-platform
get_old_date_str() {
    local days_ago=$1
    # Try GNU date first, then BSD date. Fallback to a very old fixed date if both fail.
    date -d "$days_ago days ago" +%Y%m%d%H%M.%S 2>/dev/null || \
    date -v-"$days_ago"d +%Y%m%d%H%M.%S 2>/dev/null || \
    echo "200001010000.00"
}

# --- Test Cases ---

# Test 1: No dust bunnies found
echo "--- Test 1: No dust bunnies found ---"
mkdir -p "$TEST_DIR/recent_dir"
touch "$TEST_DIR/recent_file.txt"
output=$("$SCRIPT_PATH" -d "$TEST_DIR" -a 0)
assert_contains "$output" "No dust bunnies found"
assert_equals "$MOCKED_RM_CALLS" ""
assert_equals "$MOCKED_RMDIR_CALLS" ""
MOCKED_RM_CALLS="" # Reset for next test
MOCKED_RMDIR_CALLS="" # Reset for next test
rm -rf "$TEST_DIR"/* # Clean test dir

# Test 2: Finds old files and empty directories, confirms deletion
echo "--- Test 2: Finds old files and empty directories, confirms deletion ---"
mkdir -p "$TEST_DIR/empty_dir"
mkdir -p "$TEST_DIR/non_empty_dir"
touch "$TEST_DIR/non_empty_dir/file.txt"

OLD_DATE=$(get_old_date_str 8)
touch -t "$OLD_DATE" "$TEST_DIR/old_file.txt"
touch -t "$OLD_DATE" "$TEST_DIR/another_old_file.log"

MOCKED_READ_REPLY="y" # Simulate 'yes'
output=$("$SCRIPT_PATH" -d "$TEST_DIR" -a 7)
assert_contains "$output" "Found these ancient scrolls"
assert_contains "$output" "Discovered these forgotten caverns"
assert_contains "$output" "old_file.txt"
assert_contains "$output" "another_old_file.log"
assert_contains "$output" "empty_dir"
assert_contains "$output" "Sweep complete! 3 digital dust bunnies banished to the void."

assert_contains "$MOCKED_RM_CALLS" "rm $TEST_DIR/old_file.txt"
assert_contains "$MOCKED_RM_CALLS" "rm $TEST_DIR/another_old_file.log"
assert_contains "$MOCKED_RMDIR_CALLS" "rmdir $TEST_DIR/empty_dir"
MOCKED_RM_CALLS=""
MOCKED_RMDIR_CALLS=""
rm -rf "$TEST_DIR"/*

# Test 3: Finds old files and empty directories, declines deletion
echo "--- Test 3: Finds old files and empty directories, declines deletion ---"
mkdir -p "$TEST_DIR/empty_dir"
OLD_DATE=$(get_old_date_str 8)
touch -t "$OLD_DATE" "$TEST_DIR/old_file.txt"

MOCKED_READ_REPLY="n" # Simulate 'no'
output=$("$SCRIPT_PATH" -d "$TEST_DIR" -a 7)
assert_contains "$output" "Found these ancient scrolls"
assert_contains "$output" "Discovered these forgotten caverns"
assert_contains "$output" "Digital dust bunnies get to live another day"
assert_equals "$MOCKED_RM_CALLS" ""
assert_equals "$MOCKED_RMDIR_CALLS" ""
MOCKED_RM_CALLS=""
MOCKED_RMDIR_CALLS=""
rm -rf "$TEST_DIR"/*

# Test 4: Dry run
echo "--- Test 4: Dry run ---"
mkdir -p "$TEST_DIR/empty_dir"
OLD_DATE=$(get_old_date_str 8)
touch -t "$OLD_DATE" "$TEST_DIR/old_file.txt"

output=$("$SCRIPT_PATH" -d "$TEST_DIR" -a 7 -n)
assert_contains "$output" "Found these ancient scrolls"
assert_contains "$output" "Discovered these forgotten caverns"
assert_contains "$output" "(Dry run complete. No changes were made.)"
assert_equals "$MOCKED_RM_CALLS" ""
assert_equals "$MOCKED_RMDIR_CALLS" ""
MOCKED_RM_CALLS=""
MOCKED_RMDIR_CALLS=""
rm -rf "$TEST_DIR"/*

# Test 5: Assume 'yes' (-y)
echo "--- Test 5: Assume 'yes' (-y) ---"
mkdir -p "$TEST_DIR/empty_dir"
OLD_DATE=$(get_old_date_str 8)
touch -t "$OLD_DATE" "$TEST_DIR/old_file.txt"

output=$("$SCRIPT_PATH" -d "$TEST_DIR" -a 7 -y)
assert_contains "$output" "Found these ancient scrolls"
assert_contains "$output" "Discovered these forgotten caverns"
assert_contains "$output" "Sweep complete! 2 digital dust bunnies banished to the void."
assert_contains "$MOCKED_RM_CALLS" "rm $TEST_DIR/old_file.txt"
assert_contains "$MOCKED_RMDIR_CALLS" "rmdir $TEST_DIR/empty_dir"
MOCKED_RM_CALLS=""
MOCKED_RMDIR_CALLS=""
rm -rf "$TEST_DIR"/*

echo "All tests passed!"
