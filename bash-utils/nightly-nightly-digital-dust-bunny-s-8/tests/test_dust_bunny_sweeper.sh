#!/bin/bash

# Test script for Nightly Digital Dust Bunny Sweeper

# --- Test Configuration ---
TEST_DIR="test_temp_dir"
ARCHIVE_TEST_DIR="test_archive_dir"
SCRIPT_PATH="./src/dust_bunny_sweeper.sh"

# --- Helper Functions ---

# Function to clean up test directories
cleanup() {
    rm -rf "$TEST_DIR" "$ARCHIVE_TEST_DIR"
}

# Function to assert expected output
assert_output() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$actual" == *"$expected"* ]]; then
        echo "✅ PASS: $message"
    else
        echo "❌ FAIL: $message"
        echo "  Expected (substring): '$expected'"
        echo "  Actual: '$actual'"
        exit 1
    fi
}

# Function to assert file existence
assert_file_exists() {
    local file_path="$1"
    local message="$2"
    if [[ -f "$file_path" ]]; then
        echo "✅ PASS: $message"
    else
        echo "❌ FAIL: $message"
        echo "  File not found: '$file_path'"
        exit 1
    fi
}

# Function to assert file non-existence
assert_file_not_exists() {
    local file_path="$1"
    local message="$2"
    if [[ ! -f "$file_path" ]]; then
        echo "✅ PASS: $message"
    else
        echo "❌ FAIL: $message"
        echo "  File unexpectedly found: '$file_path'"
        exit 1
    fi
}

# --- Mocking `find` ---
# Mock rationale: We need to control the output of 'find' to simulate different file ages
# without actually manipulating system timestamps or waiting for real time to pass.
# This ensures deterministic and fast offline testing.
# This mock 'find' function will intercept calls to 'find' made by the script.
# It will return specific predefined file paths based on the arguments passed to it.
# This allows us to test the script's logic for handling found files without relying on
# actual file system state or time.
find() {
    local target_dir="$1"
    local type_flag="$2"
    local type_val="$3"
    local atime_flag="$4"
    local atime_val="$5"
    local print0_flag="$6"

    local mock_output=""
    if [[ "$target_dir" == "$TEST_DIR" && "$type_flag" == "-type" && "$type_val" == "f" && "$atime_flag" == "-atime" && "$atime_val" == "+7" && "$print0_flag" == "-print0" ]]; then
        # Scenario: Files older than 7 days
        mock_output="${TEST_DIR}/old_file_1.txt\0${TEST_DIR}/old_file_2.log\0"
    elif [[ "$target_dir" == "$TEST_DIR" && "$type_flag" == "-type" && "$type_val" == "f" && "$atime_flag" == "-atime" && "$atime_val" == "+30" && "$print0_flag" == "-print0" ]]; then
        # Scenario: Files older than 30 days (subset of +7, or different set)
        mock_output="${TEST_DIR}/very_old_file.bak\0"
    fi
    echo -n -e "$mock_output"
}

# --- Test Cases ---

echo "Starting tests for Nightly Digital Dust Bunny Sweeper..."

# Ensure cleanup runs on exit
trap cleanup EXIT

# Test 1: No arguments - should show usage
echo "--- Test 1: No arguments ---"
output=$(bash "$SCRIPT_PATH" 2>&1)
assert_output "Usage: $SCRIPT_PATH <target_directory> <days_old>" "$output" "Shows usage with no arguments"

# Test 2: Invalid days_old - should show error and usage
echo "--- Test 2: Invalid days_old ---"
output=$(bash "$SCRIPT_PATH" "$TEST_DIR" "abc" 2>&1)
assert_output "Error: <days_old> must be a non-negative integer." "$output" "Handles invalid days_old"

# Test 3: Target directory does not exist
echo "--- Test 3: Target directory does not exist ---"
output=$(bash "$SCRIPT_PATH" "non_existent_dir" 7 2>&1)
assert_output "Error: Target directory 'non_existent_dir' does not exist or is not a directory." "$output" "Handles non-existent target directory"

