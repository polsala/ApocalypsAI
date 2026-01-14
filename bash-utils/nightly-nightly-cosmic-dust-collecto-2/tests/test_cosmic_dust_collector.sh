#!/bin/bash

# Test suite for Nightly Cosmic Dust Collector

# --- Test Setup ---
TEST_DIR=$(mktemp -d -t cosmic-dust-test-XXXXXX)
SCRIPT_PATH="./src/cosmic_dust_collector.sh"
EXIT_CODE=0

# Clean up function
cleanup() {
    if [[ -d "$TEST_DIR" ]]; then
        rm -rf "$TEST_DIR"
    fi
}
trap cleanup EXIT

# Assertion function
assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$expected" != "$actual" ]]; then
        echo "FAIL: $message"
        echo "  Expected: '$expected'"
        echo "  Actual:   '$actual'"
        EXIT_CODE=1
    else
        echo "PASS: $message"
    fi
}

assert_file_exists() {
    local file="$1"
    local message="$2"
    if [[ ! -f "$file" ]]; then
        echo "FAIL: $message - File '$file' does not exist."
        EXIT_CODE=1
    else
        echo "PASS: $message - File '$file' exists."
    fi
}

assert_file_not_exists() {
    local file="$1"
    local message="$2"
    if [[ -f "$file" ]]; then
        echo "FAIL: $message - File '$file' unexpectedly exists."
        EXIT_CODE=1
    else
        echo "PASS: $message - File '$file' does not exist."
    fi
}

assert_dir_exists() {
    local dir="$1"
    local message="$2"
    if [[ ! -d "$dir" ]]; then
        echo "FAIL: $message - Directory '$dir' does not exist."
        EXIT_CODE=1
    else
        echo "PASS: $message - Directory '$dir' exists."
    fi
}

assert_dir_not_exists() {
    local dir="$1"
    local message="$2"
    if [[ -d "$dir" ]]; then
        echo "FAIL: $message - Directory '$dir' unexpectedly exists."
        EXIT_CODE=1
    else
        echo "PASS: $message - Directory '$dir' does not exist."
    fi
}

# --- Test Cases ---

echo "--- Running Nightly Cosmic Dust Collector Tests ---"

# Test 1: Help message
test_help_message() {
    echo "Test 1: Display help message"
    local output=$("$SCRIPT_PATH" --help 2>&1)
    assert_equals 0 $? "Help command should exit with 0"
    [[ "$output" == *"Usage: $0 [OPTIONS] --target <directory>"* ]]
    assert_equals true $? "Help message should contain usage info"
}
test_help_message

# Test 2: No target directory provided
test_no_target() {
    echo "Test 2: No target directory provided"
    local output=$("$SCRIPT_PATH" 2>&1)
    assert_equals 1 $? "Script should exit with 1 if no target"
    [[ "$output" == *"Error: At least one --target directory is required."* ]]
    assert_equals true $? "Error message for missing target"
}
test_no_target

# Test 3: Invalid age argument
test_invalid_age() {
    echo "Test 3: Invalid age argument"
    local output=$("$SCRIPT_PATH" --age abc --target "$TEST_DIR" 2>&1)
    assert_equals 1 $? "Script should exit with 1 for invalid age"
    [[ "$output" == *"Error: --age requires a positive integer for days."* ]]
    assert_equals true $? "Error message for invalid age"
}
test_invalid_age

