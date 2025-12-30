#!/bin/bash

# Test suite for Nightly Cosmic Dust Collector

# Source the main script to test its functions
# We will override critical commands before sourcing to mock them.

# --- Test Setup ---
TEST_DIR=$(mktemp -d)
MOCK_FIND_OUTPUT=""
MOCK_DU_SIZE=1024 # Default mock size for files
MOCK_RM_SUCCESS=0 # Default mock success for rm
MOCK_RMDIR_SUCCESS=0 # Default mock success for rmdir

# Mock rationale: Prevent actual file system changes and control 'find' output.
find() {
    echo "$MOCK_FIND_OUTPUT"
    return 0
}

# Mock rationale: Prevent actual file system access and return a controlled size.
du() {
    echo "$MOCK_DU_SIZE\t$1"
    return 0
}

# Mock rationale: Prevent actual file deletion and control exit status.
rm() {
    if [[ "$MOCK_RM_SUCCESS" -ne 0 ]]; then
        return 1
    fi
    return 0
}

# Mock rationale: Prevent actual directory deletion and control exit status.
rmdir() {
    if [[ "$MOCK_RMDIR_SUCCESS" -ne 0 ]]; then
        return 1
    fi
    return 0
}

# Override date for deterministic logging
# Mock rationale: Ensure consistent timestamps in logs for comparison.
date() {
    echo "2023-10-27 10:00:00"
}

# Override HOME for deterministic path resolution
# Mock rationale: Ensure HOME path is predictable for tests.
HOME="$TEST_DIR/mock_home"
mkdir -p "$HOME"

# Source the script after mocks are defined
# This allows the script to use our mocked functions.
. src/cosmic_dust_collector.sh

# Reset mocks and cleanup after each test
reset_mocks() {
    MOCK_FIND_OUTPUT=""
    MOCK_DU_SIZE=1024
    MOCK_RM_SUCCESS=0
    MOCK_RMDIR_SUCCESS=0
    TOTAL_DUST_COLLECTED_BYTES=0 # Reset internal script variable
    # Clear CLEANUP_PATHS to prevent accidental real system scans
    CLEANUP_PATHS=("$TEST_DIR/mock_path")
    OLD_FILES_DAYS=7 # Reset to default
}

cleanup() {
    rm -rf "$TEST_DIR"
}

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

run_test() {
    local test_name="$1"
    local func_to_test="$2"
    shift 2
    echo "Running test: $test_name"
    reset_mocks
    "$func_to_test" "$@"
    if [[ $? -eq 0 ]]; then
        echo "PASS: $test_name"
    else
        echo "FAIL: $test_name"
        exit 1
    fi
}

# --- Test Cases ---

test_dry_run_no_dust() {
    MOCK_FIND_OUTPUT="" # No files found
    mkdir -p "$TEST_DIR/mock_path"
    local output=$(main -d 2>&1)
    assert_contains "Scanning '$TEST_DIR/mock_path' for cosmic dust older than 7 days..." "$output"
    assert_contains "No ancient cosmic dust found in '$TEST_DIR/mock_path'." "$output"
    assert_contains "Total cosmic dust identified: 0.0B" "$output"
    assert_contains "DRY RUN MODE ACTIVE" "$output"
    assert_contains "This was a DRY RUN. No actual dust was removed." "$output"
    assert_not_contains "Would remove" "$output"
    assert_not_contains "Removing ancient cosmic dust" "$output"
}

test_dry_run_with_dust() {
    MOCK_FIND_OUTPUT="$TEST_DIR/mock_path/old_log.log\n$TEST_DIR/mock_path/temp_file.tmp"
    MOCK_DU_SIZE=5120 # 5KB
    mkdir -p "$TEST_DIR/mock_path"
    local output=$(main -d 2>&1)
    assert_contains "Scanning '$TEST_DIR/mock_path' for cosmic dust older than 7 days..." "$output"
    assert_contains "DRY RUN: Would remove ancient cosmic dust: '$TEST_DIR/mock_path/old_log.log' (Size: 5.0KiB)" "$output"
    assert_contains "DRY RUN: Would remove ancient cosmic dust: '$TEST_DIR/mock_path/temp_file.tmp' (Size: 5.0KiB)" "$output"
    assert_contains "Total cosmic dust identified: 10.0KiB" "$output"
    assert_contains "DRY RUN MODE ACTIVE" "$output"
    assert_contains "This was a DRY RUN. No actual dust was removed." "$output"
    assert_not_contains "Removing ancient cosmic dust" "$output" # Ensure actual removal message is not present
}

