#!/bin/bash

# Test suite for nightly-digital-detritus-duster

# Mock rationale:
# We need to test file creation, modification times, and deletion.
# This requires creating temporary files and directories, and using `touch` to manipulate timestamps.
# The `find` and `rm` commands are core to the utility, so we test their interaction with these mock files.
# We capture stdout/stderr to verify the script's output messages.
# A fixed past timestamp is used for "old" files to ensure deterministic test results regardless of when the tests are run.

# --- Test Setup ---
TEST_DIR=$(mktemp -d -t duster-test-XXXXXX)
SCRIPT_PATH="./src/detritus_duster.sh"
EXIT_CODE=0

# Define a fixed old timestamp for deterministic tests
OLD_TIMESTAMP="202001010000.00" # Mock rationale: A fixed past date to ensure files are always "old"

echo "--- Running tests for nightly-digital-detritus-duster ---"
echo "Test directory: $TEST_DIR"

# Ensure the script is executable
chmod +x "$SCRIPT_PATH"

# Function to clean up test environment
cleanup() {
    echo "Cleaning up test directory: $TEST_DIR"
    rm -rf "$TEST_DIR"
    exit $EXIT_CODE
}
trap cleanup EXIT

# Function to assert output contains a string
assert_output_contains() {
    local output="$1"
    local expected_string="$2"
    local test_name="$3"
    if echo "$output" | grep -qF "$expected_string"; then
        echo "PASS: $test_name (contains \"$expected_string\")"
    else
        echo "FAIL: $test_name (expected to contain \"$expected_string\", but got: $output)"
        EXIT_CODE=1
    fi
}

# Function to assert output does NOT contain a string
assert_output_not_contains() {
    local output="$1"
    local unexpected_string="$2"
    local test_name="$3"
    if ! echo "$output" | grep -qF "$unexpected_string"; then
        echo "PASS: $test_name (does not contain \"$unexpected_string\")"
    else
        echo "FAIL: $test_name (expected NOT to contain \"$unexpected_string\", but got: $output)"
        EXIT_CODE=1
    fi
}

# Function to assert file exists
assert_file_exists() {
    local file_path="$1"
    local test_name="$2"
    if [[ -f "$file_path" ]]; then
        echo "PASS: $test_name (file exists: $file_path)"
    else
        echo "FAIL: $test_name (file does not exist: $file_path)"
        EXIT_CODE=1
    fi
}

# Function to assert file does not exist
assert_file_not_exists() {
    local file_path="$1"
    local test_name="$2"
    if [[ ! -f "$file_path" ]]; then
        echo "PASS: $test_name (file does not exist: $file_path)"
    else
        echo "FAIL: $test_name (file exists: $file_path)"
        EXIT_CODE=1
    fi
}

# --- Test Cases ---

# Test 1: Help message
echo "--- Test 1: Help message ---"
OUTPUT=$("$SCRIPT_PATH" -h)
assert_output_contains "$OUTPUT" "Usage: $SCRIPT_PATH <directory> <age_in_days> [OPTIONS]" "Display help"

# Test 2: Missing arguments
echo "--- Test 2: Missing arguments ---"
OUTPUT=$("$SCRIPT_PATH" 2>&1)
assert_output_contains "$OUTPUT" "Error: Missing directory or age_in_days argument." "Missing args error"
OUTPUT=$("$SCRIPT_PATH" "$TEST_DIR" 2>&1)
assert_output_contains "$OUTPUT" "Error: Missing directory or age_in_days argument." "Missing age error"

# Test 3: Invalid age
echo "--- Test 3: Invalid age ---"
OUTPUT=$("$SCRIPT_PATH" "$TEST_DIR" "abc" 2>&1)
assert_output_contains "$OUTPUT" "Error: Age in days must be a positive integer." "Invalid age error"

# Test 4: Non-existent directory
echo "--- Test 4: Non-existent directory ---"
OUTPUT=$("$SCRIPT_PATH" "/non/existent/path" 1 2>&1)
assert_output_contains "$OUTPUT" "Error: Directory '/non/existent/path' does not exist or is not a directory." "Non-existent directory error"

# Test 5: Dry-run with no old files
echo "--- Test 5: Dry-run with no old files ---"
FILE_NEW="$TEST_DIR/new_file.txt"
touch "$FILE_NEW" # Creates file with current timestamp
OUTPUT=$("$SCRIPT_PATH" "$TEST_DIR" 1 2>&1) # Age 1 day, so new file is not old
assert_output_contains "$OUTPUT" "No ancient scrolls or forgotten bits found." "Dry-run no old files"
assert_file_exists "$FILE_NEW" "File should still exist after dry-run"

# Test 6: Dry-run with old files (non-verbose)
echo "--- Test 6: Dry-run with old files (non-verbose) ---"
FILE_OLD_1="$TEST_DIR/old_file_1.log"
FILE_OLD_2="$TEST_DIR/old_file_2.tmp"
touch -t "${OLD_TIMESTAMP}" "$FILE_OLD_1" # Mock rationale: Create file with a fixed old timestamp
touch -t "${OLD_TIMESTAMP}" "$FILE_OLD_2" # Mock rationale: Create file with a fixed old timestamp
OUTPUT=$("$SCRIPT_PATH" "$TEST_DIR" 1 2>&1) # Age 1 day, so both are old
assert_output_contains "$OUTPUT" "Found 2 pieces of digital detritus." "Dry-run found old files count"
assert_output_contains "$OUTPUT" "(Use -v for detailed list)" "Dry-run non-verbose hint"
assert_output_not_contains "$OUTPUT" "$FILE_OLD_1" "Dry-run non-verbose should not list file 1"
assert_output_not_contains "$OUTPUT" "$FILE_OLD_2" "Dry-run non-verbose should not list file 2"
assert_file_exists "$FILE_OLD_1" "Old file 1 should still exist after dry-run"
assert_file_exists "$FILE_OLD_2" "Old file 2 should still exist after dry-run"

