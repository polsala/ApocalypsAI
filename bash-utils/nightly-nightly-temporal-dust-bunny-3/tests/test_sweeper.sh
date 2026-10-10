#!/bin/bash

# Mock rationale:
# We are testing a shell script that interacts with the filesystem and `find` command.
# Instead of mocking `find` directly, we create temporary files and directories with
# specific modification times using `touch -t`. This allows us to test the script's
# logic with actual filesystem operations, which is more robust for a bash utility.
# The `rm -rf` and `mv` commands are also tested directly.
# The `SWEEPER_LOG` is redirected to a temporary file for each test to ensure isolation.

# Set -e to exit immediately if a command exits with a non-zero status.
set -e

# Define the path to the script
SCRIPT_PATH="./src/temporal_dust_bunny_sweeper.sh"

# Temporary directory for tests
TEST_DIR="/tmp/test_temporal_sweeper_$$"
ARCHIVE_TEST_DIR="/tmp/test_temporal_archive_$$"
TEST_LOG="/tmp/test_sweeper_log_$$"

# Override SWEEPER_LOG for tests
export SWEEPER_LOG="$TEST_LOG"

# --- Helper Functions ---

setup_test_environment() {
    rm -rf "$TEST_DIR" "$ARCHIVE_TEST_DIR" "$TEST_LOG"
    mkdir -p "$TEST_DIR/old_files" "$TEST_DIR/recent_files" "$TEST_DIR/old_dirs/subdir"
    mkdir -p "$ARCHIVE_TEST_DIR"
    touch "$TEST_LOG"

    # Create old files/dirs (e.g., 100 days ago)
    # Format for touch -t: YYYYMMDDhhmm
    OLD_DATE=""
    if date -v -100d '+%Y%m%d%H%M' &>/dev/null; then
        # macOS/BSD date
        OLD_DATE=$(date -v -100d '+%Y%m%d%H%M')
    else
        # GNU date (Linux)
        OLD_DATE=$(date --date="100 days ago" '+%Y%m%d%H%M')
    fi

    touch -t "$OLD_DATE" "$TEST_DIR/old_files/file1.txt"
    touch -t "$OLD_DATE" "$TEST_DIR/old_files/file2.log"
    touch -t "$OLD_DATE" "$TEST_DIR/old_dirs/old_dir1" # Directory mtime
    touch -t "$OLD_DATE" "$TEST_DIR/old_dirs/subdir/old_file_in_subdir.txt"

    # Create recent files/dirs (e.g., 1 day ago)
    RECENT_DATE=""
    if date -v -1d '+%Y%m%d%H%M' &>/dev/null; then
        # macOS/BSD date
        RECENT_DATE=$(date -v -1d '+%Y%m%d%H%M')
    else
        # GNU date (Linux)
        RECENT_DATE=$(date --date="1 day ago" '+%Y%m%d%H%M')
    fi
    touch -t "$RECENT_DATE" "$TEST_DIR/recent_files/recent_file1.txt"
    mkdir -p "$TEST_DIR/recent_dirs/recent_dir1"
    touch -t "$RECENT_DATE" "$TEST_DIR/recent_dirs/recent_dir1" # Update dir mtime
}

cleanup_test_environment() {
    rm -rf "$TEST_DIR" "$ARCHIVE_TEST_DIR" "$TEST_LOG"
}

assert_contains() {
    local expected="$1"
    local actual="$2"
    if ! grep -qF "$expected" <<< "$actual"; then
        echo "FAIL: Expected '$actual' to contain '$expected'"
        exit 1
    fi
}

assert_not_contains() {
    local expected="$1"
    local actual="$2"
    if grep -qF "$expected" <<< "$actual"; then
        echo "FAIL: Expected '$actual' NOT to contain '$expected'"
        exit 1
    fi
}

assert_file_exists() {
    local file="$1"
    if [[ ! -e "$file" ]]; then
        echo "FAIL: Expected file to exist: $file"
        exit 1
    fi
}

assert_file_not_exists() {
    local file="$1"
    if [[ -e "$file" ]]; then
        echo "FAIL: Expected file NOT to exist: $file"
        exit 1
    fi
}

