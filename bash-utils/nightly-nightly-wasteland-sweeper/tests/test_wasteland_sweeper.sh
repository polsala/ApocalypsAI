#!/bin/bash

# Mock rationale:
# The script relies on 'find' for listing files/directories and 'rm' for deletion.
# To make tests deterministic and offline, these commands are mocked.
# 'find' is mocked to return predefined lists of files/directories.
# 'rm' is mocked to record what it would have deleted without actual file system changes.
# 'read' is mocked to provide predefined user input for confirmation prompts.

# Setup test environment
TEST_DIR=$(mktemp -d)
SCRIPT_PATH="./src/wasteland_sweeper.sh"

# Mock variables
MOCK_FIND_OUTPUT=""
MOCK_RM_CALLED_WITH=""
MOCK_READ_RESPONSE="y" # Default to 'y' for confirmation

# Mock functions
find() {
    # echo "MOCK_FIND_CALLED_WITH: $*" >&2 # For debugging
    echo "$MOCK_FIND_OUTPUT"
}

rm() {
    # echo "MOCK_RM_CALLED_WITH: $*" >&2 # For debugging
    MOCK_RM_CALLED_WITH="$MOCK_RM_CALLED_WITH $*"
    return 0 # Simulate success
}

read() {
    # echo "MOCK_READ_CALLED_WITH: $*" >&2 # For debugging
    echo "$MOCK_READ_RESPONSE"
}

# Helper function to run the script and capture output
run_script() {
    local path="$1"
    local age="$2"
    local dry_run_flag="$3"
    bash "$SCRIPT_PATH" "$path" "$age" "$dry_run_flag"
}

# Test counter
TEST_COUNT=0
PASS_COUNT=0

assert_contains() {
    TEST_COUNT=$((TEST_COUNT + 1))
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if echo "$haystack" | grep -qF "$needle"; then
        echo "PASS: $message"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "FAIL: $message (Expected to contain '$needle', but got: '$haystack')"
    fi
}

assert_not_contains() {
    TEST_COUNT=$((TEST_COUNT + 1))
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if ! echo "$haystack" | grep -qF "$needle"; then
        echo "PASS: $message"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "FAIL: $message (Expected NOT to contain '$needle', but got: '$haystack')"
    fi
}

assert_equals() {
    TEST_COUNT=$((TEST_COUNT + 1))
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$expected" == "$actual" ]]; then
        echo "PASS: $message"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "FAIL: $message (Expected '$expected', but got '$actual')"
    fi
}

# --- Tests ---

echo "Running tests for wasteland_sweeper.sh"

# Test 1: Dry run, no files/dirs
MOCK_FIND_OUTPUT=""
MOCK_RM_CALLED_WITH=""
OUTPUT=$(run_script "$TEST_DIR" 7 --dry-run)
assert_contains "$OUTPUT" "Mode: Dry Run" "Test 1: Dry run mode reported"
assert_contains "$OUTPUT" "No old files found." "Test 1: No old files reported"
assert_contains "$OUTPUT" "No empty directories found." "Test 1: No empty dirs reported"
assert_equals "" "$MOCK_RM_CALLED_WITH" "Test 1: RM not called in dry run with no files"

# Test 2: Dry run, with old files and empty dirs
MOCK_FIND_OUTPUT="${TEST_DIR}/old_file_1\n${TEST_DIR}/old_file_2\n${TEST_DIR}/empty_dir_1\n${TEST_DIR}/empty_dir_2"
MOCK_RM_CALLED_WITH=""
OUTPUT=$(run_script "$TEST_DIR" 7 --dry-run)
assert_contains "$OUTPUT" "Mode: Dry Run" "Test 2: Dry run mode reported"
assert_contains "$OUTPUT" "[FILE] ${TEST_DIR}/old_file_1" "Test 2: Old file 1 listed"
assert_contains "$OUTPUT" "[FILE] ${TEST_DIR}/old_file_2" "Test 2: Old file 2 listed"
assert_contains "$OUTPUT" "[DIR] ${TEST_DIR}/empty_dir_1" "Test 2: Empty dir 1 listed"
assert_contains "$OUTPUT" "[DIR] ${TEST_DIR}/empty_dir_2" "Test 2: Empty dir 2 listed"
assert_contains "$OUTPUT" "(Dry run: Files listed above would be removed.)" "Test 2: Dry run message for files"
assert_contains "$OUTPUT" "(Dry run: Directories listed above would be removed.)" "Test 2: Dry run message for dirs"
assert_equals "" "$MOCK_RM_CALLED_WITH" "Test 2: RM not called in dry run with files"

