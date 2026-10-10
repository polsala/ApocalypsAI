#!/bin/bash

# Test suite for Nightly Digital Dust Sweeper

SCRIPT_PATH="./src/dust_sweeper.sh"
TEST_DIR="test_temp_dust_sweeper"

# --- Setup and Teardown ---
setup() {
    mkdir -p "$TEST_DIR"
    # Create some files with different ages
    # Mock rationale: Using 'date -d' is a common GNU date extension for setting relative times.
    # This ensures deterministic file ages for testing purposes across common Linux environments.
    touch -t $(date -d "8 days ago" +%Y%m%d%H%M) "$TEST_DIR/old_file_8d.txt" # 8 days old
    touch -t $(date -d "10 days ago" +%Y%m%d%H%M) "$TEST_DIR/old_file_10d.log" # 10 days old
    touch -t $(date -d "6 days ago" +%Y%m%d%H%M) "$TEST_DIR/new_file_6d.txt" # 6 days old (too new for MIN_AGE_DAYS=7)
    touch -t $(date -d "1 day ago" +%Y%m%d%H%M) "$TEST_DIR/very_new_file_1d.tmp" # 1 day old
    touch "$TEST_DIR/current_file.txt" # Current timestamp

    # File with spaces
    touch -t $(date -d "9 days ago" +%Y%m%d%H%M) "$TEST_DIR/old file with spaces.txt" # 9 days old

    # Directory (should not be deleted)
    mkdir "$TEST_DIR/old_dir_8d"
    touch -t $(date -d "8 days ago" +%Y%m%d%H%M) "$TEST_DIR/old_dir_8d/inside.txt"
}

teardown() {
    rm -rf "$TEST_DIR"
}

# --- Test Helpers ---
assert_contains() {
    local expected="$1"
    local actual="$2"
    if ! echo "$actual" | grep -qF "$expected"; then
        echo "FAIL: Expected output to contain '$expected', but got:"
        echo "$actual"
        exit 1
    fi
}

assert_not_contains() {
    local unexpected="$1"
    local actual="$2"
    if echo "$actual" | grep -qF "$unexpected"; then
        echo "FAIL: Expected output NOT to contain '$unexpected', but got:"
        echo "$actual"
        exit 1
    fi
}

assert_file_exists() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        echo "FAIL: Expected file '$file' to exist, but it does not."
        exit 1
    }
}

assert_file_not_exists() {
    local file="$1"
    if [[ -f "$file" ]]; then
        echo "FAIL: Expected file '$file' NOT to exist, but it does."
        exit 1
    }
}

# --- Tests ---

# Test 1: Dry run - list files older than 7 days
test_dry_run_7_days() {
    echo "Running test_dry_run_7_days..."
    local output=$(bash "$SCRIPT_PATH" "$TEST_DIR" 7)
    assert_contains "Mode: DRY RUN" "$output"
    assert_contains "$TEST_DIR/old_file_8d.txt" "$output"
    assert_contains "$TEST_DIR/old_file_10d.log" "$output"
    assert_contains "$TEST_DIR/old file with spaces.txt" "$output"
    assert_not_contains "$TEST_DIR/new_file_6d.txt" "$output"
    assert_not_contains "$TEST_DIR/very_new_file_1d.tmp" "$output"
    assert_not_contains "$TEST_DIR/current_file.txt" "$output"
    assert_file_exists "$TEST_DIR/old_file_8d.txt" # Should still exist after dry run
    echo "PASS: test_dry_run_7_days"
}

# Test 2: Live sweep - delete files older than 7 days
test_live_sweep_7_days() {
    echo "Running test_live_sweep_7_days..."
    local output=$(bash "$SCRIPT_PATH" --sweep "$TEST_DIR" 7)
    assert_contains "Mode: LIVE SWEEP" "$output"
    assert_contains "removed '$TEST_DIR/old_file_8d.txt'" "$output"
    assert_contains "removed '$TEST_DIR/old_file_10d.log'" "$output"
    assert_contains "removed '$TEST_DIR/old file with spaces.txt'" "$output"
    assert_file_not_exists "$TEST_DIR/old_file_8d.txt"
    assert_file_not_exists "$TEST_DIR/old_file_10d.log"
    assert_file_not_exists "$TEST_DIR/old file with spaces.txt"
    assert_file_exists "$TEST_DIR/new_file_6d.txt" # Should not be deleted
    assert_file_exists "$TEST_DIR/very_new_file_1d.tmp" # Should not be deleted
    assert_file_exists "$TEST_DIR/current_file.txt" # Should not be deleted
    assert_file_exists "$TEST_DIR/old_dir_8d" # Directory should not be deleted
    echo "PASS: test_live_sweep_7_days"
}

