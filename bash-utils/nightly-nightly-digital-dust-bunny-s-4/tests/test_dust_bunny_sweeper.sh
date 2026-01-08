#!/bin/bash

# Test suite for Nightly Digital Dust Bunny Sweeper

# --- Test Configuration ---
TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXXX)
SCRIPT_PATH="./src/dust_bunny_sweeper.sh"
# --- End Test Configuration ---

# --- Helper Functions ---
setup_test_env() {
    mkdir -p "$TEST_DIR/subdir1" "$TEST_DIR/subdir2" "$TEST_DIR/empty_dir"
    
    # Create old files (older than 7 days)
    touch -d "8 days ago" "$TEST_DIR/old_file1.log"
    touch -d "10 days ago" "$TEST_DIR/subdir1/old_file2.tmp"
    touch -d "15 days ago" "$TEST_DIR/subdir1/old_file3.cache"
    touch -d "9 days ago" "$TEST_DIR/empty_dir" # Make empty_dir old too

    # Create recent files (newer than 7 days)
    touch -d "1 day ago" "$TEST_DIR/recent_file1.log"
    touch -d "3 days ago" "$TEST_DIR/subdir2/recent_file2.tmp"
    
    # Create an empty directory that is recent
    mkdir -p "$TEST_DIR/recent_empty_dir"
    touch -d "1 day ago" "$TEST_DIR/recent_empty_dir"

    # Create a non-empty old directory (should not be found by -empty)
    mkdir -p "$TEST_DIR/old_non_empty_dir"
    touch -d "8 days ago" "$TEST_DIR/old_non_empty_dir/file_inside.txt"
    touch -d "8 days ago" "$TEST_DIR/old_non_empty_dir" # Make dir itself old
}

cleanup_test_env() {
    rm -rf "$TEST_DIR"
}

# Mock rationale: We need to prevent actual file system modifications during tests.
# Mocking 'find' allows us to control exactly what the script "sees" as old files.
# Mocking 'rm' allows us to verify that the script *would* attempt to delete the correct files,
# without actually deleting anything from the test environment or real system.
# We capture the arguments passed to 'rm' to assert correctness.

MOCKED_RM_CALLS=""
mock_rm() {
    MOCKED_RM_CALLS+="rm $*;"
    # echo "MOCKED RM: $*" >&2 # For debugging mock calls
    return 0 # Always succeed in mock
}

MOCKED_FIND_OUTPUT=""
mock_find() {
    echo -n "$MOCKED_FIND_OUTPUT"
    return 0
}

# Store original commands
ORIG_RM=$(which rm)
ORIG_FIND=$(which find)

# --- Test Cases ---

test_no_arguments_shows_usage() {
    echo "Running test: No arguments shows usage"
    output=$($SCRIPT_PATH 2>&1)
    if [[ "$output" == *"Usage: $0"* ]]; then
        echo "  PASS: Usage message displayed."
    else
        echo "  FAIL: Usage message not displayed. Output: $output"
        exit 1
    fi
}

test_invalid_directory_shows_usage() {
    echo "Running test: Invalid directory shows usage"
    output=$($SCRIPT_PATH /nonexistent/path 7 2>&1)
    if [[ "$output" == *"Error: Directory '/nonexistent/path' does not exist"* && "$output" == *"Usage: $0"* ]]; then
        echo "  PASS: Error and usage message displayed for invalid directory."
    else
        echo "  FAIL: Error/usage not displayed for invalid directory. Output: $output"
        exit 1
    fi
}

test_no_old_files_found() {
    echo "Running test: No old files found"
    MOCKED_FIND_OUTPUT="" # Mock rationale: Simulate no old files found by 'find'.
    output=$(echo "n" | $SCRIPT_PATH "$TEST_DIR" 1 2>&1) # Age 1 day, so only recent files exist
    if [[ "$output" == *"No digital dust bunnies found"* ]]; then
        echo "  PASS: Correctly reported no dust bunnies."
    else
        echo "  FAIL: Incorrect output for no dust bunnies. Output: $output"
        exit 1
    fi
    if [[ -n "$MOCKED_RM_CALLS" ]]; then
        echo "  FAIL: rm was called when no dust bunnies should be found. Calls: $MOCKED_RM_CALLS"
        exit 1
    fi
    MOCKED_RM_CALLS="" # Reset for next test
}

