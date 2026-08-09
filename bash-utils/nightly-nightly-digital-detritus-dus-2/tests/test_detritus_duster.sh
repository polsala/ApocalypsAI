#!/bin/bash

# Test script for nightly-digital-detritus-duster.sh

# --- Test Setup ---
TEST_DIR=$(mktemp -d -t duster-test-XXXXXX)
QUARANTINE_DIR="$TEST_DIR/DigitalQuarantineZone"
SCRIPT_PATH="$(dirname "$0")"/../src/nightly-digital-detritus-duster.sh
MOCKED_FIND_OUTPUT=""
MOCKED_READ_REPLY="y" # Default to 'y' for moving files in non-dry-run tests
MOCKED_MV_CALLS=()

# Mock rationale: Overriding `find` to control its output deterministically.
# This prevents actual filesystem scans and ensures tests are fast and isolated.
find() {
    echo -e "$MOCKED_FIND_OUTPUT"
}

# Mock rationale: Overriding `read` to provide deterministic user input.
# This prevents tests from hanging and allows testing both 'y' and 'N' scenarios.
read() {
    if [[ "$1" == *"-p"* ]]; then # Check if -p (prompt) is used
        echo "$2" # Print the prompt
    fi
    REPLY="$MOCKED_READ_REPLY"
    echo "$REPLY" # Simulate user typing
}

# Mock rationale: Overriding `mv` to record calls instead of performing actual file moves.
# This allows verification of which files *would* have been moved without altering the filesystem.
mv() {
    MOCKED_MV_CALLS+=("$@")
    # Simulate success
    return 0
}

# Helper function to create a file with a specific modification time
create_test_file() {
    local path="$1"
    local days_ago="$2"
    touch -t "$(date -d "$days_ago days ago" +%Y%m%d%H%M.%S)" "$path"
}

# Helper function to assert test results
assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [ "$expected" == "$actual" ]; then
        echo "✅ Test Passed: $message"
    else
        echo "❌ Test Failed: $message"
        echo "   Expected: '$expected'"
        echo "   Actual:   '$actual'"
        exit 1
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if [[ "$haystack" == *"$needle"* ]]; then
        echo "✅ Test Passed: $message"
    else
        echo "❌ Test Failed: $message"
        echo "   Expected to contain: '$needle'"
        echo "   Actual output: '$haystack'"
        exit 1
    fi
}

assert_not_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if [[ "$haystack" != *"$needle"* ]]; then
        echo "✅ Test Passed: $message"
    else
        echo "❌ Test Failed: $message"
        echo "   Expected NOT to contain: '$needle'"
        echo "   Actual output: '$haystack'"
        exit 1
    fi
}

