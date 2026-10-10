#!/bin/bash

set -euo pipefail

# Define the path to the script under test
SCRIPT_PATH="./src/temporal_pocket_cleaner.sh"

# Define a temporary directory for tests
TEST_DIR=""

# --- Helper Functions ---

# Function to create a temporary test directory
setup_test_environment() {
    TEST_DIR=$(mktemp -d -t temporal_pocket_test_XXXXXX)
    echo "Created test directory: $TEST_DIR"
    chmod +x "$SCRIPT_PATH" # Ensure the script is executable for tests
}

# Function to clean up the temporary test directory
cleanup_test_environment() {
    if [[ -d "$TEST_DIR" ]]; then
        rm -rf "$TEST_DIR"
        echo "Cleaned up test directory: $TEST_DIR"
    fi
}

# Function to assert a condition
assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$expected" != "$actual" ]]; then
        echo "FAIL: $message"
        echo "  Expected: '$expected'"
        echo "  Actual:   '$actual'"
        cleanup_test_environment
        exit 1
    else
        echo "PASS: $message"
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if ! echo "$haystack" | grep -qF "$needle"; then
        echo "FAIL: $message"
        echo "  Expected to contain: '$needle'"
        echo "  Actual output: '$haystack'"
        cleanup_test_environment
        exit 1
    else
        echo "PASS: $message"
    fi
}

assert_not_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if echo "$haystack" | grep -qF "$needle"; then
        echo "FAIL: $message"
        echo "  Expected NOT to contain: '$needle'"
        echo "  Actual output: '$haystack'"
        cleanup_test_environment
        exit 1
    else
        echo "PASS: $message"
    fi
}

# --- Test Cases ---

test_clean_command() {
    echo "--- Running test_clean_command ---"
    local current_dir="$TEST_DIR/data"
    mkdir -p "$current_dir"

    # Create files with different ages
    # Mock rationale: Using `touch -d` to set specific modification times for files
    # allows deterministic testing of the `find -mtime` logic in the main script,
    # independent of the actual system clock.
    touch -d "2 days ago" "$current_dir/recent_file.txt"
    touch -d "10 days ago" "$current_dir/old_file_1.log"
    touch -d "40 days ago" "$current_dir/old_file_2.json"
    touch -d "5 days ago" "$current_dir/another_recent.md"
    mkdir "$current_dir/subdir" # Should not be moved

    # Run clean command for files older than 7 days
    "$SCRIPT_PATH" clean "$current_dir" 7 > /dev/null

    # Check if recent files are still in current_dir
    assert_equals "1" "$(find "$current_dir" -maxdepth 1 -type f -name "recent_file.txt" | wc -l)" "recent_file.txt should remain"
    assert_equals "1" "$(find "$current_dir" -maxdepth 1 -type f -name "another_recent.md" | wc -l)" "another_recent.md should remain"

    # Check if old files are in the temporal pocket
    local pocket_path="$current_dir/.temporal_pocket"
    assert_equals "1" "$(find "$pocket_path" -maxdepth 1 -type f -name "old_file_1.log" | wc -l)" "old_file_1.log should be in pocket"
    assert_equals "1" "$(find "$pocket_path" -maxdepth 1 -type f -name "old_file_2.json" | wc -l)" "old_file_2.json should be in pocket"

    # Check if old files are NOT in current_dir anymore
    assert_equals "0" "$(find "$current_dir" -maxdepth 1 -type f -name "old_file_1.log" | wc -l)" "old_file_1.log should NOT be in current_dir"
    assert_equals "0" "$(find "$current_dir" -maxdepth 1 -type f -name "old_file_2.json" | wc -l)" "old_file_2.json should NOT be in current_dir"

    # Check that the subdirectory was not moved
    assert_equals "1" "$(find "$current_dir" -maxdepth 1 -type d -name "subdir" | wc -l)" "subdir should remain"
}

test_list_command() {
    echo "--- Running test_list_command ---"
    local current_dir="$TEST_DIR/list_data"
    mkdir -p "$current_dir/.temporal_pocket"

    # Create files directly in the pocket for listing
    # Mock rationale: Directly creating files in the `.temporal_pocket` simulates
    # the state after a `clean` operation, allowing deterministic testing of the `list` command's output.
    touch "$current_dir/.temporal_pocket/pocket_file_A.txt"
    touch "$current_dir/.temporal_pocket/pocket_file_B.log"
    touch "$current_dir/.temporal_pocket/pocket_file_C.json"

    local output=$("$SCRIPT_PATH" list "$current_dir")

    assert_contains "$output" "pocket_file_A.txt" "List output should contain pocket_file_A.txt"
    assert_contains "$output" "pocket_file_B.log" "List output should contain pocket_file_B.log"
    assert_contains "$output" "pocket_file_C.json" "List output should contain pocket_file_C.json"
    assert_contains "$output" "Files in temporal pocket" "List output should have header"

    # Test empty pocket
    local empty_dir="$TEST_DIR/empty_pocket_data"
    mkdir -p "$empty_dir"
    output=$("$SCRIPT_PATH" list "$empty_dir")
    assert_contains "$output" "Temporal pocket '$empty_dir/.temporal_pocket' does not exist or is empty." "List output for empty pocket should indicate it's empty"
}

