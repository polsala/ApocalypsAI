#!/bin/bash

# Test suite for Nightly Temporal Debris Sweeper

# Source the script to test
SCRIPT_TO_TEST="../src/temporal_debris_sweeper.sh"

# --- Test Utilities ---
TEST_DIR=""
setup() {
    TEST_DIR=$(mktemp -d -t temporal_debris_test_XXXXXX)
    # Mock rationale: We need a controlled environment for file creation and deletion.
    # Using mktemp ensures isolation and clean-up.
    # We will create files with specific timestamps for testing age logic.
    # We will mock 'rm' to verify what *would* be deleted without actually deleting system files.
    # We will mock 'read' to control user input for confirmation.
    MOCKED_RM_CALLS=()
    MOCKED_READ_REPLY=""
}

teardown() {
    if [ -d "$TEST_DIR" ]; then
        rm -rf "$TEST_DIR"
    fi
}

# Mock rm and read for tests
MOCKED_RM_CALLS=()
MOCKED_READ_REPLY=""

# Mock rationale: Intercept 'rm' calls to verify which files would be deleted
# without actually performing deletion, making tests deterministic and safe.
rm() {
    MOCKED_RM_CALLS+=("$@")
    # echo "MOCKED RM: $@" >&2 # For debugging
}

# Mock rationale: Control user input for confirmation prompts, making tests deterministic.
read() {
    # echo "MOCKED READ: $@" >&2 # For debugging
    if [[ "$1" == *"-n 1 -r"* ]]; then # Check if it's the confirmation prompt
        REPLY="$MOCKED_READ_REPLY"
        return 0
    fi
    # Fallback for other read calls if any, though none expected in this script
    builtin read "$@"
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    if ! echo "$haystack" | grep -qF "$needle"; then
        echo "FAIL: Expected '$haystack' to contain '$needle'"
        exit 1
    fi
}

assert_not_contains() {
    local haystack="$1"
    local needle="$2"
    if echo "$haystack" | grep -qF "$needle"; then
        echo "FAIL: Expected '$haystack' NOT to contain '$needle'"
        exit 1
    fi
}

assert_equals() {
    local actual="$1"
    local expected="$2"
    if [ "$actual" != "$expected" ]; then
        echo "FAIL: Expected '$expected', got '$actual'"
        exit 1
    fi
}

# --- Test Cases ---

test_dry_run_no_debris() {
    setup
    echo "Running test: dry_run_no_debris"

    # Create a file that is not old enough
    touch "$TEST_DIR/recent_file.txt"

    output=$($SCRIPT_TO_TEST -p "$TEST_DIR" -a 1)
    assert_contains "$output" "No temporal debris found"
    assert_contains "$output" "This was a dry run"
    assert_equals "${#MOCKED_RM_CALLS[@]}" 0 # No rm calls in dry run
    teardown
    echo "PASS: dry_run_no_debris"
}

test_dry_run_with_debris() {
    setup
    echo "Running test: dry_run_with_debris"

    # Create an old file
    OLD_DATE_STR=$(date -u -d "2 days ago" "+%Y%m%d%H%M.%S" 2>/dev/null || date -u -v-2d "+%Y%m%d%H%M.%S")
    touch -t "${OLD_DATE_STR%.*}" "$TEST_DIR/old_file.log"

    # Create a recent file
    touch "$TEST_DIR/recent_file.txt"

    output=$($SCRIPT_TO_TEST -p "$TEST_DIR" -a 1) # Age 1 day, old_file.log is older
    assert_contains "$output" "Identified temporal debris:"
    assert_contains "$output" "$TEST_DIR/old_file.log"
    assert_not_contains "$output" "$TEST_DIR/recent_file.txt"
    assert_contains "$output" "This was a dry run"
    assert_equals "${#MOCKED_RM_CALLS[@]}" 0 # No rm calls in dry run
    teardown
    echo "PASS: dry_run_with_debris"
}

test_sweep_with_confirmation_yes() {
    setup
    echo "Running test: sweep_with_confirmation_yes"

    OLD_DATE_STR=$(date -u -d "2 days ago" "+%Y%m%d%H%M.%S" 2>/dev/null || date -u -v-2d "+%Y%m%d%H%M.%S")
    touch -t "${OLD_DATE_STR%.*}" "$TEST_DIR/old_file_to_delete.tmp"
    touch "$TEST_DIR/recent_file.txt"

    MOCKED_READ_REPLY="y" # Mock rationale: Simulate user entering 'y' for confirmation.
    output=$($SCRIPT_TO_TEST -p "$TEST_DIR" -a 1 -s)

    assert_contains "$output" "Sweeping away temporal debris..."
    assert_contains "$output" "Temporal debris swept!"
    assert_equals "${#MOCKED_RM_CALLS[@]}" 1 # Expect one rm call
    assert_contains "${MOCKED_RM_CALLS[0]}" "$TEST_DIR/old_file_to_delete.tmp"
    assert_contains "${MOCKED_RM_CALLS[0]}" "-rf"
    assert_not_contains "${MOCKED_RM_CALLS[0]}" "$TEST_DIR/recent_file.txt"

    teardown
    echo "PASS: sweep_with_confirmation_yes"
}

