#!/bin/bash

# Test suite for Nightly Digital Dust Bunny Sweeper

set -euo pipefail

SCRIPT_PATH="./src/dust_bunny_sweeper.sh"
TEST_DIR=""

# Helper function for assertions
assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$expected" == "$actual" ]]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message"
        echo "  Expected: '$expected'"
        echo "  Actual:   '$actual'"
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
        echo "FAIL: $message"
        echo "  Expected to contain: '$needle'"
        echo "  Actual output: '$haystack'"
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
        echo "FAIL: $message"
        echo "  Expected NOT to contain: '$needle'"
        echo "  Actual output: '$haystack'"
        exit 1
    fi
}

assert_file_exists() {
    local file="$1"
    local message="$2"
    if [[ -f "$file" ]]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message"
        echo "  File '$file' does not exist."
        exit 1
    fi
}

assert_file_not_exists() {
    local file="$1"
    local message="$2"
    if [[ ! -f "$file" ]]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message"
        echo "  File '$file' unexpectedly exists."
        exit 1
    fi
}

# Setup function
setup() {
    TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXXX)
    chmod +x "$SCRIPT_PATH"
    echo "Setup: Created test directory $TEST_DIR"
}

# Teardown function
teardown() {
    if [[ -d "$TEST_DIR" ]]; then
        rm -rf "$TEST_DIR"
        echo "Teardown: Removed test directory $TEST_DIR"
    fi
}

# Test cases

# Test 1: Help message
test_help_message() {
    echo "Running Test 1: Help message"
    local output
    output=$("$SCRIPT_PATH" -h)
    assert_contains "$output" "Usage: dust_bunny_sweeper.sh [OPTIONS] <DIRECTORY1>" "Help message should contain usage info"
    assert_contains "$output" "Options:" "Help message should list options"
    assert_contains "$output" "Safety Notice:" "Help message should include safety notice"
}

# Test 2: No directories specified
test_no_directories() {
    echo "Running Test 2: No directories specified"
    local output
    if output=$("$SCRIPT_PATH" 2>&1); then
        echo "FAIL: Script should exit with error when no directories are specified."
        exit 1
    else
        assert_contains "$output" "Error: No directories specified for sweeping." "Error message for no directories"
    fi
}

# Test 3: Dry run - no files should be deleted
test_dry_run_no_deletion() {
    echo "Running Test 3: Dry run - no files should be deleted"
    local dir="$TEST_DIR/dry_run_test"
    mkdir -p "$dir"

    # Create an old file (3 days old)
    touch -t "$(date +%Y%m%d%H%M.%S --date='3 days ago')" "$dir/old_file.txt" # Mock rationale: Using 'date --date' and 'touch -t' to set specific modification times for files allows deterministic testing of age-based filtering.
    # Create a new file (current time)
    touch "$dir/new_file.txt"

    local output
    output=$("$SCRIPT_PATH" -a 2 -d "$dir") # Age 2 means files older than 2 days (i.e., 3 days old)
    
    assert_contains "$output" "Mode: DRY RUN (NO DELETIONS)" "Output should indicate dry run mode"
    assert_contains "$output" "Found the following digital dust bunnies in '$dir' (DRY RUN - no files deleted):" "Output should list files found"
    assert_contains "$output" "- $dir/old_file.txt" "Old file should be listed in dry run"
    assert_not_contains "$output" "- $dir/new_file.txt" "New file should not be listed in dry run"
    assert_file_exists "$dir/old_file.txt" "Old file should still exist after dry run"
    assert_file_exists "$dir/new_file.txt" "New file should still exist after dry run"
}

# Test 4: Sweep - old files should be deleted
test_sweep_deletion() {
    echo "Running Test 4: Sweep - old files should be deleted"
    local dir="$TEST_DIR/sweep_test"
    mkdir -p "$dir"

    # Create an old file (3 days old)
    touch -t "$(date +%Y%m%d%H%M.%S --date='3 days ago')" "$dir/old_file_to_delete.txt" # Mock rationale: Using 'date --date' and 'touch -t' to set specific modification times for files allows deterministic testing of age-based filtering.
    # Create a new file (current time)
    touch "$dir/new_file_to_keep.txt"
    # Create another old file with spaces in name
    touch -t "$(date +%Y%m%d%H%M.%S --date='4 days ago')" "$dir/old file with spaces.log"

    local output
    output=$("$SCRIPT_PATH" -a 2 -s "$dir") # Age 2 means files older than 2 days (i.e., 3 and 4 days old)

    assert_contains "$output" "Mode: SWEEP (DELETING FILES)" "Output should indicate sweep mode"
    assert_contains "$output" "Sweeping away the following dust bunnies from '$dir':" "Output should indicate sweeping"
    assert_contains "$output" "removing '$dir/old_file_to_delete.txt'" "Old file deletion should be logged"
    assert_contains "$output" "removing '$dir/old file with spaces.log'" "Old file with spaces deletion should be logged"
    assert_file_not_exists "$dir/old_file_to_delete.txt" "Old file should be deleted after sweep"
    assert_file_not_exists "$dir/old file with spaces.log" "Old file with spaces should be deleted after sweep"
    assert_file_exists "$dir/new_file_to_keep.txt" "New file should still exist after sweep"
}