# --- Test Cases ---

test_dry_run_finds_old_files() {
    echo "Running test: dry_run_finds_old_files"
    setup_test_environment

    OUTPUT=$("$SCRIPT_PATH" --age 90 --dry-run "$TEST_DIR" 2>&1)

    assert_contains "Found: $TEST_DIR/old_files/file1.txt" "$OUTPUT"
    assert_contains "Found: $TEST_DIR/old_files/file2.log" "$OUTPUT"
    assert_contains "Found: $TEST_DIR/old_dirs/old_dir1" "$OUTPUT"
    assert_contains "Found: $TEST_DIR/old_dirs/subdir/old_file_in_subdir.txt" "$OUTPUT"
    assert_not_contains "Found: $TEST_DIR/recent_files/recent_file1.txt" "$OUTPUT"
    assert_contains "This was a dry run. No temporal matter was disturbed." "$OUTPUT"
    assert_contains "Ancient temporal dust bunnies detected:" "$OUTPUT"
    assert_not_contains "No dust bunnies found." "$OUTPUT"

    assert_file_exists "$TEST_DIR/old_files/file1.txt" # Should still exist in dry run
    assert_file_exists "$TEST_LOG"
    assert_contains "Initiating Temporal Dust Bunny Scan" "$(cat "$TEST_LOG")"
    assert_contains "Temporal sweep complete." "$(cat "$TEST_LOG")"

    cleanup_test_environment
    echo "Test passed: dry_run_finds_old_files"
}

test_dry_run_no_old_files() {
    echo "Running test: dry_run_no_old_files"
    setup_test_environment

    OUTPUT=$("$SCRIPT_PATH" --age 5 --dry-run "$TEST_DIR" 2>&1) # Age 5 days, recent files are 1 day old

    assert_not_contains "Found: $TEST_DIR/old_files/file1.txt" "$OUTPUT"
    assert_not_contains "Found: $TEST_DIR/recent_files/recent_file1.txt" "$OUTPUT"
    assert_contains "The temporal realms are surprisingly pristine. No dust bunnies found." "$OUTPUT"
    assert_contains "This was a dry run. No temporal matter was disturbed." "$OUTPUT"

    cleanup_test_environment
    echo "Test passed: dry_run_no_old_files"
}

test_sweep_deletes_old_files() {
    echo "Running test: sweep_deletes_old_files"
    setup_test_environment

    OUTPUT=$("$SCRIPT_PATH" --age 90 --sweep "$TEST_DIR" 2>&1)

    assert_contains "Sweeping: $TEST_DIR/old_files/file1.txt" "$OUTPUT"
    assert_contains "Sweeping: $TEST_DIR/old_files/file2.log" "$OUTPUT"
    assert_contains "Sweeping: $TEST_DIR/old_dirs/old_dir1" "$OUTPUT"
    assert_not_contains "Sweeping: $TEST_DIR/recent_files/recent_file1.txt" "$OUTPUT"
    assert_contains "Temporal sweep complete. The realms are a bit tidier now." "$OUTPUT"

    assert_file_not_exists "$TEST_DIR/old_files/file1.txt"
    assert_file_not_exists "$TEST_DIR/old_files/file2.log"
    assert_file_not_exists "$TEST_DIR/old_dirs/old_dir1" # Entire directory should be gone
    assert_file_exists "$TEST_DIR/recent_files/recent_file1.txt" # Should still exist

    assert_contains "Swept: $TEST_DIR/old_files/file1.txt" "$(cat "$TEST_LOG")"
    assert_contains "Swept: $TEST_DIR/old_dirs/old_dir1" "$(cat "$TEST_LOG")"

    cleanup_test_environment
    echo "Test passed: sweep_deletes_old_files"
}