test_actual_run_with_dust() {
    MOCK_FIND_OUTPUT="$TEST_DIR/mock_path/old_log.log\n$TEST_DIR/mock_path/temp_file.tmp"
    MOCK_DU_SIZE=2048 # 2KB
    mkdir -p "$TEST_DIR/mock_path"
    local output=$(main 2>&1)
    assert_contains "Scanning '$TEST_DIR/mock_path' for cosmic dust older than 7 days..." "$output"
    assert_contains "Removing ancient cosmic dust: '$TEST_DIR/mock_path/old_log.log' (Size: 2.0KiB)" "$output"
    assert_contains "Removing ancient cosmic dust: '$TEST_DIR/mock_path/temp_file.tmp' (Size: 2.0KiB)" "$output"
    assert_contains "Total cosmic dust identified: 4.0KiB" "$output"
    assert_not_contains "DRY RUN MODE ACTIVE" "$output"
    assert_not_contains "This was a DRY RUN." "$output"
    assert_not_contains "Would remove" "$output" # Ensure dry run message is not present
}

test_verbose_output() {
    MOCK_FIND_OUTPUT="$TEST_DIR/mock_path/old_log.log"
    MOCK_DU_SIZE=100
    mkdir -p "$TEST_DIR/mock_path"
    local output=$(main -v 2>&1)
    assert_contains "[INFO] Scanning '$TEST_DIR/mock_path' for cosmic dust older than 7 days..." "$output"
    assert_contains "[INFO] Removing ancient cosmic dust: '$TEST_DIR/mock_path/old_log.log' (Size: 100.0B)" "$output"
    assert_contains "[INFO] Nightly Cosmic Dust Collection complete!" "$output"
}

test_path_does_not_exist() {
    CLEANUP_PATHS=("/non/existent/path") # Override for this test
    local output=$(main 2>&1)
    assert_contains "[WARN] Cleanup path '/non/existent/path' does not exist or is not a directory. Skipping." "$output"
    assert_contains "Total cosmic dust identified: 0.0B" "$output"
}

test_empty_directory_removal() {
    MOCK_FIND_OUTPUT="$TEST_DIR/mock_path/old_file.log\n$TEST_DIR/mock_path/empty_dir" # Mock find returns a file and an empty dir
    # Mock find for empty directories specifically
    find() {
        if [[ "$@" == *"-type d -empty"* ]]; then
            echo "$TEST_DIR/mock_path/empty_dir"
        else
            echo "$TEST_DIR/mock_path/old_file.log"
        fi
    }
    mkdir -p "$TEST_DIR/mock_path/empty_dir" # Ensure the mock path exists for the script's check
    local output=$(main 2>&1)
    assert_contains "Removing empty cosmic void: '$TEST_DIR/mock_path/empty_dir'" "$output"
    assert_contains "Removing ancient cosmic dust: '$TEST_DIR/mock_path/old_file.log'" "$output"
}

test_rm_failure() {
    MOCK_FIND_OUTPUT="$TEST_DIR/mock_path/old_log.log"
    MOCK_RM_SUCCESS=1 # Simulate rm failure
    mkdir -p "$TEST_DIR/mock_path"
    local output=$(main 2>&1)
    assert_contains "Failed to remove '$TEST_DIR/mock_path/old_log.log'." "$output"
    assert_contains "Total cosmic dust identified: 1.0KiB" "$output" # Size should still be counted
}

test_rmdir_failure() {
    MOCK_FIND_OUTPUT="$TEST_DIR/mock_path/empty_dir" # Mock find returns an empty dir
    find() {
        if [[ "$@" == *"-type d -empty"* ]]; then
            echo "$TEST_DIR/mock_path/empty_dir"
        else
            echo ""
        fi
    }
    MOCK_RMDIR_SUCCESS=1 # Simulate rmdir failure
    mkdir -p "$TEST_DIR/mock_path/empty_dir"
    local output=$(main 2>&1)
    assert_contains "Failed to remove empty directory '$TEST_DIR/mock_path/empty_dir'." "$output"
    assert_contains "Total cosmic dust identified: 0.0B" "$output"
}


# --- Run all tests ---
run_test "Dry run with no dust" test_dry_run_no_dust
run_test "Dry run with dust" test_dry_run_with_dust
run_test "Actual run with dust" test_actual_run_with_dust
run_test "Verbose output" test_verbose_output
run_test "Non-existent path handling" test_path_does_not_exist
run_test "Empty directory removal" test_empty_directory_removal
run_test "File removal failure handling" test_rm_failure
run_test "Empty directory removal failure handling" test_rmdir_failure

cleanup
echo "All tests passed!"
exit 0