# Test 7: Dry-run with old files (verbose)
echo "--- Test 7: Dry-run with old files (verbose) ---"
OUTPUT=$("$SCRIPT_PATH" "$TEST_DIR" 1 -v 2>&1) # Age 1 day, so both are old
assert_output_contains "$OUTPUT" "Found 2 pieces of digital detritus." "Dry-run verbose found old files count"
assert_output_contains "$OUTPUT" "- Found: $FILE_OLD_1" "Dry-run verbose should list file 1"
assert_output_contains "$OUTPUT" "- Found: $FILE_OLD_2" "Dry-run verbose should list file 2"
assert_file_exists "$FILE_OLD_1" "Old file 1 should still exist after verbose dry-run"
assert_file_exists "$FILE_OLD_2" "Old file 2 should still exist after verbose dry-run"

# Test 8: Delete old files (non-verbose)
echo "--- Test 8: Delete old files (non-verbose) ---"
FILE_TO_DELETE_1="$TEST_DIR/delete_me_1.txt"
FILE_TO_DELETE_2="$TEST_DIR/delete_me_2.log"
touch -t "${OLD_TIMESTAMP}" "$FILE_TO_DELETE_1" # Mock rationale: Create file with a fixed old timestamp
touch -t "${OLD_TIMESTAMP}" "$FILE_TO_DELETE_2" # Mock rationale: Create file with a fixed old timestamp
assert_file_exists "$FILE_TO_DELETE_1" "File 1 should exist before deletion"
assert_file_exists "$FILE_TO_DELETE_2" "File 2 should exist before deletion"
OUTPUT=$("$SCRIPT_PATH" "$TEST_DIR" 1 --delete 2>&1) # Age 1 day, so both are old enough
assert_output_contains "$OUTPUT" "CAUTION: Delete mode is ENABLED." "Delete mode warning"
assert_output_contains "$OUTPUT" "Digital detritus swept away silently." "Non-verbose delete message"
assert_output_not_contains "$OUTPUT" "$FILE_TO_DELETE_1" "Non-verbose delete should not list file 1"
assert_output_not_contains "$OUTPUT" "$FILE_TO_DELETE_2" "Non-verbose delete should not list file 2"
assert_file_not_exists "$FILE_TO_DELETE_1" "File 1 should be deleted"
assert_file_not_exists "$FILE_TO_DELETE_2" "File 2 should be deleted"

# Test 9: Delete old files (verbose)
echo "--- Test 9: Delete old files (verbose) ---"
FILE_TO_DELETE_V_1="$TEST_DIR/delete_me_v_1.txt"
FILE_TO_DELETE_V_2="$TEST_DIR/delete_me_v_2.log"
touch -t "${OLD_TIMESTAMP}" "$FILE_TO_DELETE_V_1" # Mock rationale: Create file with a fixed old timestamp
touch -t "${OLD_TIMESTAMP}" "$FILE_TO_DELETE_V_2" # Mock rationale: Create file with a fixed old timestamp
assert_file_exists "$FILE_TO_DELETE_V_1" "Verbose delete file 1 should exist before deletion"
assert_file_exists "$FILE_TO_DELETE_V_2" "Verbose delete file 2 should exist before deletion"
OUTPUT=$("$SCRIPT_PATH" "$TEST_DIR" 1 --delete -v 2>&1) # Age 1 day, so both are old enough
assert_output_contains "$OUTPUT" "CAUTION: Delete mode is ENABLED." "Verbose delete mode warning"
assert_output_contains "$OUTPUT" "- Sweeping: $FILE_TO_DELETE_V_1" "Verbose delete should list file 1"
assert_output_contains "$OUTPUT" "- Sweeping: $FILE_TO_DELETE_V_2" "Verbose delete should list file 2"
assert_file_not_exists "$FILE_TO_DELETE_V_1" "Verbose delete file 1 should be deleted"
assert_file_not_exists "$FILE_TO_DELETE_V_2" "Verbose delete file 2 should be deleted"

# Test 10: Files with spaces in names
echo "--- Test 10: Files with spaces in names ---"
FILE_WITH_SPACES="$TEST_DIR/file with spaces.txt"
touch -t "${OLD_TIMESTAMP}" "$FILE_WITH_SPACES" # Mock rationale: Create file with a fixed old timestamp
OUTPUT=$("$SCRIPT_PATH" "$TEST_DIR" 1 -v 2>&1)
assert_output_contains "$OUTPUT" "- Found: $FILE_WITH_SPACES" "Dry-run verbose should list file with spaces"
assert_file_exists "$FILE_WITH_SPACES" "File with spaces should exist after dry-run"
OUTPUT=$("$SCRIPT_PATH" "$TEST_DIR" 1 --delete 2>&1)
assert_file_not_exists "$FILE_WITH_SPACES" "File with spaces should be deleted"

echo "--- All tests completed ---"