test_old_files_and_empty_dirs_identified_and_deleted_interactive() {
    echo "Running test: Old files and empty dirs identified and deleted (interactive)"
    
    # Mock rationale: Simulate 'find' output for old files and empty directories.
    # We need to ensure the script correctly identifies these specific paths for deletion.
    MOCKED_FIND_OUTPUT=$(printf "%s\0" \
        "$TEST_DIR/old_file1.log" \
        "$TEST_DIR/subdir1/old_file2.tmp" \
        "$TEST_DIR/subdir1/old_file3.cache" \
        "$TEST_DIR/empty_dir")

    # Simulate 'y' input for confirmation
    output=$(echo "y" | $SCRIPT_PATH "$TEST_DIR" 7 2>&1)

    if [[ "$output" == *"Found the following digital dust bunnies:"* && \
          "$output" == *"$TEST_DIR/old_file1.log"* && \
          "$output" == *"$TEST_DIR/subdir1/old_file2.tmp"* && \
          "$output" == *"$TEST_DIR/subdir1/old_file3.cache"* && \
          "$output" == *"$TEST_DIR/empty_dir"* && \
          "$output" == *"Sweeping away digital dust bunnies..."* && \
          "$output" == *"Digital dust bunnies successfully swept away!"* ]]; then
        echo "  PASS: Correctly identified and reported dust bunnies, and confirmed sweeping."
    else
        echo "  FAIL: Incorrect output for interactive deletion. Output: $output"
        exit 1
    fi

    # Verify rm was called with the correct files
    expected_rm_calls="rm -rf $TEST_DIR/old_file1.log $TEST_DIR/subdir1/old_file2.tmp $TEST_DIR/subdir1/old_file3.cache $TEST_DIR/empty_dir;"
    if [[ "$MOCKED_RM_CALLS" == *"$expected_rm_calls"* ]]; then
        echo "  PASS: rm was called with the expected dust bunnies."
    else
        echo "  FAIL: rm was NOT called with expected dust bunnies. Expected: '$expected_rm_calls', Actual: '$MOCKED_RM_CALLS'"
        exit 1
    fi
    MOCKED_RM_CALLS="" # Reset for next test
}

test_old_files_and_empty_dirs_identified_and_deleted_force() {
    echo "Running test: Old files and empty dirs identified and deleted (force)"
    
    # Mock rationale: Simulate 'find' output for old files and empty directories.
    # We need to ensure the script correctly identifies these specific paths for deletion.
    MOCKED_FIND_OUTPUT=$(printf "%s\0" \
        "$TEST_DIR/old_file1.log" \
        "$TEST_DIR/subdir1/old_file2.tmp" \
        "$TEST_DIR/subdir1/old_file3.cache" \
        "$TEST_DIR/empty_dir")

    output=$($SCRIPT_PATH "$TEST_DIR" 7 --force 2>&1)

    if [[ "$output" == *"Found the following digital dust bunnies:"* && \
          "$output" == *"$TEST_DIR/old_file1.log"* && \
          "$output" == *"$TEST_DIR/subdir1/old_file2.tmp"* && \
          "$output" == *"$TEST_DIR/subdir1/old_file3.cache"* && \
          "$output" == *"$TEST_DIR/empty_dir"* && \
          "$output" == *"Sweeping away digital dust bunnies..."* && \
          "$output" == *"Digital dust bunnies successfully swept away!"* ]]; then
        echo "  PASS: Correctly identified and reported dust bunnies, and force-swept."
    else
        echo "  FAIL: Incorrect output for force deletion. Output: $output"
        exit 1
    fi

    # Verify rm was called with the correct files
    expected_rm_calls="rm -rf $TEST_DIR/old_file1.log $TEST_DIR/subdir1/old_file2.tmp $TEST_DIR/subdir1/old_file3.cache $TEST_DIR/empty_dir;"
    if [[ "$MOCKED_RM_CALLS" == *"$expected_rm_calls"* ]]; then
        echo "  PASS: rm was called with the expected dust bunnies."
    else
        echo "  FAIL: rm was NOT called with expected dust bunnies. Expected: '$expected_rm_calls', Actual: '$MOCKED_RM_CALLS'"
        exit 1
    fi
    MOCKED_RM_CALLS="" # Reset for next test
}

test_old_files_and_empty_dirs_identified_but_not_deleted_interactive() {
    echo "Running test: Old files and empty dirs identified but not deleted (interactive 'n')"
    
    # Mock rationale: Simulate 'find' output for old files and empty directories.
    MOCKED_FIND_OUTPUT=$(printf "%s\0" \
        "$TEST_DIR/old_file1.log" \
        "$TEST_DIR/subdir1/old_file2.tmp")

    # Simulate 'n' input for confirmation
    output=$(echo "n" | $SCRIPT_PATH "$TEST_DIR" 7 2>&1)

    if [[ "$output" == *"Found the following digital dust bunnies:"* && \
          "$output" == *"$TEST_DIR/old_file1.log"* && \
          "$output" == *"$TEST_DIR/subdir1/old_file2.tmp"* && \
          "$output" == *"Digital dust bunnies spared."* ]]; then
        echo "  PASS: Correctly identified and reported, and confirmed sparing."
    else
        echo "  FAIL: Incorrect output for interactive sparing. Output: $output"
        exit 1
    fi

    # Verify rm was NOT called
    if [[ -n "$MOCKED_RM_CALLS" ]]; then
        echo "  FAIL: rm was called when it should not have been. Calls: $MOCKED_RM_CALLS"
        exit 1
    fi
    MOCKED_RM_CALLS="" # Reset for next test
}