# Reset mocks and environment for each test
reset_test_env() {
    rm -rf "$TEST_DIR"/*
    mkdir -p "$TEST_DIR"
    mkdir -p "$QUARANTINE_DIR"
    MOCKED_FIND_OUTPUT=""
    MOCKED_READ_REPLY="y"
    MOCKED_MV_CALLS=()
}

# --- Test Cases ---

echo "Running tests for nightly-digital-detritus-duster.sh"

# Test 1: No files found
test_no_files_found() {
    reset_test_env
    local output=$("$SCRIPT_PATH" -a 1 "$TEST_DIR" 2>&1)
    assert_contains "$output" "No detritus found" "Test 1: Should report no detritus when find is empty"
    assert_equals "0" "${#MOCKED_MV_CALLS[@]}" "Test 1: No mv calls should be made"
}

# Test 2: Dry run - files found, correct output
test_dry_run_files_found() {
    reset_test_env
    MOCKED_FIND_OUTPUT="$TEST_DIR/old_file_1.txt\n$TEST_DIR/old_file_2.log"
    local output=$("$SCRIPT_PATH" -d -a 1 "$TEST_DIR" 2>&1)
    assert_contains "$output" "Performing a dry run" "Test 2: Should indicate dry run"
    assert_contains "$output" "Found a dusty relic: '$TEST_DIR/old_file_1.txt'" "Test 2: Should list old_file_1"
    assert_contains "$output" "Found a dusty relic: '$TEST_DIR/old_file_2.log'" "Test 2: Should list old_file_2"
    assert_equals "0" "${#MOCKED_MV_CALLS[@]}" "Test 2: No mv calls in dry run"
}

# Test 3: Actual run - files moved, user confirms
test_actual_run_user_confirms() {
    reset_test_env
    MOCKED_FIND_OUTPUT="$TEST_DIR/old_file_1.txt\n$TEST_DIR/old_file_2.log"
    MOCKED_READ_REPLY="y"
    local output=$("$SCRIPT_PATH" -a 1 "$TEST_DIR" 2>&1)
    assert_contains "$output" "Sweeping away digital detritus" "Test 3: Should indicate dusting"
    assert_contains "$output" "Dusted: '$TEST_DIR/old_file_1.txt'" "Test 3: Should report old_file_1 dusted"
    assert_contains "$output" "Dusted: '$TEST_DIR/old_file_2.log'" "Test 3: Should report old_file_2 dusted"
    assert_equals "4" "${#MOCKED_MV_CALLS[@]}" "Test 3: Two mv calls expected (file path and dest path for each)"
    assert_contains "${MOCKED_MV_CALLS[*]}" "$TEST_DIR/old_file_1.txt" "Test 3: mv called for old_file_1"
    assert_contains "${MOCKED_MV_CALLS[*]}" "$TEST_DIR/old_file_2.log" "Test 3: mv called for old_file_2"
    assert_contains "${MOCKED_MV_CALLS[*]}" "$QUARANTINE_DIR/" "Test 3: mv called with quarantine dir"
}

# Test 4: Actual run - files not moved, user declines
test_actual_run_user_declines() {
    reset_test_env
    MOCKED_FIND_OUTPUT="$TEST_DIR/old_file_1.txt"
    MOCKED_READ_REPLY="n"
    local output=$("$SCRIPT_PATH" -a 1 "$TEST_DIR" 2>&1)
    assert_contains "$output" "Dusting aborted" "Test 4: Should report dusting aborted"
    assert_not_contains "$output" "Dusted: '$TEST_DIR/old_file_1.txt'" "Test 4: Should not report file dusted"
    assert_equals "0" "${#MOCKED_MV_CALLS[@]}" "Test 4: No mv calls when user declines"
}

# Test 5: Exclusion pattern works
test_exclusion_pattern() {
    reset_test_env
    MOCKED_FIND_OUTPUT="$TEST_DIR/old_file.txt\n$TEST_DIR/important.log\n$TEST_DIR/temp_dir/cache.tmp"
    MOCKED_READ_REPLY="y"
    local output=$("$SCRIPT_PATH" -a 1 -e "*.log" -e "temp_dir/*" "$TEST_DIR" 2>&1)
    assert_contains "$output" "Skipping (excluded): '$TEST_DIR/important.log'" "Test 5: Should skip .log file"
    assert_contains "$output" "Skipping (excluded): '$TEST_DIR/temp_dir/cache.tmp'" "Test 5: Should skip temp_dir file"
    assert_contains "$output" "Dusted: '$TEST_DIR/old_file.txt'" "Test 5: Should dust non-excluded file"
    assert_equals "2" "${#MOCKED_MV_CALLS[@]}" "Test 5: One mv call expected (for old_file.txt)"
    assert_contains "${MOCKED_MV_CALLS[*]}" "$TEST_DIR/old_file.txt" "Test 5: mv called for old_file.txt"
    assert_not_contains "${MOCKED_MV_CALLS[*]}" "$TEST_DIR/important.log" "Test 5: mv not called for important.log"
}

# Test 6: Custom quarantine directory
test_custom_quarantine_dir() {
    reset_test_env
    local custom_q_dir="$TEST_DIR/MyCustomCompost"
    MOCKED_FIND_OUTPUT="$TEST_DIR/old_file.txt"
    MOCKED_READ_REPLY="y"
    local output=$("$SCRIPT_PATH" -a 1 -q "$custom_q_dir" "$TEST_DIR" 2>&1)
    assert_contains "$output" "Digital Quarantine Zone created at: '$custom_q_dir'" "Test 6: Should report custom quarantine created"
    assert_contains "$output" "Dusted: '$TEST_DIR/old_file.txt'" "Test 6: Should dust file"
    assert_contains "${MOCKED_MV_CALLS[*]}" "$custom_q_dir/" "Test 6: mv called with custom quarantine dir"
}

# Test 7: Invalid age parameter
test_invalid_age() {
    reset_test_env
    local output=$("$SCRIPT_PATH" -a abc "$TEST_DIR" 2>&1)
    assert_contains "$output" "Error: Age must be a positive integer." "Test 7: Should error on invalid age"
    assert_contains "$output" "Usage:" "Test 7: Should show usage"
}

# Test 8: No target directories
test_no_target_dirs() {
    reset_test_env
    local output=$("$SCRIPT_PATH" -a 1 2>&1)
    assert_contains "$output" "Error: Please specify at least one directory to dust." "Test 8: Should error on no target dirs"
    assert_contains "$output" "Usage:" "Test 8: Should show usage"
}

# Test 9: Non-existent target directory
test_non_existent_target_dir() {
    reset_test_env
    local non_existent_dir="$TEST_DIR/non_existent"
    local output=$("$SCRIPT_PATH" -a 1 "$non_existent_dir" 2>&1)
    assert_contains "$output" "Warning: Directory '$non_existent_dir' not found or not a directory. Skipping." "Test 9: Should warn and skip non-existent dir"
    assert_contains "$output" "No detritus found" "Test 9: Should report no detritus"
}

# Run all tests
test_no_files_found
test_dry_run_files_found
test_actual_run_user_confirms
test_actual_run_user_declines
test_exclusion_pattern
test_custom_quarantine_dir
test_invalid_age
test_no_target_dirs
test_non_existent_target_dir

echo "All tests completed successfully!"

# --- Cleanup ---
rm -rf "$TEST_DIR"
