#!/bin/bash

# Test suite for Nightly Temporal Dust Bunny Sweeper

# --- Test Setup ---
TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXXXXX)
SCRIPT_PATH="./src/dust_bunny_sweeper.sh"
ARCHIVE_DIR_NAME=".dust_bunnies_archive"

# Mock rationale: For `find` based scripts, creating temporary files and directories
# with specific access/modification times using `touch` is a robust and
# deterministic way to test the script's logic without external dependencies
# or complex mocking frameworks. `touch` is a standard utility.

cleanup() {
    echo "Cleaning up test directory: $TEST_DIR"
    rm -rf "$TEST_DIR"
}

trap cleanup EXIT

# --- Helper Functions ---
create_test_file() {
    local path="$1"
    local access_date="$2" # YYYYMMDDhhmm.SS format
    mkdir -p "$(dirname "$path")"
    touch -a -t "$access_date" "$path"
    echo "Created file: $path (accessed: $access_date)"
}

assert_output_contains() {
    local output="$1"
    local expected="$2"
    if ! echo "$output" | grep -qF "$expected"; then
        echo "FAIL: Expected output to contain '$expected', but got:"
        echo "$output"
        exit 1
    fi
}

assert_output_not_contains() {
    local output="$1"
    local unexpected="$2"
    if echo "$output" | grep -qF "$unexpected"; then
        echo "FAIL: Expected output NOT to contain '$unexpected', but got:"
        echo "$output"
        exit 1
    fi
}

assert_file_exists() {
    local path="$1"
    if [ ! -f "$path" ]; then
        echo "FAIL: Expected file '$path' to exist, but it does not."
        exit 1
    fi
}

assert_file_not_exists() {
    local path="$1"
    if [ -f "$path" ]; then
        echo "FAIL: Expected file '$path' NOT to exist, but it does."
        exit 1
    fi
}

# --- Test Cases ---

# Test 1: No arguments
test_no_arguments() {
    echo "Running Test 1: No arguments"
    output=$("$SCRIPT_PATH" 2>&1)
    assert_output_contains "$output" "Usage: $0 <directory> <age_in_days> [--sweep]"
    echo "Test 1 Passed."
}

# Test 2: Invalid directory
test_invalid_directory() {
    echo "Running Test 2: Invalid directory"
    output=$("$SCRIPT_PATH" "$TEST_DIR/non_existent" 10 2>&1)
    assert_output_contains "$output" "Error: Directory '$TEST_DIR/non_existent' not found."
    echo "Test 2 Passed."
}

# Test 3: Invalid age_in_days
test_invalid_age() {
    echo "Running Test 3: Invalid age_in_days"
    output=$("$SCRIPT_PATH" "$TEST_DIR" "abc" 2>&1)
    assert_output_contains "$output" "Error: Age in days must be a non-negative integer."
    output=$("$SCRIPT_PATH" "$TEST_DIR" "-5" 2>&1)
    assert_output_contains "$output" "Error: Age in days must be a non-negative integer."
    echo "Test 3 Passed."
}

# Test 4: No dust bunnies found
test_no_dust_bunnies() {
    echo "Running Test 4: No dust bunnies found"
    local current_time=$(date +%Y%m%d%H%M.%S)
    create_test_file "$TEST_DIR/recent_file.txt" "$current_time"
    output=$("$SCRIPT_PATH" "$TEST_DIR" 1 2>&1) # Look for files older than 1 day
    assert_output_contains "$output" "No temporal dust bunnies found. Your digital space is sparkling clean!"
    assert_output_not_contains "$output" "recent_file.txt"
    echo "Test 4 Passed."
}

# Test 5: Dust bunnies found (dry run)
test_dust_bunnies_dry_run() {
    echo "Running Test 5: Dust bunnies found (dry run)"
    local current_time=$(date +%Y%m%d%H%M.%S)
    local old_time=$(date -d "2 days ago" +%Y%m%d%H%M.%S)

    create_test_file "$TEST_DIR/recent/file1.txt" "$current_time"
    create_test_file "$TEST_DIR/old/file2.log" "$old_time"
    create_test_file "$TEST_DIR/another_old_file.dat" "$old_time"

    output=$("$SCRIPT_PATH" "$TEST_DIR" 1 2>&1) # Look for files older than 1 day
    assert_output_contains "$output" "Found the following temporal dust bunnies"
    assert_output_contains "$output" "$TEST_DIR/old/file2.log"
    assert_output_contains "$output" "$TEST_DIR/another_old_file.dat"
    assert_output_not_contains "$output" "$TEST_DIR/recent/file1.txt"

    assert_file_exists "$TEST_DIR/recent/file1.txt"
    assert_file_exists "$TEST_DIR/old/file2.log"
    assert_file_exists "$TEST_DIR/another_old_file.dat"
    echo "Test 5 Passed."
}

