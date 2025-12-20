#!/bin/bash

# Nightly Scavenger's Stash Sorter Tests

# --- Test Setup ---
TEST_DIR="/tmp/scavenger_stash_test_$(date +%s%N)"
SCRIPT_PATH="./src/sort_stash.sh"

# Function to set up a test environment
setup_test_env() {
    mkdir -p "$TEST_DIR"
    echo "Setting up test environment in $TEST_DIR"
}

# Function to clean up test environment
cleanup_test_env() {
    if [ -d "$TEST_DIR" ]; then
        rm -rf "$TEST_DIR"
        echo "Cleaned up $TEST_DIR"
    fi
}

# --- Helper Functions for Assertions ---
assert_file_exists() {
    local file_path="$1"
    local test_name="$2"
    if [ ! -f "$file_path" ]; then
        echo "FAIL: $test_name - File '$file_path' does not exist."
        exit 1
    fi
}

assert_file_not_exists() {
    local file_path="$1"
    local test_name="$2"
    if [ -f "$file_path" ]; then
        echo "FAIL: $test_name - File '$file_path' unexpectedly exists."
        exit 1
    fi
}

assert_dir_exists() {
    local dir_path="$1"
    local test_name="$2"
    if [ ! -d "$dir_path" ]; then
        echo "FAIL: $test_name - Directory '$dir_path' does not exist."
        exit 1
    fi
}

assert_output_contains() {
    local output="$1"
    local expected_string="$2"
    local test_name="$3"
    if ! echo "$output" | grep -q "$expected_string"; then
        echo "FAIL: $test_name - Output did not contain '$expected_string'."
        echo "Output: $output"
        exit 1
    fi
}

# --- Test Cases ---

# Test 1: No arguments - should print usage and exit with error
test_no_arguments() {
    echo "Running Test 1: No arguments"
    cleanup_test_env # Ensure clean slate
    output=$("$SCRIPT_PATH" 2>&1)
    if [ "$?" -eq 0 ]; then
        echo "FAIL: Test 1 - Script exited with success (0) but expected error."
        exit 1
    fi
    assert_output_contains "$output" "Usage: $0 <directory_path>" "Test 1"
    echo "PASS: Test 1"
}

# Test 2: Invalid directory - should print error and exit with error
test_invalid_directory() {
    echo "Running Test 2: Invalid directory"
    cleanup_test_env
    output=$("$SCRIPT_PATH" "/non/existent/path_$(date +%s%N)" 2>&1)
    if [ "$?" -eq 0 ]; then
        echo "FAIL: Test 2 - Script exited with success (0) but expected error."
        exit 1
    fi
    assert_output_contains "$output" "Error: Stash directory" "Test 2"
    assert_output_contains "$output" "not found or is not a directory." "Test 2"
    echo "PASS: Test 2"
}

# Test 3: Empty directory - should do nothing and report no provisions
test_empty_directory() {
    echo "Running Test 3: Empty directory"
    setup_test_env
    output=$("$SCRIPT_PATH" "$TEST_DIR" 2>&1)
    if [ "$?" -ne 0 ]; then
        echo "FAIL: Test 3 - Script exited with error ($?) but expected success."
        exit 1
    fi
    assert_dir_exists "$TEST_DIR/Documents" "Test 3"
    assert_dir_exists "$TEST_DIR/Images" "Test 3"
    assert_dir_exists "$TEST_DIR/Archives" "Test 3"
    assert_dir_exists "$TEST_DIR/Executables" "Test 3"
    assert_dir_exists "$TEST_DIR/Other" "Test 3"
    assert_output_contains "$output" "No new provisions found in '$TEST_DIR'." "Test 3"
    cleanup_test_env
    echo "PASS: Test 3"
}

# Test 4: Directory with mixed files - should sort correctly
test_mixed_files() {
    echo "Running Test 4: Mixed files"
    setup_test_env
    touch "$TEST_DIR/report.txt"
    touch "$TEST_DIR/photo.jpeg"
    touch "$TEST_DIR/archive.zip"
    touch "$TEST_DIR/script.sh"
    touch "$TEST_DIR/unknown.xyz"
    touch "$TEST_DIR/another_doc.pdf"

    output=$("$SCRIPT_PATH" "$TEST_DIR" 2>&1)
    if [ "$?" -ne 0 ]; then
        echo "FAIL: Test 4 - Script exited with error ($?) but expected success."
        exit 1
    fi

    assert_file_exists "$TEST_DIR/Documents/report.txt" "Test 4"
    assert_file_exists "$TEST_DIR/Documents/another_doc.pdf" "Test 4"
    assert_file_exists "$TEST_DIR/Images/photo.jpeg" "Test 4"
    assert_file_exists "$TEST_DIR/Archives/archive.zip" "Test 4"
    assert_file_exists "$TEST_DIR/Executables/script.sh" "Test 4"
    assert_file_exists "$TEST_DIR/Other/unknown.xyz" "Test 4"

    assert_file_not_exists "$TEST_DIR/report.txt" "Test 4"
    assert_file_not_exists "$TEST_DIR/photo.jpeg" "Test 4"
    assert_file_not_exists "$TEST_DIR/archive.zip" "Test 4"
    assert_file_not_exists "$TEST_DIR/script.sh" "Test 4"
    assert_file_not_exists "$TEST_DIR/unknown.xyz" "Test 4"
    assert_file_not_exists "$TEST_DIR/another_doc.pdf" "Test 4"

    assert_output_contains "$output" "Stash sorted! Your inventory is now more manageable, survivor. (6 items moved)" "Test 4"
    cleanup_test_env
    echo "PASS: Test 4"
}