# Test 3: Live run, with old files and empty dirs, user confirms
MOCK_FIND_OUTPUT="${TEST_DIR}/old_file_3\n${TEST_DIR}/old_file_4\n${TEST_DIR}/empty_dir_3\n${TEST_DIR}/empty_dir_4"
MOCK_RM_CALLED_WITH=""
MOCK_READ_RESPONSE="y"
OUTPUT=$(run_script "$TEST_DIR" 7)
assert_contains "$OUTPUT" "Mode: Live Cleanup" "Test 3: Live cleanup mode reported"
assert_contains "$OUTPUT" "Proceed with deleting these files? (y/N):" "Test 3: File confirmation prompt shown"
assert_contains "$OUTPUT" "Proceed with deleting these empty directories? (y/N):" "Test 3: Dir confirmation prompt shown"
assert_contains "$OUTPUT" "Old files removed." "Test 3: Files reported as removed"
assert_contains "$OUTPUT" "Empty directories removed." "Test 3: Dirs reported as removed"
assert_contains "$MOCK_RM_CALLED_WITH" "rm -v ${TEST_DIR}/old_file_3 ${TEST_DIR}/old_file_4" "Test 3: RM called for files"
assert_contains "$MOCK_RM_CALLED_WITH" "rm -rv ${TEST_DIR}/empty_dir_4 ${TEST_DIR}/empty_dir_3" "Test 3: RM called for dirs (reversed order)" # tac reverses order

# Test 4: Live run, user declines file deletion
MOCK_FIND_OUTPUT="${TEST_DIR}/old_file_5\n${TEST_DIR}/empty_dir_5"
MOCK_RM_CALLED_WITH=""
MOCK_READ_RESPONSE="n" # Decline files, then decline dirs
OUTPUT=$(run_script "$TEST_DIR" 7)
assert_contains "$OUTPUT" "File deletion skipped." "Test 4: File deletion skipped reported"
assert_contains "$OUTPUT" "Empty directory deletion skipped." "Test 4: Empty directory deletion skipped reported"
assert_equals "" "$MOCK_RM_CALLED_WITH" "Test 4: RM not called when user declines"

# Test 5: Invalid path
MOCK_FIND_OUTPUT=""
MOCK_RM_CALLED_WITH=""
OUTPUT=$(run_script "/non/existent/path" 7 2>&1) # Redirect stderr to stdout for capture
assert_contains "$OUTPUT" "Error: Path '/non/existent/path' does not exist or is not a directory." "Test 5: Error for invalid path"

# Test 6: Custom age
MOCK_FIND_OUTPUT="${TEST_DIR}/old_file_6"
MOCK_RM_CALLED_WITH=""
MOCK_READ_RESPONSE="y"
OUTPUT=$(run_script "$TEST_DIR" 3)
assert_contains "$OUTPUT" "Age Threshold: 3 days" "Test 6: Custom age threshold reported"
assert_contains "$OUTPUT" "Scanning for old files (older than 3 days):" "Test 6: Scanning message with custom age"
assert_contains "$MOCK_RM_CALLED_WITH" "rm -v ${TEST_DIR}/old_file_6" "Test 6: RM called for file with custom age"

# Test 7: Empty target path itself should not be listed as an empty dir to remove
# MOCK_FIND_OUTPUT will contain the target path itself if it's empty
MOCK_FIND_OUTPUT="${TEST_DIR}"
MOCK_RM_CALLED_WITH=""
MOCK_READ_RESPONSE="y"
OUTPUT=$(run_script "$TEST_DIR" 7)
assert_not_contains "$OUTPUT" "[DIR] ${TEST_DIR}" "Test 7: Target path itself not listed as empty dir to remove"
assert_contains "$OUTPUT" "No empty directories found (excluding target path itself)." "Test 7: Correct message for empty target path"
assert_not_contains "$MOCK_RM_CALLED_WITH" "rm -rv ${TEST_DIR}" "Test 7: RM not called on target path itself"

# Cleanup
rm -rf "$TEST_DIR"

echo "--- Test Summary ---"
echo "Total tests: $TEST_COUNT"
echo "Passed: $PASS_COUNT"
echo "Failed: $((TEST_COUNT - PASS_COUNT))"

if [[ "$PASS_COUNT" -eq "$TEST_COUNT" ]]; then
    exit 0
else
    exit 1
fi