# Test 3: Invalid age (less than MIN_AGE_DAYS)
test_invalid_age_too_low() {
    echo "Running test_invalid_age_too_low..."
    local output=$(bash "$SCRIPT_PATH" "$TEST_DIR" 6 2>&1)
    assert_contains "Error: <age_in_days> must be at least 7." "$output"
    echo "PASS: test_invalid_age_too_low"
}

# Test 4: Invalid age (not a number)
test_invalid_age_not_number() {
    echo "Running test_invalid_age_not_number..."
    local output=$(bash "$SCRIPT_PATH" "$TEST_DIR" "abc" 2>&1)
    assert_contains "Error: <age_in_days> must be a positive integer." "$output"
    echo "PASS: test_invalid_age_not_number"
}

# Test 5: Non-existent directory
test_non_existent_directory() {
    echo "Running test_non_existent_directory..."
    local output=$(bash "$SCRIPT_PATH" "non_existent_dir" 7 2>&1)
    assert_contains "Error: Directory 'non_existent_dir' does not exist or is not a directory." "$output"
    echo "PASS: test_non_existent_directory"
}

# Test 6: Critical directory check (e.g., /)
test_critical_directory_root() {
    echo "Running test_critical_directory_root..."
    local output=$(bash "$SCRIPT_PATH" "/" 7 2>&1)
    assert_contains "Error: Cleaning critical system directory '/' is not allowed for safety reasons." "$output"
    echo "PASS: test_critical_directory_root"
}

# Test 7: Critical directory check (e.g., /etc)
test_critical_directory_etc() {
    echo "Running test_critical_directory_etc..."
    local output=$(bash "$SCRIPT_PATH" "/etc" 7 2>&1)
    assert_contains "Error: Cleaning critical system directory '/etc' is not allowed for safety reasons." "$output"
    echo "PASS: test_critical_directory_etc"
}

# Test 8: Help message
test_help_message() {
    echo "Running test_help_message..."
    local output=$(bash "$SCRIPT_PATH" --help)
    assert_contains "Usage: $0 [OPTIONS] <directory> <age_in_days>" "$output"
    assert_contains "Nightly Digital Dust Sweeper" "$output"
    echo "PASS: test_help_message"
}

# Test 9: No arguments
test_no_arguments() {
    echo "Running test_no_arguments..."
    local output=$(bash "$SCRIPT_PATH" 2>&1)
    assert_contains "Error: Missing <directory> or <age_in_days> argument." "$output"
    echo "PASS: test_no_arguments"
}

# Test 10: Too many arguments
test_too_many_arguments() {
    echo "Running test_too_many_arguments..."
    local output=$(bash "$SCRIPT_PATH" "$TEST_DIR" 7 extra_arg 2>&1)
    assert_contains "Error: Too many arguments." "$output"
    echo "PASS: test_too_many_arguments"
}

# Test 11: Dry run - no files to delete
test_dry_run_no_files() {
    echo "Running test_dry_run_no_files..."
    # Create a fresh test directory with only new files
    teardown
    mkdir -p "$TEST_DIR"
    touch "$TEST_DIR/new_file_1.txt"
    touch "$TEST_DIR/new_file_2.txt"
    local output=$(bash "$SCRIPT_PATH" "$TEST_DIR" 7)
    assert_contains "Mode: DRY RUN" "$output"
    assert_not_contains "$TEST_DIR/new_file_1.txt" "$output"
    assert_not_contains "$TEST_DIR/new_file_2.txt" "$output"
    assert_contains "--- Dry run complete. No files were deleted. ---" "$output"
    echo "PASS: test_dry_run_no_files"
}

# Test 12: Live sweep - no files to delete
test_live_sweep_no_files() {
    echo "Running test_live_sweep_no_files..."
    # Create a fresh test directory with only new files
    teardown
    mkdir -p "$TEST_DIR"
    touch "$TEST_DIR/new_file_1.txt"
    touch "$TEST_DIR/new_file_2.txt"
    local output=$(bash "$SCRIPT_PATH" --sweep "$TEST_DIR" 7)
    assert_contains "Mode: LIVE SWEEP" "$output"
    assert_not_contains "removed" "$output" # No files should be removed
    assert_contains "--- Live sweep complete. Digital dust has been swept! ---" "$output"
    assert_file_exists "$TEST_DIR/new_file_1.txt"
    assert_file_exists "$TEST_DIR/new_file_2.txt"
    echo "PASS: test_live_sweep_no_files"
}


# --- Run all tests ---
run_test() {
    local test_func="$1"
    setup
    "$test_func"
    teardown
}

# Ensure the script is executable for tests
chmod +x "$SCRIPT_PATH"

run_test test_dry_run_7_days
run_test test_live_sweep_7_days
run_test test_invalid_age_too_low
run_test test_invalid_age_not_number
run_test test_non_existent_directory
run_test test_critical_directory_root
run_test test_critical_directory_etc
run_test test_help_message
run_test test_no_arguments
run_test test_too_many_arguments
run_test test_dry_run_no_files
run_test test_live_sweep_no_files

echo "All tests passed!"
