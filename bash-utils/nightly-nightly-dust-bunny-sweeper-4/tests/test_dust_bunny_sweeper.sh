#!/bin/bash

# Test suite for Nightly Digital Dust Bunny Sweeper

# --- Test Setup ---
TEST_DIR=$(mktemp -d)
SCRIPT_PATH="$(dirname "$0")"/../src/dust_bunny_sweeper.sh
MOCKED_RM_CALLS=""
MOCKED_RMDIR_CALLS=""

# Mock rationale: We need to prevent actual file system modifications during tests
# and control the output of 'find' to simulate different scenarios.
# Mock 'find' to return predefined lists of files/directories.
# Mock 'rm' and 'rmdir' to record calls without actual deletion.

# Mock 'find' command
find() {
    # Mock rationale: Simulate 'find' behavior without touching the actual filesystem.
    # This allows deterministic testing of the script's parsing and action logic.
    local target_dir="$1"
    shift
    local args=("$@")

    # Scenario 1: Old files
    if [[ " ${args[*]} " =~ " -type f " && " ${args[*]} " =~ " -mtime +90 " ]]; then
        if [[ "$target_dir" == "$TEST_DIR" ]]; then
            echo "$TEST_DIR/old_file.tmp"
            echo "$TEST_DIR/subdir/another_old.log"
        fi
    fi

    # Scenario 2: Empty directories
    if [[ " ${args[*]} " =~ " -type d " && " ${args[*]} " =~ " -empty " ]]; then
        if [[ "$target_dir" == "$TEST_DIR" ]]; then
            echo "$TEST_DIR/empty_dir"
            echo "$TEST_DIR/another_empty"
        fi
    fi

    # Default to empty output if no specific mock matches
    return 0
}

# Mock 'rm' command
rm() {
    # Mock rationale: Prevent actual file deletion during tests.
    # Instead, record the arguments passed to 'rm' for verification.
    MOCKED_RM_CALLS+="rm $*"$'
'
    return 0
}

# Mock 'rmdir' command
rmdir() {
    # Mock rationale: Prevent actual directory deletion during tests.
    # Instead, record the arguments passed to 'rmdir' for verification.
    MOCKED_RMDIR_CALLS+="rmdir $*"$'
'
    return 0
}

# Helper for assertions
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
        echo "FAIL: Expected '$haystack' not to contain '$needle'"
        exit 1
    fi
}

assert_equals() {
    local expected="$1"
    local actual="$2"
    if [ "$expected" != "$actual" ]; then
        echo "FAIL: Expected '$expected', got '$actual'"
        exit 1
    fi
}

# --- Test Cases ---

test_dry_run_reports_files() {
    echo "Running test_dry_run_reports_files..."
    MOCKED_RM_CALLS="" # Reset mocks
    MOCKED_RMDIR_CALLS=""

    local output=$("$SCRIPT_PATH" "$TEST_DIR")
    assert_contains "$output" "Scanning '$TEST_DIR' for digital dust bunnies older than 90 days..."
    assert_contains "$output" "Mode: Dry Run (no changes)"
    assert_contains "$output" "Found these ancient file dust bunnies:"
    assert_contains "$output" "- $TEST_DIR/old_file.tmp"
    assert_contains "$output" "- $TEST_DIR/subdir/another_old.log"
    assert_contains "$output" "Found these empty directory dust bunnies:"
    assert_contains "$output" "- $TEST_DIR/empty_dir"
    assert_contains "$output" "- $TEST_DIR/another_empty"
    assert_not_contains "$output" "(Swept away:"
    assert_equals "" "$MOCKED_RM_CALLS"
    assert_equals "" "$MOCKED_RMDIR_CALLS"
    echo "  PASS"
}

test_clean_mode_deletes_files() {
    echo "Running test_clean_mode_deletes_files..."
    MOCKED_RM_CALLS="" # Reset mocks
    MOCKED_RMDIR_CALLS=""

    local output=$("$SCRIPT_PATH" -c "$TEST_DIR")
    assert_contains "$output" "Mode: Cleaning (deleting files)"
    assert_contains "$output" "(Swept away: $TEST_DIR/old_file.tmp)"
    assert_contains "$output" "(Swept away: $TEST_DIR/subdir/another_old.log)"
    assert_contains "$output" "(Swept away: $TEST_DIR/empty_dir)"
    assert_contains "$output" "(Swept away: $TEST_DIR/another_empty)"
    assert_contains "$MOCKED_RM_CALLS" "rm -f $TEST_DIR/old_file.tmp"
    assert_contains "$MOCKED_RM_CALLS" "rm -f $TEST_DIR/subdir/another_old.log"
    assert_contains "$MOCKED_RMDIR_CALLS" "rmdir $TEST_DIR/empty_dir"
    assert_contains "$MOCKED_RMDIR_CALLS" "rmdir $TEST_DIR/another_empty"
    echo "  PASS"
}

test_custom_days_old() {
    echo "Running test_custom_days_old..."
    MOCKED_RM_CALLS="" # Reset mocks
    MOCKED_RMDIR_CALLS=""

    # Mock rationale: The 'find' mock doesn't currently use the -mtime argument
    # directly for its output, but the script's output should reflect the
    # passed argument. We'll check the output string.
    local output=$("$SCRIPT_PATH" -d 30 "$TEST_DIR")
    assert_contains "$output" "Scanning '$TEST_DIR' for digital dust bunnies older than 30 days..."
    assert_contains "$output" "Mode: Dry Run (no changes)"
    echo "  PASS"
}

test_invalid_directory_exits_with_error() {
    echo "Running test_invalid_directory_exits_with_error..."
    local non_existent_dir="$TEST_DIR/non_existent_path"
    local output=$(! "$SCRIPT_PATH" "$non_existent_dir" 2>&1) # Capture stderr
    assert_contains "$output" "Error: Target directory '$non_existent_dir' does not exist or is not a directory."
    echo "  PASS"
}

test_no_dust_bunnies_found() {
    echo "Running test_no_dust_bunnies_found..."
    MOCKED_RM_CALLS=""
    MOCKED_RMDIR_CALLS=""

    # Mock rationale: Temporarily override 'find' to simulate a scenario where no dust bunnies are found.
    # This ensures the script correctly reports the absence of findings.
    local original_find_mock=$(declare -f find) # Store original mock definition

    # Redefine find to return nothing
    find() {
        return 0
    }

    local output=$("$SCRIPT_PATH" "$TEST_DIR")
    assert_contains "$output" "No ancient file dust bunnies found. Your files are spry!"
    assert_contains "$output" "No lonely, empty directory dust bunnies found. All directories are bustling!"
    assert_equals "" "$MOCKED_RM_CALLS"
    assert_equals "" "$MOCKED_RMDIR_CALLS"

    # Restore original find mock
    eval "$original_find_mock"
    echo "  PASS"
}


# --- Run Tests ---
test_dry_run_reports_files
test_clean_mode_deletes_files
test_custom_days_old
test_invalid_directory_exits_with_error
test_no_dust_bunnies_found

# --- Cleanup ---
rm -rf "$TEST_DIR"
unset -f find rm rmdir # Unset mocks to avoid interfering with other scripts
echo "All tests completed."
