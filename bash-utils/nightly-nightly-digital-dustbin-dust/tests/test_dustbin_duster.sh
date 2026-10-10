#!/bin/bash

# Test script for nightly-digital-dustbin-duster

SCRIPT_PATH="./src/dustbin_duster.sh"
TEST_DIR="/tmp/test_dustbin_duster_$$" # Unique test directory

# --- Mocks ---

# Mock rationale: `find` is mocked to control the list of files the script "discovers".
# This ensures tests are deterministic and don't rely on actual file system state.
find() {
    local target_dir="$1"
    local mtime_arg="$6" # This will be like "+1" or "+7"

    if [[ "$target_dir" == "$TEST_DIR" && "$3" == "-type" && "$4" == "f" && "$5" == "-mtime" ]]; then
        if [[ "$mtime_arg" == "+1" ]]; then
            echo "$TEST_DIR/old_file_1.txt"
            echo "$TEST_DIR/old_file_2.log"
        elif [[ "$mtime_arg" == "+0" ]]; then # For testing DAYS_OLD=0
            echo "$TEST_DIR/old_file_1.txt"
            echo "$TEST_DIR/old_file_2.log"
            echo "$TEST_DIR/new_file.txt"
        else # Default for other mtime values, e.g., +7, +100
            echo "" # No files found by default for other mtime values
        fi
    elif [[ "$target_dir" == "/tmp" && "$3" == "-type" && "$4" == "f" && "$5" == "-mtime" && "$mtime_arg" == "+7" ]]; then
        echo "/tmp/default_old_file.txt"
    else
        # Fallback for other find calls or error cases
        command find "$@"
    fi
}

# Mock rationale: `rm` is mocked to prevent actual file deletion during tests.
# It captures the arguments to verify that the script *would have* deleted the correct files.
MOCKED_RM_CALLS=()
rm() {
    MOCKED_RM_CALLS+=("$@")
    echo "MOCK_RM: Deleted $@"
    return 0 # Simulate successful deletion
}

# Mock rationale: `read` is mocked to provide deterministic user input (e.g., 'y' or 'n')
# without requiring interactive input during automated tests.
MOCKED_READ_REPLY=""
read() {
    # This mock is simplified. In a real scenario, you might parse arguments to `read`
    # to ensure the correct prompt is displayed before returning MOCKED_READ_REPLY.
    # For this utility, we only care about the 'y/N' prompt.
    echo "MOCK_READ: Returning '$MOCKED_READ_REPLY'"
    REPLY="$MOCKED_READ_REPLY"
}

# Mock rationale: `shuf` is mocked to ensure the eulogy selection is deterministic.
# It always returns the first line of its input, making output predictable.
shuf() {
    # Assuming input is piped, and we want the first line
    head -n 1
}

# --- Test Functions ---

setup() {
    mkdir -p "$TEST_DIR"
    touch "$TEST_DIR/old_file_1.txt"
    touch "$TEST_DIR/old_file_2.log"
    touch "$TEST_DIR/new_file.txt" # This file should not be found by default `find` mock
    MOCKED_RM_CALLS=() # Reset mock calls
    MOCKED_READ_REPLY="" # Reset read reply
}

teardown() {
    command rm -rf "$TEST_DIR" # Use actual rm for cleanup
}

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
        echo "FAIL: Expected '$haystack' NOT to contain '$needle'"
        exit 1
    fi
}

assert_equals() {
    local expected="$1"
    local actual="$2"
    if [[ "$expected" != "$actual" ]]; then
        echo "FAIL: Expected '$expected', got '$actual'"
        exit 1
    fi
}

# --- Tests ---

echo "Running tests for nightly-digital-dustbin-duster..."

# Test 1: Dry run, no deletion
setup
echo "Test 1: Dry run, no deletion"
OUTPUT=$($SCRIPT_PATH "$TEST_DIR" 1 --dry-run)
assert_contains "$OUTPUT" "Scanning '$TEST_DIR' for files older than 1 days..."
assert_contains "$OUTPUT" "File: $TEST_DIR/old_file_1.txt"
assert_contains "$OUTPUT" "Action: Would delete"
assert_contains "$OUTPUT" "This was a dry run. No files were actually deleted."
assert_not_contains "$OUTPUT" "Proceed with deletion"
assert_equals "${#MOCKED_RM_CALLS[@]}" 0
echo "Test 1: PASSED"
teardown

