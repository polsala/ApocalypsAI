#!/bin/bash

# Test script for Nightly Digital Dust Bunny Sweeper

SCRIPT_TO_TEST="$(dirname "$0")"/../src/dust_bunny_sweeper.sh

# --- Test Utilities ---
assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [ "$expected" == "$actual" ]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message (Expected: '$expected', Actual: '$actual')"
        exit 1
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if echo "$haystack" | grep -qF "$needle"; then
        echo "PASS: $message"
    else
        echo "FAIL: $message (Expected to contain: '$needle', Actual: '$haystack')"
        exit 1
    fi
}

assert_not_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if ! echo "$haystack" | grep -qF "$needle"; then
        echo "PASS: $message"
    else
        echo "FAIL: $message (Expected NOT to contain: '$needle', Actual: '$haystack')"
        exit 1
    fi
}

assert_file_exists() {
    local file="$1"
    local message="$2"
    if [ -f "$file" ]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message (File '$file' does not exist)"
        exit 1
    fi
}

assert_file_not_exists() {
    local file="$1"
    local message="$2"
    if [ ! -f "$file" ]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message (File '$file' unexpectedly exists)"
        exit 1
    fi
}

# --- Setup and Teardown ---
setup() {
    TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXXXXX)
    # Mock rationale: Using mktemp creates a unique, isolated directory for each test run,
    # ensuring determinism and preventing interference with the actual filesystem.
    # All file operations are confined to this temporary directory.
    echo "Test directory: $TEST_DIR"
}

teardown() {
    if [ -d "$TEST_DIR" ]; then
        rm -rf "$TEST_DIR"
        echo "Cleaned up $TEST_DIR"
    fi
}

# --- Test Cases ---

# Test 1: Help message
test_help_message() {
    echo "Running test_help_message..."
    local output=$("$SCRIPT_TO_TEST" --help)
    assert_contains "$output" "Usage: $0 [OPTIONS] [DIRECTORY]" "Help message should contain usage"
    assert_contains "$output" "A whimsical Bash script to find and sweep away old, unused 'digital dust bunnies'" "Help message should contain description"
    assert_equals "0" "$?" "Help message should exit with 0"
}

# Test 2: List old files (dry run)
test_list_old_files() {
    echo "Running test_list_old_files..."
    setup

    # Create an old file (older than 1 day)
    touch "$TEST_DIR/old_file_1.txt"
    sleep 0.1 # Ensure different modification times
    touch "$TEST_DIR/old_file_2.log"
    sleep 0.1
    # Create a new file (current time)
    touch "$TEST_DIR/new_file.tmp"

    # Set modification times for old files
    # Mock rationale: Manually setting modification times for test files ensures
    # predictable 'age' for the `find -mtime` command, making tests deterministic.
    # This avoids reliance on real-time system clock changes.
    find "$TEST_DIR/old_file_1.txt" -exec touch -d "2 days ago" {} \+
    find "$TEST_DIR/old_file_2.log" -exec touch -d "2 days ago" {} \+

    local output=$("$SCRIPT_TO_TEST" -a 1 "$TEST_DIR") # Look for files older than 1 day
    assert_equals "0" "$?" "Script should exit with 0"
    assert_contains "$output" "Found 2 digital dust bunnies." "Should report 2 old files"
    assert_contains "$output" "$TEST_DIR/old_file_1.txt" "Should list old_file_1.txt"
    assert_contains "$output" "$TEST_DIR/old_file_2.log" "Should list old_file_2.log"
    assert_not_contains "$output" "$TEST_DIR/new_file.tmp" "Should not list new_file.tmp"

    assert_file_exists "$TEST_DIR/old_file_1.txt" "Old file 1 should still exist in dry run"
    assert_file_exists "$TEST_DIR/old_file_2.log" "Old file 2 should still exist in dry run"
    assert_file_exists "$TEST_DIR/new_file.tmp" "New file should still exist"

    teardown
}