# Test 5: Environment variable for age
test_env_var_age() {
    echo "Running Test 5: Environment variable for age"
    local dir="$TEST_DIR/env_age_test"
    mkdir -p "$dir"

    touch -t "$(date +%Y%m%d%H%M.%S --date='5 days ago')" "$dir/very_old.log"
    touch -t "$(date +%Y%m%d%H%M.%S --date='3 days ago')" "$dir/moderately_old.log"
    touch "$dir/new.log"

    local output
    DUST_BUNNY_AGE_DAYS=4 output=$("$SCRIPT_PATH" -d "$dir") # Should find 'very_old.log'
    assert_contains "$output" "- $dir/very_old.log" "Very old file should be listed with ENV AGE_DAYS=4"
    assert_not_contains "$output" "- $dir/moderately_old.log" "Moderately old file should not be listed with ENV AGE_DAYS=4"

    DUST_BUNNY_AGE_DAYS=2 output=$("$SCRIPT_PATH" -d "$dir") # Should find both old files
    assert_contains "$output" "- $dir/very_old.log" "Very old file should be listed with ENV AGE_DAYS=2"
    assert_contains "$output" "- $dir/moderately_old.log" "Moderately old file should be listed with ENV AGE_DAYS=2"
}

# Test 6: Command-line age overrides environment variable
test_cli_age_override_env() {
    echo "Running Test 6: Command-line age overrides environment variable"
    local dir="$TEST_DIR/cli_age_override_env_test"
    mkdir -p "$dir"

    touch -t "$(date +%Y%m%d%H%M.%S --date='5 days ago')" "$dir/very_old.log"
    touch -t "$(date +%Y%m%d%H%M.%S --date='3 days ago')" "$dir/moderately_old.log"
    touch "$dir/new.log"

    local output
    DUST_BUNNY_AGE_DAYS=4 output=$("$SCRIPT_PATH" -a 2 -d "$dir") # CLI -a 2 should override ENV DUST_BUNNY_AGE_DAYS=4
    assert_contains "$output" "- $dir/very_old.log" "Very old file should be listed with CLI AGE_DAYS=2"
    assert_contains "$output" "- $dir/moderately_old.log" "Moderately old file should be listed with CLI AGE_DAYS=2"
    assert_not_contains "$output" "- $dir/new.log" "New file should not be listed"
}

# Test 7: Non-existent directory
test_non_existent_directory() {
    echo "Running Test 7: Non-existent directory"
    local output
    output=$("$SCRIPT_PATH" -d "$TEST_DIR/non_existent_dir" 2>&1)
    assert_contains "$output" "Warning: Directory '$TEST_DIR/non_existent_dir' does not exist or is not a directory. Skipping." "Warning for non-existent directory"
    assert_contains "$output" "No dust bunnies found" "Should report no dust bunnies if dir doesn't exist"
}

# Test 8: Multiple directories
test_multiple_directories() {
    echo "Running Test 8: Multiple directories"
    local dir1="$TEST_DIR/multi_dir1"
    local dir2="$TEST_DIR/multi_dir2"
    mkdir -p "$dir1" "$dir2"

    touch -t "$(date +%Y%m%d%H%M.%S --date='3 days ago')" "$dir1/old_file1.txt"
    touch "$dir1/new_file1.txt"
    touch -t "$(date +%Y%m%d%H%M.%S --date='3 days ago')" "$dir2/old_file2.txt"
    touch "$dir2/new_file2.txt"

    local output
    output=$("$SCRIPT_PATH" -a 2 -d "$dir1" "$dir2")

    assert_contains "$output" "Scanning '$dir1'" "Should scan first directory"
    assert_contains "$output" "- $dir1/old_file1.txt" "Old file in dir1 should be listed"
    assert_not_contains "$output" "- $dir1/new_file1.txt" "New file in dir1 should not be listed"

    assert_contains "$output" "Scanning '$dir2'" "Should scan second directory"
    assert_contains "$output" "- $dir2/old_file2.txt" "Old file in dir2 should be listed"
    assert_not_contains "$output" "- $dir2/new_file2.txt" "New file in dir2 should not be listed"
}

