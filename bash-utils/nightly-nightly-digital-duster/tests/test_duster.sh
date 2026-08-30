#!/bin/bash

# Mock rationale:
# The tests create temporary directories and files with specific modification times
# to simulate different scenarios. User input for confirmation is mocked by piping
# 'y' or 'n' into the script's stdin. File system operations are performed in
# isolated temporary directories to ensure determinism and avoid affecting the
# actual system. `find` and `rm` are standard utilities and their behavior is
# predictable.

set -euo pipefail

SCRIPT_PATH="./src/digital_duster.sh"

# Function to create a temporary test environment
setup_test_env() {
    TEST_DIR=$(mktemp -d -t duster-test-XXXXX)
    export TEST_DIR # Make it available to subshells if needed
    cd "$TEST_DIR"
}

# Function to clean up the temporary test environment
cleanup_test_env() {
    if [[ -d "$TEST_DIR" ]]; then
        rm -rf "$TEST_DIR"
    fi
}

# Helper to create a file with a specific age
create_old_file() {
    local filename="$1"
    local days_ago="$2"
    touch -d "$days_ago days ago" "$filename"
}

# Helper to create an old empty directory
create_old_empty_dir() {
    local dirname="$1"
    local days_ago="$2"
    mkdir "$dirname"
    touch -d "$days_ago days ago" "$dirname"
}

# Helper to create an old non-empty directory
create_old_non_empty_dir() {
    local dirname="$1"
    local days_ago="$2"
    mkdir "$dirname"
    touch -d "$days_ago days ago" "$dirname"
    touch "$dirname/inside.txt"
}

# --- Test Cases ---

# Test 1: Help message
test_help_message() {
    setup_test_env
    echo "Running Test 1: Help message"
    output=$("$SCRIPT_PATH" -h)
    if ! echo "$output" | grep -q "Usage: $SCRIPT_PATH"; then
        echo "FAIL: Help message not displayed correctly."
        echo "Output: $output"
        cleanup_test_env
        exit 1
    fi
    echo "PASS: Help message displayed."
    cleanup_test_env
}

# Test 2: No old files found
test_no_old_files() {
    setup_test_env
    echo "Running Test 2: No old files found"
    touch "recent_file.txt"
    mkdir "recent_dir"
    output=$("$SCRIPT_PATH" -a 1) # Look for files older than 1 day
    if ! echo "$output" | grep -q "All clear! No digital dust bunnies found"; then
        echo "FAIL: Expected 'No digital dust bunnies found' message."
        echo "Output: $output"
        cleanup_test_env
        exit 1
    fi
    if [[ ! -f "recent_file.txt" || ! -d "recent_dir" ]]; then
        echo "FAIL: Recent files/dirs were unexpectedly removed."
        cleanup_test_env
        exit 1
    fi
    echo "PASS: Correctly reported no old files and didn't remove recent ones."
    cleanup_test_env
}

# Test 3: Dry run with old files
test_dry_run_with_old_files() {
    setup_test_env
    echo "Running Test 3: Dry run with old files"
    create_old_file "old_file.log" 5
    create_old_empty_dir "old_empty_dir" 5
    create_old_non_empty_dir "old_non_empty_dir" 5 # Should not be listed/removed by default

    output=$("$SCRIPT_PATH" -a 1 --dry-run) # Look for files older than 1 day
    if ! echo "$output" | grep -q "old_file.log"; then
        echo "FAIL: Expected 'old_file.log' in dry run output."
        echo "Output: $output"
        cleanup_test_env
        exit 1
    fi
    if ! echo "$output" | grep -q "old_empty_dir"; then
        echo "FAIL: Expected 'old_empty_dir' in dry run output."
        echo "Output: $output"
        cleanup_test_env
        exit 1
    fi
    if echo "$output" | grep -q "old_non_empty_dir"; then
        echo "FAIL: Did not expect 'old_non_empty_dir' in dry run output."
        echo "Output: $output"
        cleanup_test_env
        exit 1
    fi
    if ! echo "$output" | grep -q "This was a dry run. No files or directories were actually removed."; then
        echo "FAIL: Expected dry run message."
        echo "Output: $output"
        cleanup_test_env
        exit 1
    fi
    if [[ ! -f "old_file.log" || ! -d "old_empty_dir" ]]; then
        echo "FAIL: Files/dirs were removed during dry run."
        cleanup_test_env
        exit 1
    fi
    echo "PASS: Dry run correctly identified old items without removing them."
    cleanup_test_env
}

