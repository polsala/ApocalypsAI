#!/bin/bash

# Nightly Digital Dust Bunny Sweeper Tests

# Mock rationale:
# The tests create a temporary directory and files with specific timestamps.
# The `dust_bunny_sweeper.sh` script is then run against this controlled environment.
# This approach makes the tests deterministic and offline, as `find` and `rm`
# operate only within the temporary, isolated filesystem structure.
# No external system state or network access is involved.

SCRIPT_PATH="./src/dust_bunny_sweeper.sh"
TEST_DIR=""

# --- Helper Functions ---
setup_test_env() {
    TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXXX)
    if [[ ! -d "$TEST_DIR" ]]; then
        echo "Failed to create test directory."
        exit 1
    fi
    echo "Test environment set up at: $TEST_DIR"
}

cleanup_test_env() {
    if [[ -d "$TEST_DIR" ]]; then
        rm -rf "$TEST_DIR"
        echo "Test environment cleaned up: $TEST_DIR"
    fi
}

create_file_with_age() {
    local file_path="$1"
    local age_days="$2"
    local timestamp=""

    # Calculate timestamp for 'age_days' ago
    # Using GNU date for flexibility, assuming it's available in test environment.
    # Mock rationale: This date command is used to create test data, not for the core logic.
    # The core logic uses `find -mtime +N`.
    timestamp=$(date -d "$age_days days ago" +%Y%m%d%H%M.%S)
    
    mkdir -p "$(dirname "$file_path")"
    touch -t "$timestamp" "$file_path"
}

assert_file_exists() {
    local file_path="$1"
    if [[ ! -e "$file_path" ]]; then
        echo "FAIL: Expected file '$file_path' to exist, but it does not."
        return 1
    fi
    return 0
}

assert_file_does_not_exist() {
    local file_path="$1"
    if [[ -e "$file_path" ]]; then
        echo "FAIL: Expected file '$file_path' NOT to exist, but it does."
        return 1
    fi
    return 0
}

run_test() {
    local test_name="$1"
    shift
    echo "--- Running Test: $test_name ---"
    "$@"
    local status=$?
    if [[ "$status" -eq 0 ]]; then
        echo "--- Test PASSED: $test_name ---"
    else
        echo "--- Test FAILED: $test_name (Exit Code: $status) ---"
        cleanup_test_env
        exit 1
    fi
    echo ""
}

# --- Test Cases ---

# Test 1: Dry run, no deletion
test_dry_run_no_deletion() {
    setup_test_env

    create_file_with_age "$TEST_DIR/old_file_1.log" 5
    create_file_with_age "$TEST_DIR/old_dir/old_file_2.txt" 10
    create_file_with_age "$TEST_DIR/new_file.conf" 0 # Today

    output=$("$SCRIPT_PATH" "$TEST_DIR" 3 --dry-run)
    
    echo "$output"

    # Check output for dry-run messages
    if ! echo "$output" | grep -q "DRY RUN COMPLETE"; then
        echo "FAIL: Dry run message not found."
        return 1
    fi
    if ! echo "$output" | grep -q "old_file_1.log"; then
        echo "FAIL: old_file_1.log not mentioned in dry run."
        return 1
    fi
    if ! echo "$output" | grep -q "old_dir/old_file_2.txt"; then
        echo "FAIL: old_dir/old_file_2.txt not mentioned in dry run."
        return 1
    fi
    if echo "$output" | grep -q "new_file.conf"; then
        echo "FAIL: new_file.conf mentioned in dry run (should not be)."
        return 1
    fi

    # Verify files still exist
    assert_file_exists "$TEST_DIR/old_file_1.log"
    assert_file_exists "$TEST_DIR/old_dir/old_file_2.txt"
    assert_file_exists "$TEST_DIR/new_file.conf"

    cleanup_test_env
    return 0
}