test_archive_moves_old_files() {
    echo "Running test: archive_moves_old_files"
    setup_test_environment

    OUTPUT=$("$SCRIPT_PATH" --age 90 --archive "$ARCHIVE_TEST_DIR" "$TEST_DIR" 2>&1)

    assert_contains "Archiving: $TEST_DIR/old_files/file1.txt to $ARCHIVE_TEST_DIR" "$OUTPUT"
    assert_contains "Archiving: $TEST_DIR/old_dirs/old_dir1 to $ARCHIVE_TEST_DIR" "$OUTPUT"
    assert_not_contains "Archiving: $TEST_DIR/recent_files/recent_file1.txt" "$OUTPUT"
    assert_contains "Temporal sweep complete. The realms are a bit tidier now." "$OUTPUT"

    assert_file_not_exists "$TEST_DIR/old_files/file1.txt"
    assert_file_exists "$ARCHIVE_TEST_DIR/file1.txt"
    assert_file_not_exists "$TEST_DIR/old_dirs/old_dir1"
    assert_file_exists "$ARCHIVE_TEST_DIR/old_dir1" # Directory should be moved
    assert_file_exists "$TEST_DIR/recent_files/recent_file1.txt" # Should still exist

    assert_contains "Archived: $TEST_DIR/old_files/file1.txt to $ARCHIVE_TEST_DIR" "$(cat "$TEST_LOG")"
    assert_contains "Archived: $TEST_DIR/old_dirs/old_dir1 to $ARCHIVE_TEST_DIR" "$(cat "$TEST_LOG")"

    cleanup_test_environment
    echo "Test passed: archive_moves_old_files"
}

test_archive_dir_creation() {
    echo "Running test: archive_dir_creation"
    setup_test_environment
    local NEW_ARCHIVE_DIR="/tmp/non_existent_archive_$$"
    rm -rf "$NEW_ARCHIVE_DIR" # Ensure it doesn't exist

    OUTPUT=$("$SCRIPT_PATH" --age 90 --archive "$NEW_ARCHIVE_DIR" "$TEST_DIR" 2>&1)

    assert_contains "Creating temporal archive realm: $NEW_ARCHIVE_DIR" "$OUTPUT"
    assert_file_exists "$NEW_ARCHIVE_DIR"

    rm -rf "$NEW_ARCHIVE_DIR" # Clean up
    cleanup_test_environment
    echo "Test passed: archive_dir_creation"
}

test_invalid_options() {
    echo "Running test: invalid_options"
    setup_test_environment

    # Test missing directory
    OUTPUT=$("$SCRIPT_PATH" --age 90 --dry-run 2>&1 || true)
    assert_contains "No target directories specified." "$OUTPUT"

    # Test sweep and archive together
    OUTPUT=$("$SCRIPT_PATH" --age 90 --sweep --archive "$ARCHIVE_TEST_DIR" "$TEST_DIR" 2>&1 || true)
    assert_contains "Cannot use --sweep and --archive simultaneously. Choose one." "$OUTPUT"

    # Test unknown option
    OUTPUT=$("$SCRIPT_PATH" --invalid-option "$TEST_DIR" 2>&1 || true)
    assert_contains "Unknown option: --invalid-option" "$OUTPUT"

    cleanup_test_environment
    echo "Test passed: invalid_options"
}

test_non_existent_target_dir() {
    echo "Running test: non_existent_target_dir"
    setup_test_environment
    local NON_EXISTENT_DIR="/tmp/i_dont_exist_$$"

    OUTPUT=$("$SCRIPT_PATH" --age 90 --dry-run "$NON_EXISTENT_DIR" "$TEST_DIR" 2>&1)

    assert_contains "Warning: Directory not found, skipping: $NON_EXISTENT_DIR" "$OUTPUT"
    assert_contains "Found: $TEST_DIR/old_files/file1.txt" "$OUTPUT" # Still processes valid dir

    cleanup_test_environment
    echo "Test passed: non_existent_target_dir"
}

# --- Run all tests ---
echo "--- Starting all tests for Nightly Temporal Dust Bunny Sweeper ---"
test_dry_run_finds_old_files
test_dry_run_no_old_files
test_sweep_deletes_old_files
test_archive_moves_old_files
test_archive_dir_creation
test_invalid_options
test_non_existent_target_dir
echo "--- All tests completed successfully! ---"

cleanup_test_environment