# Test 6: Dust bunnies found (sweep mode)
test_dust_bunnies_sweep_mode() {
    echo "Running Test 6: Dust bunnies found (sweep mode)"
    local current_time=$(date +%Y%m%d%H%M.%S)
    local old_time=$(date -d "2 days ago" +%Y%m%d%H%M.%S)

    local sweep_test_dir="$TEST_DIR/sweep_test"
    mkdir -p "$sweep_test_dir"

    create_test_file "$sweep_test_dir/recent_sweep_file.txt" "$current_time"
    create_test_file "$sweep_test_dir/old_sweep_file1.log" "$old_time"
    create_test_file "$sweep_test_dir/old_sweep_file2.dat" "$old_time"

    output=$("$SCRIPT_PATH" "$sweep_test_dir" 1 --sweep 2>&1) # Look for files older than 1 day

    assert_output_contains "$output" "Sweep mode activated. Moving identified files to '$sweep_test_dir/$ARCHIVE_DIR_NAME/'"
    assert_output_contains "$output" "Moved the following files to '$sweep_test_dir/$ARCHIVE_DIR_NAME/':"
    assert_output_contains "$output" "$sweep_test_dir/old_sweep_file1.log"
    assert_output_contains "$output" "$sweep_test_dir/old_sweep_file2.dat"
    assert_output_not_contains "$output" "$sweep_test_dir/recent_sweep_file.txt"

    assert_file_exists "$sweep_test_dir/recent_sweep_file.txt"
    assert_file_not_exists "$sweep_test_dir/old_sweep_file1.log"
    assert_file_not_exists "$sweep_test_dir/old_sweep_file2.dat"

    assert_file_exists "$sweep_test_dir/$ARCHIVE_DIR_NAME/old_sweep_file1.log"
    assert_file_exists "$sweep_test_dir/$ARCHIVE_DIR_NAME/old_sweep_file2.dat"
    echo "Test 6 Passed."
}

# Test 7: Files with spaces in names (dry run)
test_files_with_spaces_dry_run() {
    echo "Running Test 7: Files with spaces in names (dry run)"
    local current_time=$(date +%Y%m%d%H%M.%S)
    local old_time=$(date -d "2 days ago" +%Y%m%d%H%M.%S)

    local space_test_dir="$TEST_DIR/space test dir"
    mkdir -p "$space_test_dir"

    create_test_file "$space_test_dir/file with spaces 1.txt" "$old_time"
    create_test_file "$space_test_dir/another file.log" "$current_time"

    output=$("$SCRIPT_PATH" "$space_test_dir" 1 2>&1)

    assert_output_contains "$output" "Found the following temporal dust bunnies"
    assert_output_contains "$output" "$space_test_dir/file with spaces 1.txt"
    assert_output_not_contains "$output" "$space_test_dir/another file.log"

    assert_file_exists "$space_test_dir/file with spaces 1.txt"
    assert_file_exists "$space_test_dir/another file.log"
    echo "Test 7 Passed."
}

# Test 8: Files with spaces in names (sweep mode)
test_files_with_spaces_sweep_mode() {
    echo "Running Test 8: Files with spaces in names (sweep mode)"
    local current_time=$(date +%Y%m%d%H%M.%S)
    local old_time=$(date -d "2 days ago" +%Y%m%d%H%M.%S)

    local space_sweep_test_dir="$TEST_DIR/space sweep test dir"
    mkdir -p "$space_sweep_test_dir"

    create_test_file "$space_sweep_test_dir/file with spaces 1.txt" "$old_time"
    create_test_file "$space_sweep_test_dir/another file.log" "$current_time"

    output=$("$SCRIPT_PATH" "$space_sweep_test_dir" 1 --sweep 2>&1)

    assert_output_contains "$output" "Moved the following files to '$space_sweep_test_dir/$ARCHIVE_DIR_NAME/':"
    assert_output_contains "$output" "$space_sweep_test_dir/file with spaces 1.txt"
    assert_output_not_contains "$output" "$space_sweep_test_dir/another file.log"

    assert_file_exists "$space_sweep_test_dir/another file.log"
    assert_file_not_exists "$space_sweep_test_dir/file with spaces 1.txt"
    assert_file_exists "$space_sweep_test_dir/$ARCHIVE_DIR_NAME/file with spaces 1.txt"
    echo "Test 8 Passed."
}

# --- Run all tests ---
echo "--- Starting all tests ---"
test_no_arguments
test_invalid_directory
test_invalid_age
test_no_dust_bunnies
test_dust_bunnies_dry_run
test_dust_bunnies_sweep_mode
test_files_with_spaces_dry_run
test_files_with_spaces_sweep_mode
echo "--- All tests completed successfully! ---"