# Test 3: Delete old files
test_delete_old_files() {
    echo "Running test_delete_old_files..."
    setup

    touch "$TEST_DIR/old_file_to_delete_1.txt"
    sleep 0.1
    touch "$TEST_DIR/old_file_to_delete_2.log"
    sleep 0.1
    touch "$TEST_DIR/new_file_to_keep.tmp"

    find "$TEST_DIR/old_file_to_delete_1.txt" -exec touch -d "2 days ago" {} \+
    find "$TEST_DIR/old_file_to_delete_2.log" -exec touch -d "2 days ago" {} \+

    local output=$("$SCRIPT_TO_TEST" -a 1 -d "$TEST_DIR")
    assert_equals "0" "$?" "Script should exit with 0"
    assert_contains "$output" "Swept away 2 out of 2 identified digital dust bunnies." "Should report 2 files deleted"
    assert_not_contains "$output" "$TEST_DIR/old_file_to_delete_1.txt" "Should not list old_file_to_delete_1.txt in final output"
    assert_not_contains "$output" "$TEST_DIR/old_file_to_delete_2.log" "Should not list old_file_to_delete_2.log in final output"

    assert_file_not_exists "$TEST_DIR/old_file_to_delete_1.txt" "Old file 1 should be deleted"
    assert_file_not_exists "$TEST_DIR/old_file_to_delete_2.log" "Old file 2 should be deleted"
    assert_file_exists "$TEST_DIR/new_file_to_keep.tmp" "New file should still exist"

    teardown
}

# Test 4: No old files
test_no_old_files() {
    echo "Running test_no_old_files..."
    setup

    touch "$TEST_DIR/recent_file_1.txt"
    sleep 0.1
    touch "$TEST_DIR/recent_file_2.log"

    local output=$("$SCRIPT_TO_TEST" -a 1 "$TEST_DIR")
    assert_equals "0" "$?" "Script should exit with 0"
    assert_contains "$output" "Found 0 digital dust bunnies." "Should report 0 old files"
    assert_not_contains "$output" "$TEST_DIR/recent_file_1.txt" "Should not list recent_file_1.txt"

    assert_file_exists "$TEST_DIR/recent_file_1.txt" "Recent file 1 should still exist"
    assert_file_exists "$TEST_DIR/recent_file_2.log" "Recent file 2 should still exist"

    teardown
}

# Test 5: Invalid directory
test_invalid_directory() {
    echo "Running test_invalid_directory..."
    local output=$("$SCRIPT_TO_TEST" -a 1 "/non/existent/path/to/dust" 2>&1)
    assert_equals "0" "$?" "Script should exit with 0 even if directory is invalid (error message printed)"
    assert_contains "$output" "Error: Directory '/non/existent/path/to/dust' does not exist or is not a directory. Skipping." "Should report error for invalid directory"
    assert_contains "$output" "Found 0 digital dust bunnies." "Should report 0 bunnies if no valid dirs"
}

# Test 6: Multiple directories
test_multiple_directories() {
    echo "Running test_multiple_directories..."
    setup
    TEST_DIR_2=$(mktemp -d -t dust-bunny-test-XXXXXXXX)
    echo "Test directory 2: $TEST_DIR_2"

    touch "$TEST_DIR/old_file_dir1.txt"
    find "$TEST_DIR/old_file_dir1.txt" -exec touch -d "2 days ago" {} \+
    touch "$TEST_DIR/new_file_dir1.txt"

    touch "$TEST_DIR_2/old_file_dir2.txt"
    find "$TEST_DIR_2/old_file_dir2.txt" -exec touch -d "2 days ago" {} \+
    touch "$TEST_DIR_2/new_file_dir2.txt"

    local output=$("$SCRIPT_TO_TEST" -a 1 "$TEST_DIR" "$TEST_DIR_2")
    assert_equals "0" "$?" "Script should exit with 0"
    assert_contains "$output" "Found 2 digital dust bunnies." "Should report 2 old files across both dirs"
    assert_contains "$output" "$TEST_DIR/old_file_dir1.txt" "Should list old_file_dir1.txt"
    assert_contains "$output" "$TEST_DIR_2/old_file_dir2.txt" "Should list old_file_dir2.txt"
    assert_file_exists "$TEST_DIR/old_file_dir1.txt" "Old file in dir1 should still exist"
    assert_file_exists "$TEST_DIR_2/old_file_dir2.txt" "Old file in dir2 should still exist"

    rm -rf "$TEST_DIR_2" # Clean up second test dir
    teardown
}