# Test 5: Files already in target subdirectories - should skip them
test_already_sorted_files() {
    echo "Running Test 5: Already sorted files"
    setup_test_env
    mkdir -p "$TEST_DIR/Documents"
    mkdir -p "$TEST_DIR/Images"
    touch "$TEST_DIR/Documents/pre_sorted_doc.txt"
    touch "$TEST_DIR/Images/pre_sorted_img.png"
    touch "$TEST_DIR/new_doc.md" # A new file to be sorted

    output=$("$SCRIPT_PATH" "$TEST_DIR" 2>&1)
    if [ "$?" -ne 0 ]; then
        echo "FAIL: Test 5 - Script exited with error ($?) but expected success."
        exit 1
    fi

    assert_file_exists "$TEST_DIR/Documents/pre_sorted_doc.txt" "Test 5"
    assert_file_exists "$TEST_DIR/Images/pre_sorted_img.png" "Test 5"
    assert_file_exists "$TEST_DIR/Documents/new_doc.md" "Test 5"
    assert_file_not_exists "$TEST_DIR/new_doc.md" "Test 5"

    assert_output_contains "$output" "already secured in 'Documents'. Skipping." "Test 5"
    assert_output_contains "$output" "already secured in 'Images'. Skipping." "Test 5"
    assert_output_contains "$output" "Stash sorted! Your inventory is now more manageable, survivor. (1 items moved)" "Test 5"
    cleanup_test_env
    echo "PASS: Test 5"
}

# Test 6: Directory with only one type of file
test_single_type_files() {
    echo "Running Test 6: Single type files"
    setup_test_env
    touch "$TEST_DIR/note1.txt"
    touch "$TEST_DIR/note2.txt"
    touch "$TEST_DIR/note3.txt"

    output=$("$SCRIPT_PATH" "$TEST_DIR" 2>&1)
    if [ "$?" -ne 0 ]; then
        echo "FAIL: Test 6 - Script exited with error ($?) but expected success."
        exit 1
    fi

    assert_file_exists "$TEST_DIR/Documents/note1.txt" "Test 6"
    assert_file_exists "$TEST_DIR/Documents/note2.txt" "Test 6"
    assert_file_exists "$TEST_DIR/Documents/note3.txt" "Test 6"
    assert_file_not_exists "$TEST_DIR/note1.txt" "Test 6"

    assert_output_contains "$output" "Stash sorted! Your inventory is now more manageable, survivor. (3 items moved)" "Test 6"
    cleanup_test_env
    echo "PASS: Test 6"
}

# Test 7: Directory with only 'Other' type files
test_only_other_files() {
    echo "Running Test 7: Only 'Other' files"
    setup_test_env
    touch "$TEST_DIR/data.db"
    touch "$TEST_DIR/config.ini"

    output=$("$SCRIPT_PATH" "$TEST_DIR" 2>&1)
    if [ "$?" -ne 0 ]; then
        echo "FAIL: Test 7 - Script exited with error ($?) but expected success."
        exit 1
    fi

    assert_file_exists "$TEST_DIR/Other/data.db" "Test 7"
    assert_file_exists "$TEST_DIR/Other/config.ini" "Test 7"
    assert_file_not_exists "$TEST_DIR/data.db" "Test 7"

    assert_output_contains "$output" "Stash sorted! Your inventory is now more manageable, survivor. (2 items moved)" "Test 7"
    cleanup_test_env
    echo "PASS: Test 7"
}

# Test 8: No files to sort, but categories exist
test_no_files_to_sort_categories_exist() {
    echo "Running Test 8: No files to sort, but categories exist"
    setup_test_env
    mkdir -p "$TEST_DIR/Documents"
    mkdir -p "$TEST_DIR/Images"
    touch "$TEST_DIR/Documents/already_here.txt"

    output=$("$SCRIPT_PATH" "$TEST_DIR" 2>&1)
    if [ "$?" -ne 0 ]; then
        echo "FAIL: Test 8 - Script exited with error ($?) but expected success."
        exit 1
    fi

    assert_file_exists "$TEST_DIR/Documents/already_here.txt" "Test 8"
    assert_output_contains "$output" "All provisions in '$TEST_DIR' were already sorted. Good work, survivor!" "Test 8"
    cleanup_test_env
    echo "PASS: Test 8"
}

# Mock rationale:
# The tests create temporary directories and files, operating on a completely isolated filesystem.
# This ensures determinism and prevents side effects on the actual system.
# The 'touch', 'mkdir', 'mv', and 'rm' commands operate within this isolated environment,
# effectively "mocking" real-world file system interactions by providing a controlled,
# reproducible state for each test. The `realpath` command is used to ensure consistent
# path resolution within the test environment.

# --- Run all tests ---
echo "--- Running all Nightly Scavenger's Stash Sorter tests ---"
test_no_arguments
test_invalid_directory
test_empty_directory
test_mixed_files
test_already_sorted_files
test_single_type_files
test_only_other_files
test_no_files_to_sort_categories_exist
echo "--- All tests passed! ---"

cleanup_test_env # Final cleanup in case of early exit or manual run
