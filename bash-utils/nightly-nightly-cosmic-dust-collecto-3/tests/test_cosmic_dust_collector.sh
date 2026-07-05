#!/bin/bash

# Test script for Nightly Cosmic Dust Collector

# --- Test Setup ---
TEST_DIR=$(mktemp -d -t cosmic-dust-test-XXXXXXXX)
SCRIPT_PATH="$(dirname "$0")"/../src/cosmic_dust_collector.sh

# Ensure the script is executable
chmod +x "$SCRIPT_PATH"

# Function to clean up test environment
cleanup() {
    if [[ -d "$TEST_DIR" ]]; then
        rm -rf "$TEST_DIR"
    fi
}

# Register cleanup function to run on exit
trap cleanup EXIT

# Helper function for assertions
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
        echo "FAIL: $message (File '$file' unexpectedly exists)"
        exit 1
    fi
}

# --- Test Cases ---

echo "Running tests for Nightly Cosmic Dust Collector..."

# Test 1: Basic dry-run, no files should be deleted
test_basic_dry_run() {
    echo "--- Test 1: Basic dry-run ---"
    local sub_dir="$TEST_DIR/test1"
    mkdir -p "$sub_dir"

    # Create files with different ages relative to now
    # Mock rationale: `touch -d "N days ago"` is used to create files with specific modification times.
    # This ensures deterministic behavior for `find -mtime +AGE` regardless of when the test runs.
    # This relies on GNU `date` extensions, common in Linux environments.
    touch -d "10 days ago" "$sub_dir/old_file_1.log"
    touch -d "5 days ago" "$sub_dir/old_file_2.log"
    touch -d "1 day ago" "$sub_dir/recent_file.log"
    touch "$sub_dir/new_file.log" # Just created, effectively 0 days old

    local output=$("$SCRIPT_PATH" "$sub_dir" 3 --dry-run --verbose 2>&1)
    local expected_old_file_1=$(basename "$sub_dir/old_file_1.log")
    local expected_old_file_2=$(basename "$sub_dir/old_file_2.log")

    assert_equals 0 $? "Script should exit successfully in dry-run"
    echo "$output" | grep -q "$expected_old_file_1"
    assert_equals 0 $? "Dry-run output should list old_file_1.log"
    echo "$output" | grep -q "$expected_old_file_2"
    assert_equals 0 $? "Dry-run output should list old_file_2.log"
    echo "$output" | grep -q "recent_file.log"
    assert_equals 1 $? "Dry-run output should NOT list recent_file.log"
    echo "$output" | grep -q "new_file.log"
    assert_equals 1 $? "Dry-run output should NOT list new_file.log"

    assert_file_exists "$sub_dir/old_file_1.log" "old_file_1.log should still exist after dry-run"
    assert_file_exists "$sub_dir/old_file_2.log" "old_file_2.log should still exist after dry-run"
    assert_file_exists "$sub_dir/recent_file.log" "recent_file.log should still exist after dry-run"
    assert_file_exists "$sub_dir/new_file.log" "new_file.log should still exist after dry-run"
    echo ""
}

# Test 2: Actual deletion
test_actual_deletion() {
    echo "--- Test 2: Actual deletion ---"
    local sub_dir="$TEST_DIR/test2"
    mkdir -p "$sub_dir"

    touch -d "10 days ago" "$sub_dir/old_file_1.log"
    touch -d "5 days ago" "$sub_dir/old_file_2.log"
    touch -d "1 day ago" "$sub_dir/recent_file.log"
    touch "$sub_dir/new_file.log"

    "$SCRIPT_PATH" "$sub_dir" 3 --verbose 2>&1 # Run with actual deletion

    assert_equals 0 $? "Script should exit successfully after deletion"
    assert_file_does_not_exist "$sub_dir/old_file_1.log" "old_file_1.log should be deleted"
    assert_file_does_not_exist "$sub_dir/old_file_2.log" "old_file_2.log should be deleted"
    assert_file_exists "$sub_dir/recent_file.log" "recent_file.log should NOT be deleted"
    assert_file_exists "$sub_dir/new_file.log" "new_file.log should NOT be deleted"
    echo ""
}