test_retrieve_command_specific() {
    echo "--- Running test_retrieve_command_specific ---"
    local current_dir="$TEST_DIR/retrieve_data"
    mkdir -p "$current_dir/.temporal_pocket"

    # Create files in the pocket
    # Mock rationale: Similar to `test_list_command`, creating files directly in
    # the pocket sets up a known state for testing retrieval.
    touch "$current_dir/.temporal_pocket/retrieve_me_1.txt"
    touch "$current_dir/.temporal_pocket/dont_retrieve_me.log"
    touch "$current_dir/.temporal_pocket/retrieve_me_2.txt"

    # Retrieve a specific file
    "$SCRIPT_PATH" retrieve "$current_dir" "retrieve_me_1.txt" > /dev/null

    # Check if the file is back in current_dir
    assert_equals "1" "$(find "$current_dir" -maxdepth 1 -type f -name "retrieve_me_1.txt" | wc -l)" "retrieve_me_1.txt should be back in current_dir"
    # Check if it's gone from the pocket
    assert_equals "0" "$(find "$current_dir/.temporal_pocket" -maxdepth 1 -type f -name "retrieve_me_1.txt" | wc -l)" "retrieve_me_1.txt should be gone from pocket"

    # Check that other files are still in the pocket
    assert_equals "1" "$(find "$current_dir/.temporal_pocket" -maxdepth 1 -type f -name "dont_retrieve_me.log" | wc -l)" "dont_retrieve_me.log should still be in pocket"
    assert_equals "1" "$(find "$current_dir/.temporal_pocket" -maxdepth 1 -type f -name "retrieve_me_2.txt" | wc -l)" "retrieve_me_2.txt should still be in pocket"
}

test_retrieve_command_all() {
    echo "--- Running test_retrieve_command_all ---"
    local current_dir="$TEST_DIR/retrieve_all_data"
    mkdir -p "$current_dir/.temporal_pocket"

    # Create files in the pocket
    touch "$current_dir/.temporal_pocket/all_file_1.txt"
    touch "$current_dir/.temporal_pocket/all_file_2.log"

    # Retrieve all files
    "$SCRIPT_PATH" retrieve "$current_dir" > /dev/null

    # Check if all files are back in current_dir
    assert_equals "1" "$(find "$current_dir" -maxdepth 1 -type f -name "all_file_1.txt" | wc -l)" "all_file_1.txt should be back in current_dir"
    assert_equals "1" "$(find "$current_dir" -maxdepth 1 -type f -name "all_file_2.log" | wc -l)" "all_file_2.log should be back in current_dir"

    # Check if the pocket is empty
    assert_equals "0" "$(find "$current_dir/.temporal_pocket" -maxdepth 1 -type f | wc -l)" "temporal pocket should be empty"
}

test_invalid_arguments() {
    echo "--- Running test_invalid_arguments ---"
    local current_dir="$TEST_DIR/invalid_args"
    mkdir -p "$current_dir"

    # Test missing arguments for clean
    local output=$("$SCRIPT_PATH" clean "$current_dir" 2>&1 || true)
    assert_contains "$output" "Usage: $SCRIPT_PATH <command> <directory> [options]" "Missing age for clean should show usage"

    # Test invalid age for clean
    output=$("$SCRIPT_PATH" clean "$current_dir" abc 2>&1 || true)
    assert_contains "$output" "Error: Age in days must be a positive integer." "Invalid age for clean should show error"

    # Test missing directory
    output=$("$SCRIPT_PATH" clean /non/existent/dir 10 2>&1 || true)
    assert_contains "$output" "Error: Directory '/non/existent/dir' not found." "Non-existent directory should show error"

    # Test unknown command
    output=$("$SCRIPT_PATH" unknown_command "$current_dir" 2>&1 || true)
    assert_contains "$output" "Error: Unknown command 'unknown_command'." "Unknown command should show error"
}

# --- Main Test Runner ---
main() {
    setup_test_environment

    test_clean_command
    test_list_command
    test_retrieve_command_specific
    test_retrieve_command_all
    test_invalid_arguments

    cleanup_test_environment
    echo "All tests passed!"
}

# Run the main test function
main