# Test 4: Dry run - old file and empty dir
test_dry_run_old_file_empty_dir() {
    echo "Test 4: Dry run - old file and empty directory"
    local sub_dir="$TEST_DIR/old_stuff"
    mkdir -p "$sub_dir"
    touch -d "8 days ago" "$sub_dir/old_file.log"
    touch "$sub_dir/new_file.txt" # Should not be collected
    mkdir -p "$TEST_DIR/empty_dir"
    mkdir -p "$TEST_DIR/non_empty_dir"
    touch "$TEST_DIR/non_empty_dir/file.txt"

    local output=$("$SCRIPT_PATH" --dry-run --age 7 --target "$TEST_DIR" 2>&1)
    assert_equals 0 $? "Dry run should exit with 0"

    [[ "$output" == *"--- DRY RUN MODE --- No actual deletions will occur. ---"* ]]
    assert_equals true $? "Dry run message present"
    [[ "$output" == *"[FILE] old_file.log"* ]]
    assert_equals true $? "Dry run should list old_file.log"
    [[ "$output" == *"[DIR] empty_dir"* ]]
    assert_equals true $? "Dry run should list empty_dir"
    [[ "$output" != *"[FILE] new_file.txt"* ]]
    assert_equals true $? "Dry run should NOT list new_file.txt"
    [[ "$output" != *"[DIR] non_empty_dir"* ]]
    assert_equals true $? "Dry run should NOT list non_empty_dir"

    assert_file_exists "$sub_dir/old_file.log" "Old file should still exist after dry run"
    assert_file_exists "$sub_dir/new_file.txt" "New file should still exist after dry run"
    assert_dir_exists "$TEST_DIR/empty_dir" "Empty dir should still exist after dry run"
    assert_dir_exists "$TEST_DIR/non_empty_dir" "Non-empty dir should still exist after dry run"
}
test_dry_run_old_file_empty_dir
cleanup && TEST_DIR=$(mktemp -d -t cosmic-dust-test-XXXXXX) # Reset TEST_DIR

# Test 5: Actual run - old file and empty dir
test_actual_run_old_file_empty_dir() {
    echo "Test 5: Actual run - old file and empty directory"
    local sub_dir="$TEST_DIR/old_stuff"
    mkdir -p "$sub_dir"
    touch -d "8 days ago" "$sub_dir/old_file.log"
    touch "$sub_dir/new_file.txt" # Should not be collected
    mkdir -p "$TEST_DIR/empty_dir"
    mkdir -p "$TEST_DIR/non_empty_dir"
    touch "$TEST_DIR/non_empty_dir/file.txt"

    local output=$("$SCRIPT_PATH" --age 7 --target "$TEST_DIR" 2>&1)
    assert_equals 0 $? "Actual run should exit with 0"

    [[ "$output" == *"[FILE] old_file.log"* ]]
    assert_equals true $? "Actual run should list old_file.log"
    [[ "$output" == *"[DIR] empty_dir"* ]]
    assert_equals true $? "Actual run should list empty_dir"
    [[ "$output" != *"[FILE] new_file.txt"* ]]
    assert_equals true $? "Actual run should NOT list new_file.txt"
    [[ "$output" != *"[DIR] non_empty_dir"* ]]
    assert_equals true $? "Actual run should NOT list non_empty_dir"

    assert_file_not_exists "$sub_dir/old_file.log" "Old file should be removed after actual run"
    assert_file_exists "$sub_dir/new_file.txt" "New file should still exist after actual run"
    assert_dir_not_exists "$TEST_DIR/empty_dir" "Empty dir should be removed after actual run"
    assert_dir_exists "$TEST_DIR/non_empty_dir" "Non-empty dir should still exist after actual run"
}
test_actual_run_old_file_empty_dir
cleanup && TEST_DIR=$(mktemp -d -t cosmic-dust-test-XXXXXX) # Reset TEST_DIR

# Test 6: Multiple target directories
test_multiple_targets() {
    echo "Test 6: Multiple target directories"
    local target1="$TEST_DIR/target1"
    local target2="$TEST_DIR/target2"
    mkdir -p "$target1" "$target2"
    touch -d "8 days ago" "$target1/old_file1.log"
    mkdir -p "$target2/empty_sub"

    local output=$("$SCRIPT_PATH" --dry-run --age 7 --target "$target1" --target "$target2" 2>&1)
    assert_equals 0 $? "Dry run with multiple targets should exit with 0"
    [[ "$output" == *"[FILE] old_file1.log"* ]]
    assert_equals true $? "Dry run should list old_file1.log from target1"
    [[ "$output" == *"[DIR] empty_sub"* ]]
    assert_equals true $? "Dry run should list empty_sub from target2"

    "$SCRIPT_PATH" --age 7 --target "$target1" --target "$target2" > /dev/null 2>&1
    assert_file_not_exists "$target1/old_file1.log" "old_file1.log should be removed"
    assert_dir_not_exists "$target2/empty_sub" "empty_sub should be removed"
}
test_multiple_targets
cleanup && TEST_DIR=$(mktemp -d -t cosmic-dust-test-XXXXXX) # Reset TEST_DIR