# Test 3: No files to delete
test_no_files_to_delete() {
    echo "--- Test 3: No files to delete ---"
    local sub_dir="$TEST_DIR/test3"
    mkdir -p "$sub_dir"

    touch -d "1 day ago" "$sub_dir/recent_file_1.log"
    touch "$sub_dir/new_file_2.log"

    local output=$("$SCRIPT_PATH" "$sub_dir" 3 --dry-run 2>&1)
    assert_equals 0 $? "Script should exit successfully when no files to delete"
    echo "$output" | grep -q "recent_file_1.log"
    assert_equals 1 $? "No files should be listed in dry-run"
    echo "$output" | grep -q "new_file_2.log"
    assert_equals 1 $? "No files should be listed in dry-run"
    echo ""
}

# Test 4: Invalid directory
test_invalid_directory() {
    echo "--- Test 4: Invalid directory ---"
    local output=$("$SCRIPT_PATH" "$TEST_DIR/non_existent_dir" 5 2>&1)
    assert_equals 1 $? "Script should exit with error for invalid directory"
    echo "$output" | grep -q "Error: Directory '$TEST_DIR/non_existent_dir' does not exist or is not a directory."
    assert_equals 0 $? "Error message for invalid directory should be present"
    echo ""
}

# Test 5: Invalid age
test_invalid_age() {
    echo "--- Test 5: Invalid age ---"
    local output=$("$SCRIPT_PATH" "$TEST_DIR" "abc" 2>&1)
    assert_equals 1 $? "Script should exit with error for invalid age"
    echo "$output" | grep -q "Error: Age must be a positive integer."
    assert_equals 0 $? "Error message for invalid age should be present"
    echo ""
}

# Test 6: Missing arguments
test_missing_arguments() {
    echo "--- Test 6: Missing arguments ---"
    local output=$("$SCRIPT_PATH" "$TEST_DIR" 2>&1)
    assert_equals 1 $? "Script should exit with error for missing age"
    echo "$output" | grep -q "Error: Missing required arguments."
    assert_equals 0 $? "Error message for missing arguments should be present"

    local output2=$("$SCRIPT_PATH" 2>&1)
    assert_equals 1 $? "Script should exit with error for missing all arguments"
    echo "$output2" | grep -q "Error: Missing required arguments."
    assert_equals 0 $? "Error message for missing arguments should be present"
    echo ""
}

# Test 7: Subdirectories and files within them
test_subdirectories() {
    echo "--- Test 7: Subdirectories and files within them ---"
    local sub_dir="$TEST_DIR/test7"
    mkdir -p "$sub_dir/nested1" "$sub_dir/nested2"

    touch -d "10 days ago" "$sub_dir/old_file.log"
    touch -d "10 days ago" "$sub_dir/nested1/old_nested_file.log"
    touch -d "1 day ago" "$sub_dir/nested2/recent_nested_file.log"

    "$SCRIPT_PATH" "$sub_dir" 3 --verbose 2>&1

    assert_equals 0 $? "Script should exit successfully after deletion in subdirectories"
    assert_file_does_not_exist "$sub_dir/old_file.log" "old_file.log in root should be deleted"
    assert_file_does_not_exist "$sub_dir/nested1/old_nested_file.log" "old_nested_file.log should be deleted"
    assert_file_exists "$sub_dir/nested2/recent_nested_file.log" "recent_nested_file.log should NOT be deleted"
    echo ""
}

# Run all tests
test_basic_dry_run
test_actual_deletion
test_no_files_to_delete
test_invalid_directory
test_invalid_age
test_missing_arguments
test_subdirectories

echo "All tests completed."