test_sweep_with_confirmation_no() {
    setup
    echo "Running test: sweep_with_confirmation_no"

    OLD_DATE_STR=$(date -u -d "2 days ago" "+%Y%m%d%H%M.%S" 2>/dev/null || date -u -v-2d "+%Y%m%d%H%M.%S")
    touch -t "${OLD_DATE_STR%.*}" "$TEST_DIR/old_file_not_to_delete.tmp"

    MOCKED_READ_REPLY="n" # Mock rationale: Simulate user entering 'n' for confirmation.
    output=$($SCRIPT_TO_TEST -p "$TEST_DIR" -a 1 -s)

    assert_contains "$output" "Sweeping aborted."
    assert_equals "${#MOCKED_RM_CALLS[@]}" 0 # No rm calls
    teardown
    echo "PASS: sweep_with_confirmation_no"
}

test_sweep_force_no_confirmation() {
    setup
    echo "Running test: sweep_force_no_confirmation"

    OLD_DATE_STR=$(date -u -d "2 days ago" "+%Y%m%d%H%M.%S" 2>/dev/null || date -u -v-2d "+%Y%m%d%H%M.%S")
    touch -t "${OLD_DATE_STR%.*}" "$TEST_DIR/old_file_force_delete.tmp"

    output=$($SCRIPT_TO_TEST -p "$TEST_DIR" -a 1 -f) # -f implies -s and no confirmation

    assert_contains "$output" "Sweeping away temporal debris..."
    assert_contains "$output" "Temporal debris swept!"
    assert_equals "${#MOCKED_RM_CALLS[@]}" 1 # Expect one rm call
    assert_contains "${MOCKED_RM_CALLS[0]}" "$TEST_DIR/old_file_force_delete.tmp"
    teardown
    echo "PASS: sweep_force_no_confirmation"
}

test_invalid_path() {
    setup
    echo "Running test: invalid_path"
    output=$($SCRIPT_TO_TEST -p "/non/existent/path_12345" 2>&1)
    assert_contains "$output" "Error: Path '/non/existent/path_12345' is not a valid directory."
    teardown
    echo "PASS: invalid_path"
}

test_invalid_age() {
    setup
    echo "Running test: invalid_age"
    output=$($SCRIPT_TO_TEST -p "$TEST_DIR" -a "abc" 2>&1)
    assert_contains "$output" "Error: Age must be a non-negative integer."
    output=$($SCRIPT_TO_TEST -p "$TEST_DIR" -a "-5" 2>&1)
    assert_contains "$output" "Error: Age must be a non-negative integer."
    teardown
    echo "PASS: invalid_age"
}

test_directory_deletion() {
    setup
    echo "Running test: directory_deletion"

    OLD_DATE_STR=$(date -u -d "2 days ago" "+%Y%m%d%H%M.%S" 2>/dev/null || date -u -v-2d "+%Y%m%d%H%M.%S")
    mkdir "$TEST_DIR/old_dir"
    touch -t "${OLD_DATE_STR%.*}" "$TEST_DIR/old_dir"
    touch -t "${OLD_DATE_STR%.*}" "$TEST_DIR/old_dir/file_inside.txt"

    MOCKED_READ_REPLY="y"
    output=$($SCRIPT_TO_TEST -p "$TEST_DIR" -a 1 -s)

    assert_contains "$output" "Sweeping away temporal debris..."
    assert_contains "$output" "Temporal debris swept!"
    # find -depth processes contents before directory, so rm -rf will be called on the dir itself
    # The find command lists both the file and the directory. xargs rm -rf will receive both.
    # rm -rf on the directory will remove its contents. So we expect rm -rf to be called on the directory.
    assert_equals "${#MOCKED_RM_CALLS[@]}" 1 # Expect one rm call for the directory
    assert_contains "${MOCKED_RM_CALLS[0]}" "$TEST_DIR/old_dir"
    assert_contains "${MOCKED_RM_CALLS[0]}" "-rf"
    teardown
    echo "PASS: directory_deletion"
}

# Run all tests
echo "--- Running Nightly Temporal Debris Sweeper Tests ---"
test_dry_run_no_debris
test_dry_run_with_debris
test_sweep_with_confirmation_yes
test_sweep_with_confirmation_no
test_sweep_force_no_confirmation
test_invalid_path
test_invalid_age
test_directory_deletion
echo "--- All tests passed! ---"