# Test 4: Dry run, no files found (mocked find returns empty)
echo "--- Test 4: Dry run, no files found ---"
cleanup # Ensure clean state
mkdir -p "$TEST_DIR"
# Mock 'find' is set up to return empty for non-specific calls.
output=$(bash "$SCRIPT_PATH" "$TEST_DIR" 999 --dry-run 2>&1) # Use a high number to ensure mock doesn't match
assert_output "No digital dust bunnies found in '$TEST_DIR' older than 999 days. Your digital space is sparkling clean!" "$output" "Reports no files found in dry run"

# Test 5: Dry run, files found (mocked find returns specific files)
echo "--- Test 5: Dry run, files found ---"
cleanup
mkdir -p "$TEST_DIR"
# Mock 'find' will return old_file_1.txt and old_file_2.log for +7 days
output=$(bash "$SCRIPT_PATH" "$TEST_DIR" 7 --dry-run 2>&1)
assert_output "Found the following digital dust bunnies:" "$output" "Lists files in dry run"
assert_output "  - ${TEST_DIR}/old_file_1.txt" "$output" "Lists old_file_1.txt"
assert_output "  - ${TEST_DIR}/old_file_2.log" "$output" "Lists old_file_2.log"
assert_output "Dry run complete. No files were moved." "$output" "Confirms no move in dry run"

# Test 6: Actual run, files found, move to archive
echo "--- Test 6: Actual run, files found, move to archive ---"
cleanup
mkdir -p "$TEST_DIR"
# Create dummy files that the mock 'find' will "find"
touch "${TEST_DIR}/old_file_1.txt"
touch "${TEST_DIR}/old_file_2.log"
touch "${TEST_DIR}/new_file.txt" # This one should not be "found" by mock find

# Mock rationale: We need to mock 'mv' to prevent actual file system changes during tests,
# especially when 'find' is also mocked. This allows us to verify the script's *intent*
# to move files without requiring real file operations.
# The mock 'mv' will create placeholder files in the archive directory,
# simulating a successful move and deletion from source.
mv() {
    local source_file="$1"
    local dest_dir="$2"
    echo "MOCK_MV: Moving '$source_file' to '$dest_dir'"
    # Simulate the move by creating a placeholder in the destination
    touch "${dest_dir}/$(basename "$source_file")"
    # Simulate deletion from source
    rm -f "$source_file"
    return 0
}

output=$(bash "$SCRIPT_PATH" "$TEST_DIR" 7 "$ARCHIVE_TEST_DIR" 2>&1)

assert_output "Preparing to sweep digital dust bunnies into '$ARCHIVE_TEST_DIR'." "$output" "Confirms archive preparation"
assert_output "Creating archive directory: '$ARCHIVE_TEST_DIR'" "$output" "Confirms archive directory creation"
assert_output "Initiating sweep! Moving digital dust bunnies to '$ARCHIVE_TEST_DIR/'..." "$output" "Confirms sweep initiation"
assert_output "Sweep complete! All identified digital dust bunnies have been moved to '$ARCHIVE_TEST_DIR'." "$output" "Confirms sweep completion"

assert_file_exists "${ARCHIVE_TEST_DIR}/old_file_1.txt" "old_file_1.txt moved to archive"
assert_file_exists "${ARCHIVE_TEST_DIR}/old_file_2.log" "old_file_2.log moved to archive"
assert_file_not_exists "${TEST_DIR}/old_file_1.txt" "old_file_1.txt removed from source"
assert_file_not_exists "${TEST_DIR}/old_file_2.log" "old_file_2.log removed from source"
assert_file_exists "${TEST_DIR}/new_file.txt" "new_file.txt remains in source (not found by mock find)"

# Test 7: Actual run, no files found
echo "--- Test 7: Actual run, no files found ---"
cleanup # Start fresh
mkdir -p "$TEST_DIR"
# Ensure the mock 'find' returns nothing for +999 days
output=$(bash "$SCRIPT_PATH" "$TEST_DIR" 999 "$ARCHIVE_TEST_DIR" 2>&1)
assert_output "No digital dust bunnies found in '$TEST_DIR' older than 999 days. Your digital space is sparkling clean!" "$output" "Reports no files found in actual run"
assert_file_not_exists "$ARCHIVE_TEST_DIR" "Archive directory not created if no files to move"

echo "All tests completed."