# Test 9: Default dry run behavior
test_default_dry_run() {
    echo "Running Test 9: Default dry run behavior"
    local dir="$TEST_DIR/default_dry_run_test"
    mkdir -p "$dir"

    touch -t "$(date +%Y%m%d%H%M.%S --date='8 days ago')" "$dir/default_old_file.txt" # Older than default 7 days
    touch "$dir/default_new_file.txt"

    local output
    output=$("$SCRIPT_PATH" "$dir") # No -d or -s, should be dry run with default age 7

    assert_contains "$output" "Mode: DRY RUN (NO DELETIONS)" "Default should be dry run"
    assert_contains "$output" "Age threshold: 7 days" "Default age should be 7 days"
    assert_contains "$output" "- $dir/default_old_file.txt" "Old file should be listed in default dry run"
    assert_file_exists "$dir/default_old_file.txt" "Old file should still exist after default dry run"
}

# Test 10: Environment variable DUST_BUNNY_SWEEP=true
test_env_var_sweep() {
    echo "Running Test 10: Environment variable DUST_BUNNY_SWEEP=true"
    local dir="$TEST_DIR/env_sweep_test"
    mkdir -p "$dir"

    touch -t "$(date +%Y%m%d%H%M.%S --date='8 days ago')" "$dir/env_old_file.txt"
    touch "$dir/env_new_file.txt"

    local output
    DUST_BUNNY_SWEEP=true output=$("$SCRIPT_PATH" -a 7 "$dir") # Should sweep with ENV DUST_BUNNY_SWEEP=true

    assert_contains "$output" "Mode: SWEEP (DELETING FILES)" "Output should indicate sweep mode from ENV"
    assert_contains "$output" "removing '$dir/env_old_file.txt'" "Old file deletion should be logged"
    assert_file_not_exists "$dir/env_old_file.txt" "Old file should be deleted by ENV sweep"
    assert_file_exists "$dir/env_new_file.txt" "New file should still exist"
}

# Test 11: Command-line -d overrides DUST_BUNNY_SWEEP=true
test_cli_dry_run_override_env_sweep() {
    echo "Running Test 11: Command-line -d overrides DUST_BUNNY_SWEEP=true"
    local dir="$TEST_DIR/cli_dry_run_override_env_sweep_test"
    mkdir -p "$dir"

    touch -t "$(date +%Y%m%d%H%M.%S --date='8 days ago')" "$dir/cli_old_file.txt"
    touch "$dir/cli_new_file.txt"

    local output
    DUST_BUNNY_SWEEP=true output=$("$SCRIPT_PATH" -a 7 -d "$dir") # CLI -d should override ENV DUST_BUNNY_SWEEP=true

    assert_contains "$output" "Mode: DRY RUN (NO DELETIONS)" "Output should indicate dry run mode from CLI"
    assert_contains "$output" "- $dir/cli_old_file.txt" "Old file should be listed in dry run"
    assert_file_exists "$dir/cli_old_file.txt" "Old file should still exist after CLI dry run"
}

# Test 12: Command-line -s overrides DUST_BUNNY_DRY_RUN=true
test_cli_sweep_override_env_dry_run() {
    echo "Running Test 12: Command-line -s overrides DUST_BUNNY_DRY_RUN=true"
    local dir="$TEST_DIR/cli_sweep_override_env_dry_run_test"
    mkdir -p "$dir"

    touch -t "$(date +%Y%m%d%H%M.%S --date='8 days ago')" "$dir/cli_old_file.txt"
    touch "$dir/cli_new_file.txt"

    local output
    DUST_BUNNY_DRY_RUN=true output=$("$SCRIPT_PATH" -a 7 -s "$dir") # CLI -s should override ENV DUST_BUNNY_DRY_RUN=true

    assert_contains "$output" "Mode: SWEEP (DELETING FILES)" "Output should indicate sweep mode from CLI"
    assert_contains "$output" "removing '$dir/cli_old_file.txt'" "Old file deletion should be logged"
    assert_file_not_exists "$dir/cli_old_file.txt" "Old file should be deleted by CLI sweep"
}


# Run all tests
main() {
    setup

    test_help_message
    test_no_directories
    test_dry_run_no_deletion
    test_sweep_deletion
    test_env_var_age
    test_cli_age_override_env
    test_non_existent_directory
    test_multiple_directories
    test_default_dry_run
    test_env_var_sweep
    test_cli_dry_run_override_env_sweep
    test_cli_sweep_override_env_dry_run

    echo ""
    echo "All tests passed!"
}

# Execute main, ensuring teardown runs
trap teardown EXIT
main