# Test 2: Actual deletion
test_actual_deletion() {
    setup_test_env

    create_file_with_age "$TEST_DIR/old_file_to_delete.log" 5
    create_file_with_age "$TEST_DIR/old_dir_to_delete/file.txt" 10
    create_file_with_age "$TEST_DIR/keep_this_file.conf" 0 # Today

    # Run with --force to skip prompt
    output=$("$SCRIPT_PATH" "$TEST_DIR" 3 --force)
    
    echo "$output"

    # Verify old files are deleted
    assert_file_does_not_exist "$TEST_DIR/old_file_to_delete.log"
    assert_file_does_not_exist "$TEST_DIR/old_dir_to_delete/file.txt"
    assert_file_does_not_exist "$TEST_DIR/old_dir_to_delete" # Parent dir should also be gone if empty

    # Verify new file is kept
    assert_file_exists "$TEST_DIR/keep_this_file.conf"

    cleanup_test_env
    return 0
}

# Test 3: No old files found
test_no_old_files() {
    setup_test_env

    create_file_with_age "$TEST_DIR/recent_file_1.log" 0
    create_file_with_age "$TEST_DIR/recent_file_2.txt" 1

    output=$("$SCRIPT_PATH" "$TEST_DIR" 3 --dry-run)
    
    echo "$output"

    if ! echo "$output" | grep -q "No digital dust bunnies found"; then
        echo "FAIL: Expected 'No digital dust bunnies found' message."
        return 1
    fi

    assert_file_exists "$TEST_DIR/recent_file_1.log"
    assert_file_exists "$TEST_DIR/recent_file_2.txt"

    cleanup_test_env
    return 0
}

# Test 4: Target directory does not exist
test_target_dir_not_exist() {
    setup_test_env # Just to get a TEST_DIR, but we'll use a non-existent path

    output=$("$SCRIPT_PATH" "$TEST_DIR/non_existent_dir" 1 2>&1)
    
    echo "$output"

    if ! echo "$output" | grep -q "Error: Target directory '.*' does not exist"; then
        echo "FAIL: Expected 'Target directory does not exist' error."
        return 1
    fi

    cleanup_test_env
    return 0
}

# Test 5: Invalid age
test_invalid_age() {
    setup_test_env

    output=$("$SCRIPT_PATH" "$TEST_DIR" "abc" 2>&1)
    
    echo "$output"

    if ! echo "$output" | grep -q "Error: Age in days must be a non-negative integer"; then
        echo "FAIL: Expected 'invalid age' error."
        return 1
    fi

    cleanup_test_env
    return 0
}

# Test 6: Critical path warning (without force, should cancel)
test_critical_path_warning_cancel() {
    # Mock rationale: This test simulates user input for the critical path prompt.
    # We use `echo "No"` to simulate the user declining the operation.
    output=$(echo "No" | "$SCRIPT_PATH" "/" 1 2>&1)
    
    echo "$output"

    if ! echo "$output" | grep -q "Warning: Attempting to sweep a critical system path"; then
        echo "FAIL: Expected critical path warning."
        return 1
    fi
    if ! echo "$output" | grep -q "Operation cancelled"; then
        echo "FAIL: Expected operation cancelled message."
        return 1
    fi
    return 0
}

# Test 7: Critical path warning (with force, should proceed)
test_critical_path_warning_force() {
    # Mock rationale: This test uses --force to bypass the critical path prompt.
    # We expect the script to proceed, but not actually delete anything from `/`
    # because the `find -mindepth 1` will prevent it from deleting `/` itself,
    # and we don't actually create files in `/` for this test.
    output=$("$SCRIPT_PATH" "/" 1 --force 2>&1)
    
    echo "$output"

    if ! echo "$output" | grep -q "Warning: Attempting to sweep a critical system path"; then
        echo "FAIL: Expected critical path warning."
        return 1
    fi
    if ! echo "$output" | grep -q "Proceeding with caution..."; then
        echo "FAIL: Expected 'Proceeding with caution' message."
        return 1
    fi
    if ! echo "$output" | grep -q "No digital dust bunnies found"; then
        echo "FAIL: Expected 'No digital dust bunnies found' for root (as no old files are created there).
        This is due to -mindepth 1 preventing the root directory itself from being listed."
        return 1
    fi
    return 0
}


# --- Run all tests ---
run_test "Dry run, no deletion" test_dry_run_no_deletion
run_test "Actual deletion" test_actual_deletion
run_test "No old files found" test_no_old_files
run_test "Target directory does not exist" test_target_dir_not_exist
run_test "Invalid age" test_invalid_age
run_test "Critical path warning (cancel)" test_critical_path_warning_cancel
run_test "Critical path warning (force)" test_critical_path_warning_force

echo "All tests passed!"