# Test 2: Actual deletion, user confirms
setup
echo "Test 2: Actual deletion, user confirms"
MOCKED_READ_REPLY="y"
OUTPUT=$($SCRIPT_PATH "$TEST_DIR" 1)
assert_contains "$OUTPUT" "Scanning '$TEST_DIR' for files older than 1 days..."
assert_contains "$OUTPUT" "File: $TEST_DIR/old_file_1.txt"
assert_contains "$OUTPUT" "Whisper: \"Farewell, digital dust bunny. May your bits find peace in the great beyond.\"" # First eulogy from mock shuf
assert_contains "$OUTPUT" "Proceed with deletion of these files? (y/N): MOCK_READ: Returning 'y'"
assert_contains "$OUTPUT" "[DELETED] $TEST_DIR/old_file_1.txt"
assert_contains "$OUTPUT" "[DELETED] $TEST_DIR/old_file_2.log"
assert_contains "$OUTPUT" "Digital dustbin dusted!"
assert_equals "${#MOCKED_RM_CALLS[@]}" 2
assert_contains "${MOCKED_RM_CALLS[0]}" "$TEST_DIR/old_file_1.txt"
assert_contains "${MOCKED_RM_CALLS[1]}" "$TEST_DIR/old_file_2.log"
echo "Test 2: PASSED"
teardown

# Test 3: Actual deletion, user declines
setup
echo "Test 3: Actual deletion, user declines"
MOCKED_READ_REPLY="n"
OUTPUT=$($SCRIPT_PATH "$TEST_DIR" 1)
assert_contains "$OUTPUT" "Scanning '$TEST_DIR' for files older than 1 days..."
assert_contains "$OUTPUT" "File: $TEST_DIR/old_file_1.txt"
assert_contains "$OUTPUT" "Proceed with deletion of these files? (y/N): MOCK_READ: Returning 'n'"
assert_contains "$OUTPUT" "Aborting. The digital ghosts live to see another day."
assert_equals "${#MOCKED_RM_CALLS[@]}" 0
echo "Test 3: PASSED"
teardown

# Test 4: No old files found (by using a very high DAYS_OLD)
setup
echo "Test 4: No old files found"
OUTPUT=$($SCRIPT_PATH "$TEST_DIR" 100) # Use 100 days, which our mock find won't match
assert_contains "$OUTPUT" "Scanning '$TEST_DIR' for files older than 100 days..."
assert_contains "$OUTPUT" "No digital dust bunnies found. Your system is remarkably tidy!"
assert_not_contains "$OUTPUT" "Proceed with deletion"
assert_equals "${#MOCKED_RM_CALLS[@]}" 0
echo "Test 4: PASSED"
teardown

# Test 5: Invalid DAYS_OLD
setup
echo "Test 5: Invalid DAYS_OLD"
OUTPUT=$($SCRIPT_PATH "$TEST_DIR" "abc" 2>&1) # Redirect stderr to stdout
assert_contains "$OUTPUT" "Error: DAYS_OLD must be a positive integer."
assert_contains "$OUTPUT" "Usage: $SCRIPT_PATH [DIRECTORY] [DAYS_OLD] [--dry-run]"
assert_equals "${#MOCKED_RM_CALLS[@]}" 0
echo "Test 5: PASSED"
teardown

# Test 6: Non-existent directory
setup
echo "Test 6: Non-existent directory"
OUTPUT=$($SCRIPT_PATH "/non/existent/path_$$" 1 2>&1) # Redirect stderr to stdout
assert_contains "$OUTPUT" "Error: Directory '/non/existent/path_$$' not found."
assert_equals "${#MOCKED_RM_CALLS[@]}" 0
echo "Test 6: PASSED"
teardown

# Test 7: Default directory and days_old
setup
echo "Test 7: Default directory and days_old"
MOCKED_READ_REPLY="n" # Decline deletion for this test
OUTPUT=$($SCRIPT_PATH) # No arguments, uses defaults
assert_contains "$OUTPUT" "Scanning '/tmp' for files older than 7 days..."
assert_contains "$OUTPUT" "File: /tmp/default_old_file.txt"
assert_contains "$OUTPUT" "Aborting. The digital ghosts live to see another day."
assert_equals "${#MOCKED_RM_CALLS[@]}" 0
echo "Test 7: PASSED"
teardown

echo "All tests completed."