# Test 7: Age 0 - only empty directories
test_age_zero() {
    echo "Test 7: Age 0 - only empty directories"
    local sub_dir="$TEST_DIR/sub"
    mkdir -p "$sub_dir"
    touch -d "1 day ago" "$sub_dir/recent_file.txt"
    mkdir -p "$TEST_DIR/empty_dir_age0"

    local output=$("$SCRIPT_PATH" --dry-run --age 0 --target "$TEST_DIR" 2>&1)
    assert_equals 0 $? "Dry run with age 0 should exit with 0"
    [[ "$output" != *"[FILE] recent_file.txt"* ]]
    assert_equals true $? "Dry run should NOT list recent_file.txt with age 0"
    [[ "$output" == *"[DIR] empty_dir_age0"* ]]
    assert_equals true $? "Dry run should list empty_dir_age0 with age 0"

    "$SCRIPT_PATH" --age 0 --target "$TEST_DIR" > /dev/null 2>&1
    assert_file_exists "$sub_dir/recent_file.txt" "recent_file.txt should still exist"
    assert_dir_not_exists "$TEST_DIR/empty_dir_age0" "empty_dir_age0 should be removed"
}
test_age_zero
cleanup && TEST_DIR=$(mktemp -d -t cosmic-dust-test-XXXXXX) # Reset TEST_DIR

# Test 8: Non-existent target directory
test_non_existent_target() {
    echo "Test 8: Non-existent target directory"
    local non_existent_dir="$TEST_DIR/does_not_exist"
    local output=$("$SCRIPT_PATH" --target "$non_existent_dir" 2>&1)
    assert_equals 0 $? "Script should exit 0 even if target doesn't exist (with warning)"
    [[ "$output" == *"Warning: Target directory '$non_existent_dir' does not exist or is not a directory. Skipping."* ]]
    assert_equals true $? "Warning message for non-existent target"
}
test_non_existent_target
cleanup && TEST_DIR=$(mktemp -d -t cosmic-dust-test-XXXXXX) # Reset TEST_DIR

# Test 9: Nested empty directories
test_nested_empty_dirs() {
    echo "Test 9: Nested empty directories"
    mkdir -p "$TEST_DIR/parent_empty/child_empty/grandchild_empty"
    mkdir -p "$TEST_DIR/parent_with_file/child_empty"
    touch "$TEST_DIR/parent_with_file/file.txt"

    local output=$("$SCRIPT_PATH" --dry-run --age 0 --target "$TEST_DIR" 2>&1)
    assert_equals 0 $? "Dry run for nested empty dirs should exit 0"
    [[ "$output" == *"[DIR] grandchild_empty"* ]]
    assert_equals true $? "Dry run should list grandchild_empty"
    [[ "$output" == *"[DIR] child_empty"* ]]
    assert_equals true $? "Dry run should list child_empty (from parent_empty)"
    [[ "$output" == *"[DIR] parent_empty"* ]]
    assert_equals true $? "Dry run should list parent_empty"
    [[ "$output" != *"[DIR] parent_with_file"* ]]
    assert_equals true $? "Dry run should NOT list parent_with_file"
    [[ "$output" != *"[DIR] child_empty"* && "$output" == *"$TEST_DIR/parent_with_file/child_empty"* ]] # Ensure it doesn't list the one under parent_with_file
    assert_equals true $? "Dry run should NOT list child_empty under parent_with_file"

    "$SCRIPT_PATH" --age 0 --target "$TEST_DIR" > /dev/null 2>&1
    assert_dir_not_exists "$TEST_DIR/parent_empty" "parent_empty should be removed"
    assert_dir_not_exists "$TEST_DIR/parent_empty/child_empty" "child_empty should be removed"
    assert_dir_not_exists "$TEST_DIR/parent_empty/child_empty/grandchild_empty" "grandchild_empty should be removed"
    assert_dir_exists "$TEST_DIR/parent_with_file" "parent_with_file should still exist"
    assert_dir_exists "$TEST_DIR/parent_with_file/child_empty" "child_empty under parent_with_file should still exist (rmdir fails if not empty)"
    assert_file_exists "$TEST_DIR/parent_with_file/file.txt" "file.txt should still exist"
}
test_nested_empty_dirs
cleanup && TEST_DIR=$(mktemp -d -t cosmic-dust-test-XXXXXX) # Reset TEST_DIR


echo "--- All tests completed ---"
exit $EXIT_CODE