# Test 7: Delete multiple directories
test_delete_multiple_directories() {
    echo "Running test_delete_multiple_directories..."
    setup
    TEST_DIR_2=$(mktemp -d -t dust-bunny-test-XXXXXXXX)
    echo "Test directory 2: $TEST_DIR_2"

    touch "$TEST_DIR/old_file_dir1.txt"
    find "$TEST_DIR/old_file_dir1.txt" -exec touch -d "2 days ago" {} \+
    touch "$TEST_DIR/new_file_dir1.txt"

    touch "$TEST_DIR_2/old_file_dir2.txt"
    find "$TEST_DIR_2/old_file_dir2.txt" -exec touch -d "2 days ago" {} \+
    touch "$TEST_DIR_2/new_file_dir2.txt"

    local output=$("$SCRIPT_TO_TEST" -a 1 -d "$TEST_DIR" "$TEST_DIR_2")
    assert_equals "0" "$?" "Script should exit with 0"
    assert_contains "$output" "Swept away 2 out of 2 identified digital dust bunnies." "Should report 2 files deleted across both dirs"
    assert_file_not_exists "$TEST_DIR/old_file_dir1.txt" "Old file in dir1 should be deleted"
    assert_file_not_exists "$TEST_DIR_2/old_file_dir2.txt" "Old file in dir2 should be deleted"
    assert_file_exists "$TEST_DIR/new_file_dir1.txt" "New file in dir1 should exist"
    assert_file_exists "$TEST_DIR_2/new_file_dir2.txt" "New file in dir2 should exist"

    rm -rf "$TEST_DIR_2" # Clean up second test dir
    teardown
}

# Test 8: Verbose mode
test_verbose_mode() {
    echo "Running test_verbose_mode..."
    setup

    touch "$TEST_DIR/old_verbose_file.txt"
    find "$TEST_DIR/old_verbose_file.txt" -exec touch -d "2 days ago" {} \+
    touch "$TEST_DIR/new_verbose_file.tmp"

    local output=$("$SCRIPT_TO_TEST" -a 1 -v "$TEST_DIR")
    assert_equals "0" "$?" "Script should exit with 0"
    assert_contains "$output" "Searching in: $TEST_DIR" "Verbose mode should show searching directory"
    assert_contains "$output" "Found 1 digital dust bunnies." "Should report 1 old file"

    local output_delete=$("$SCRIPT_TO_TEST" -a 1 -d -v "$TEST_DIR")
    assert_equals "0" "$?" "Script should exit with 0"
    assert_contains "$output_delete" "Sweeping away: $TEST_DIR/old_verbose_file.txt" "Verbose delete mode should show sweeping action"
    assert_contains "$output_delete" "Swept away 1 out of 1 identified digital dust bunnies." "Should report 1 file deleted"

    teardown
}

# Test 9: Age argument validation
test_age_argument_validation() {
    echo "Running test_age_argument_validation..."
    local output=$("$SCRIPT_TO_TEST" -a "not_a_number" 2>&1)
    assert_equals "1" "$?" "Script should exit with 1 for invalid age argument"
    assert_contains "$output" "Error: --age requires a numeric argument." "Should show error for non-numeric age"

    local output_missing=$("$SCRIPT_TO_TEST" -a 2>&1)
    assert_equals "1" "$?" "Script should exit with 1 for missing age argument"
    assert_contains "$output_missing" "Error: --age requires a numeric argument." "Should show error for missing age value"
}


# Run all tests
echo "--- Starting Nightly Digital Dust Bunny Sweeper Tests ---"
test_help_message
test_list_old_files
test_delete_old_files
test_no_old_files
test_invalid_directory
test_multiple_directories
test_delete_multiple_directories
test_verbose_mode
test_age_argument_validation
echo "--- All tests passed! ---"