# Test 4: Delete old files (user confirms)
test_delete_old_files_confirm() {
    setup_test_env
    echo "Running Test 4: Delete old files (user confirms)"
    create_old_file "old_file_to_delete.tmp" 5
    create_old_empty_dir "old_empty_dir_to_delete" 5
    create_old_non_empty_dir "old_non_empty_dir_to_keep" 5

    echo "y" | "$SCRIPT_PATH" -a 1 > /dev/null # Pipe 'y' for confirmation, suppress output for cleaner test log

    if [[ -f "old_file_to_delete.tmp" || -d "old_empty_dir_to_delete" ]]; then
        echo "FAIL: Old files/dirs were not deleted after confirmation."
        cleanup_test_env
        exit 1
    fi
    if [[ ! -d "old_non_empty_dir_to_keep" ]]; then
        echo "FAIL: Non-empty directory was unexpectedly deleted."
        cleanup_test_env
        exit 1
    fi
    echo "PASS: Old files/dirs correctly deleted after confirmation."
    cleanup_test_env
}

# Test 5: Do not delete old files (user cancels)
test_delete_old_files_cancel() {
    setup_test_env
    echo "Running Test 5: Do not delete old files (user cancels)"
    create_old_file "old_file_to_keep.bak" 5
    create_old_empty_dir "old_empty_dir_to_keep" 5

    echo "n" | "$SCRIPT_PATH" -a 1 > /dev/null # Pipe 'n' for cancellation

    if [[ ! -f "old_file_to_keep.bak" || ! -d "old_empty_dir_to_keep" ]]; then
        echo "FAIL: Old files/dirs were deleted despite cancellation."
        cleanup_test_env
        exit 1
    fi
    echo "PASS: Old files/dirs correctly kept after cancellation."
    cleanup_test_env
}

# Test 6: Invalid age argument
test_invalid_age_argument() {
    setup_test_env
    echo "Running Test 6: Invalid age argument"
    output=$("$SCRIPT_PATH" -a abc 2>&1 || true) # Capture stderr, allow failure
    if ! echo "$output" | grep -q "Error: Age must be a positive integer."; then
        echo "FAIL: Did not catch invalid age argument."
        echo "Output: $output"
        cleanup_test_env
        exit 1
    fi
    echo "PASS: Correctly handled invalid age argument."
    cleanup_test_env
}

# Test 7: Non-existent directory
test_non_existent_directory() {
    setup_test_env
    echo "Running Test 7: Non-existent directory"
    output=$("$SCRIPT_PATH" /non/existent/path 2>&1 || true) # Capture stderr, allow failure
    if ! echo "$output" | grep -q "Error: Target directory '/non/existent/path' does not exist."; then
        echo "FAIL: Did not catch non-existent directory."
        echo "Output: $output"
        cleanup_test_env
        exit 1
    fi
    echo "PASS: Correctly handled non-existent directory."
    cleanup_test_env
}

# Test 8: Default age and directory
test_default_age_and_directory() {
    setup_test_env
    echo "Running Test 8: Default age and directory"
    # Create a file older than default 30 days
    create_old_file "default_old_file.log" 31
    # Create a file younger than default 30 days
    touch "default_recent_file.txt"

    output=$("$SCRIPT_PATH" --dry-run) # Use dry-run to check listing
    if ! echo "$output" | grep -q "default_old_file.log"; then
        echo "FAIL: Expected 'default_old_file.log' in default dry run output."
        echo "Output: $output"
        cleanup_test_env
        exit 1
    fi
    if echo "$output" | grep -q "default_recent_file.txt"; then
        echo "FAIL: Did not expect 'default_recent_file.txt' in default dry run output."
        echo "Output: $output"
        cleanup_test_env
        exit 1
    fi
    echo "PASS: Default age and directory handling is correct."
    cleanup_test_env
}

# Test 9: Empty directory not created by script, but existing and old
test_existing_old_empty_dir() {
    setup_test_env
    echo "Running Test 9: Existing old empty directory"
    mkdir "pre_existing_empty_dir"
    touch -d "5 days ago" "pre_existing_empty_dir"

    output=$("$SCRIPT_PATH" -a 1 --dry-run)
    if ! echo "$output" | grep -q "pre_existing_empty_dir"; then
        echo "FAIL: Expected 'pre_existing_empty_dir' in dry run output."
        echo "Output: $output"
        cleanup_test_env
        exit 1
    fi
    echo "PASS: Correctly identified existing old empty directory."
    cleanup_test_env
}


# Run all tests
test_help_message
test_no_old_files
test_dry_run_with_old_files
test_delete_old_files_confirm
test_delete_old_files_cancel
test_invalid_age_argument
test_non_existent_directory
test_default_age_and_directory
test_existing_old_empty_dir

echo ""
echo "All tests passed successfully! ✨"