test_invalid_age_defaults_to_7_days() {
    echo "Running test: Invalid age defaults to 7 days"
    
    # Mock rationale: Simulate 'find' output for files older than 7 days.
    # The script should use the default 7 days when an invalid age is provided.
    MOCKED_FIND_OUTPUT=$(printf "%s\0" \
        "$TEST_DIR/old_file1.log" \
        "$TEST_DIR/subdir1/old_file2.tmp")

    # Pass an invalid age (e.g., "abc")
    output=$(echo "y" | $SCRIPT_PATH "$TEST_DIR" "abc" 2>&1)

    if [[ "$output" == *"Invalid age 'abc'. Using default age of 7 days."* && \
          "$output" == *"Scanning '$TEST_DIR' for digital dust bunnies older than 7 days..."* && \
          "$output" == *"Digital dust bunnies successfully swept away!"* ]]; then
        echo "  PASS: Correctly warned about invalid age and used default."
    else
        echo "  FAIL: Did not handle invalid age correctly. Output: $output"
        exit 1
    fi
    # Verify rm was called with the correct files (based on 7 days)
    expected_rm_calls="rm -rf $TEST_DIR/old_file1.log $TEST_DIR/subdir1/old_file2.tmp;"
    if [[ "$MOCKED_RM_CALLS" == *"$expected_rm_calls"* ]]; then
        echo "  PASS: rm was called with the expected dust bunnies based on default age."
    else
        echo "  FAIL: rm was NOT called with expected dust bunnies based on default age. Expected: '$expected_rm_calls', Actual: '$MOCKED_RM_CALLS'"
        exit 1
    fi
    MOCKED_RM_CALLS="" # Reset for next test
}

test_force_flag_as_second_arg() {
    echo "Running test: --force flag as second argument"
    
    MOCKED_FIND_OUTPUT=$(printf "%s\0" \
        "$TEST_DIR/old_file1.log")

    output=$($SCRIPT_PATH "$TEST_DIR" --force 2>&1)

    if [[ "$output" == *"Scanning '$TEST_DIR' for digital dust bunnies older than 7 days..."* && \
          "$output" == *"Digital dust bunnies successfully swept away!"* ]]; then
        echo "  PASS: --force flag handled correctly as second argument, default age used."
    else
        echo "  FAIL: --force flag as second argument failed. Output: $output"
        exit 1
    fi
    expected_rm_calls="rm -rf $TEST_DIR/old_file1.log;"
    if [[ "$MOCKED_RM_CALLS" == *"$expected_rm_calls"* ]]; then
        echo "  PASS: rm was called with the expected dust bunnies."
    else
        echo "  FAIL: rm was NOT called with expected dust bunnies. Expected: '$expected_rm_calls', Actual: '$MOCKED_RM_CALLS'"
        exit 1
    fi
    MOCKED_RM_CALLS="" # Reset for next test
}


# --- Main Test Runner ---
main() {
    echo "Starting Nightly Digital Dust Bunny Sweeper Test Suite..."
    
    # Override `find` and `rm` with mock functions
    # Mock rationale: This is crucial for deterministic and offline testing.
    # It prevents actual file system changes and allows us to control the output of 'find'
    # and capture calls to 'rm'.
    eval "find() { mock_find \"\$@\"; }"
    eval "rm() { mock_rm \"\$@\"; }"

    setup_test_env

    test_no_arguments_shows_usage
    test_invalid_directory_shows_usage
    test_no_old_files_found
    test_old_files_and_empty_dirs_identified_and_deleted_interactive
    test_old_files_and_empty_dirs_identified_and_deleted_force
    test_old_files_and_empty_dirs_identified_but_not_deleted_interactive
    test_invalid_age_defaults_to_7_days
    test_force_flag_as_second_arg

    cleanup_test_env
    
    # Restore original commands
    unset -f rm
    unset -f find
    eval "rm() { $ORIG_RM \"\$@\"; }"
    eval "find() { $ORIG_FIND \"\$@\"; }"

    echo "All tests completed."
}

main
