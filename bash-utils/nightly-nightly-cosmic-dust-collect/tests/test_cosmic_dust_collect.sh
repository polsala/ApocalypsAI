#!/bin/bash

# Automated tests for Nightly Cosmic Dust Collector

set -euo pipefail

SCRIPT_PATH="$(dirname "$0")"/../src/cosmic_dust_collect.sh

# --- Test Helper Functions --- #
setup_test_env() {
    TEST_DIR=$(mktemp -d)
    ARCHIVE_TEST_DIR=$(mktemp -d)
    echo "Test environment setup: TEST_DIR=$TEST_DIR, ARCHIVE_TEST_DIR=$ARCHIVE_TEST_DIR"
}

cleanup_test_env() {
    if [[ -d "$TEST_DIR" ]]; then
        rm -rf "$TEST_DIR"
        echo "Cleaned up $TEST_DIR"
    fi
    if [[ -d "$ARCHIVE_TEST_DIR" ]]; then
        rm -rf "$ARCHIVE_TEST_DIR"
        echo "Cleaned up $ARCHIVE_TEST_DIR"
    fi
}

create_file() {
    local path="$1"
    local content="$2"
    local mtime_offset_days="$3"
    echo -n "$content" > "$path"
    if [[ -n "$mtime_offset_days" ]]; then
        # Mock rationale: Using 'touch -d' to set modification times deterministically.
        # This simulates files of different ages without relying on real-time passage.
        touch -d "$(date -d "-$mtime_offset_days days" +%Y-%m-%d)" "$path"
    fi
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

assert_file_exists() {
    local path="$1"
    if [[ ! -f "$path" ]]; then
        echo "FAIL: Expected file to exist: $path"
        exit 1
    fi
}

assert_file_not_exists() {
    local path="$1"
    if [[ -f "$path" ]]; then
        echo "FAIL: Expected file NOT to exist: $path"
        exit 1
    fi
}

assert_dir_empty() {
    local path="$1"
    if [[ $(find "$path" -maxdepth 1 -type f | wc -l) -ne 0 ]]; then
        echo "FAIL: Expected directory '$path' to be empty of files."
        exit 1
    fi
}

# --- Test Cases --- #

# Test 1: Dry run - default age (30 days)
test_dry_run_default_age() {
    echo "Running Test 1: Dry run - default age (30 days)"
    setup_test_env

    create_file "$TEST_DIR/old_file_1.txt" "content" 31
    create_file "$TEST_DIR/old_file_2.log" "content" 35
    create_file "$TEST_DIR/recent_file.txt" "content" 10
    create_file "$TEST_DIR/empty_file.txt" "" 40

    OUTPUT=$(bash "$SCRIPT_PATH" "$TEST_DIR")

    assert_contains "$OUTPUT" "Found 3 files matching criteria"
    assert_contains "$OUTPUT" "$TEST_DIR/old_file_1.txt"
    assert_contains "$OUTPUT" "$TEST_DIR/old_file_2.log"
    assert_contains "$OUTPUT" "$TEST_DIR/empty_file.txt"
    assert_not_contains "$OUTPUT" "$TEST_DIR/recent_file.txt"
    assert_contains "$OUTPUT" "--- DRY RUN: Files that would be processed ---"
    assert_file_exists "$TEST_DIR/old_file_1.txt"
    assert_file_exists "$TEST_DIR/recent_file.txt"

    cleanup_test_env
    echo "Test 1 Passed."
}

# Test 2: Dry run - specific age
test_dry_run_specific_age() {
    echo "Running Test 2: Dry run - specific age"
    setup_test_env

    create_file "$TEST_DIR/old_file_1.txt" "content" 61
    create_file "$TEST_DIR/old_file_2.log" "content" 65
    create_file "$TEST_DIR/recent_file.txt" "content" 50

    OUTPUT=$(bash "$SCRIPT_PATH" --age 60 "$TEST_DIR")

    assert_contains "$OUTPUT" "Found 2 files matching criteria"
    assert_contains "$OUTPUT" "$TEST_DIR/old_file_1.txt"
    assert_contains "$OUTPUT" "$TEST_DIR/old_file_2.log"
    assert_not_contains "$OUTPUT" "$TEST_DIR/recent_file.txt"

    cleanup_test_env
    echo "Test 2 Passed."
}

# Test 3: Dry run - empty files only
test_dry_run_empty_files() {
    echo "Running Test 3: Dry run - empty files only"
    setup_test_env

    create_file "$TEST_DIR/empty_file_1.txt" "" 10
    create_file "$TEST_DIR/empty_file_2.log" "" 50
    create_file "$TEST_DIR/non_empty_file.txt" "content" 10

    OUTPUT=$(bash "$SCRIPT_PATH" --empty "$TEST_DIR")

    assert_contains "$OUTPUT" "Found 2 files matching criteria"
    assert_contains "$OUTPUT" "$TEST_DIR/empty_file_1.txt"
    assert_contains "$OUTPUT" "$TEST_DIR/empty_file_2.log"
    assert_not_contains "$OUTPUT" "$TEST_DIR/non_empty_file.txt"

    cleanup_test_env
    echo "Test 3 Passed."
}

# Test 4: Delete files
test_delete_files() {
    echo "Running Test 4: Delete files"
    setup_test_env

    create_file "$TEST_DIR/file_to_delete_1.txt" "content" 31
    create_file "$TEST_DIR/file_to_delete_2.log" "content" 35
    create_file "$TEST_DIR/file_to_keep.txt" "content" 10

    OUTPUT=$(bash "$SCRIPT_PATH" --delete "$TEST_DIR")

    assert_contains "$OUTPUT" "Deleting 2 files..."
    assert_contains "$OUTPUT" "Files deleted successfully."
    assert_file_not_exists "$TEST_DIR/file_to_delete_1.txt"
    assert_file_not_exists "$TEST_DIR/file_to_delete_2.log"
    assert_file_exists "$TEST_DIR/file_to_keep.txt"

    cleanup_test_env
    echo "Test 4 Passed."
}

# Test 5: Archive files
test_archive_files() {
    echo "Running Test 5: Archive files"
    setup_test_env

    create_file "$TEST_DIR/file_to_archive_1.txt" "content" 31
    create_file "$TEST_DIR/file_to_archive_2.log" "content" 35
    create_file "$TEST_DIR/file_to_keep.txt" "content" 10

    OUTPUT=$(bash "$SCRIPT_PATH" --archive "$ARCHIVE_TEST_DIR" "$TEST_DIR")

    assert_contains "$OUTPUT" "Archiving 2 files to"
    assert_contains "$OUTPUT" "Archive created successfully. Deleting original files..."
    assert_contains "$OUTPUT" "Original files deleted successfully."
    assert_file_not_exists "$TEST_DIR/file_to_archive_1.txt"
    assert_file_not_exists "$TEST_DIR/file_to_archive_2.log"
    assert_file_exists "$TEST_DIR/file_to_keep.txt"
    
    # Check if an archive file was created in ARCHIVE_TEST_DIR
    ARCHIVE_COUNT=$(find "$ARCHIVE_TEST_DIR" -maxdepth 1 -type f -name "cosmic_dust_*.tar.gz" | wc -l)
    if [[ "$ARCHIVE_COUNT" -ne 1 ]]; then
        echo "FAIL: Expected 1 archive file, found $ARCHIVE_COUNT" >&2
        exit 1
    fi

    cleanup_test_env
    echo "Test 5 Passed."
}

# Test 6: No files found
test_no_files_found() {
    echo "Running Test 6: No files found"
    setup_test_env

    create_file "$TEST_DIR/recent_file.txt" "content" 10

    OUTPUT=$(bash "$SCRIPT_PATH" --age 30 "$TEST_DIR")

    assert_contains "$OUTPUT" "No cosmic dust found in '$TEST_DIR' matching criteria."
    assert_file_exists "$TEST_DIR/recent_file.txt"

    cleanup_test_env
    echo "Test 6 Passed."
}

# Test 7: Invalid directory
test_invalid_directory() {
    echo "Running Test 7: Invalid directory"
    setup_test_env

    OUTPUT=$(bash "$SCRIPT_PATH" /non/existent/path 2>&1 || true)

    assert_contains "$OUTPUT" "Error: Target directory '/non/existent/path' does not exist or is not a directory."

    cleanup_test_env
    echo "Test 7 Passed."
}

# Test 8: Archive directory does not exist
test_archive_dir_not_exist() {
    echo "Running Test 8: Archive directory does not exist"
    setup_test_env

    create_file "$TEST_DIR/old_file.txt" "content" 31

    OUTPUT=$(bash "$SCRIPT_PATH" --archive /non/existent/archive/dir "$TEST_DIR" 2>&1 || true)

    assert_contains "$OUTPUT" "Error: Archive directory '/non/existent/archive/dir' does not exist or is not a directory."

    cleanup_test_env
    echo "Test 8 Passed."
}

# Test 9: Cannot use --archive and --delete together
test_archive_and_delete_conflict() {
    echo "Running Test 9: Cannot use --archive and --delete together"
    setup_test_env

    create_file "$TEST_DIR/old_file.txt" "content" 31

    OUTPUT=$(bash "$SCRIPT_PATH" --archive "$ARCHIVE_TEST_DIR" --delete "$TEST_DIR" 2>&1 || true)

    assert_contains "$OUTPUT" "Error: Cannot use --archive and --delete simultaneously."

    cleanup_test_env
    echo "Test 9 Passed."
}

# Test 10: Empty files with specific age
test_empty_files_with_age() {
    echo "Running Test 10: Empty files with specific age"
    setup_test_env

    create_file "$TEST_DIR/empty_old.txt" "" 40
    create_file "$TEST_DIR/empty_recent.txt" "" 10
    create_file "$TEST_DIR/full_old.txt" "content" 40

    OUTPUT=$(bash "$SCRIPT_PATH" --age 30 --empty "$TEST_DIR")

    assert_contains "$OUTPUT" "Found 1 files matching criteria"
    assert_contains "$OUTPUT" "$TEST_DIR/empty_old.txt"
    assert_not_contains "$OUTPUT" "$TEST_DIR/empty_recent.txt"
    assert_not_contains "$OUTPUT" "$TEST_DIR/full_old.txt"

    cleanup_test_env
    echo "Test 10 Passed."
}

# Test 11: No arguments (should show help/error)
test_no_arguments() {
    echo "Running Test 11: No arguments"
    OUTPUT=$(bash "$SCRIPT_PATH" 2>&1 || true)
    assert_contains "$OUTPUT" "Error: No target directory specified."
    echo "Test 11 Passed."
}

# Test 12: Argument parsing for --age without value
test_age_no_value() {
    echo "Running Test 12: --age without value"
    setup_test_env
    OUTPUT=$(bash "$SCRIPT_PATH" --age "$TEST_DIR" 2>&1 || true)
    assert_contains "$OUTPUT" "Error: --age requires a number of days."
    cleanup_test_env
    echo "Test 12 Passed."
}

# Test 13: Argument parsing for --archive without value
test_archive_no_value() {
    echo "Running Test 13: --archive without value"
    setup_test_env
    OUTPUT=$(bash "$SCRIPT_PATH" --archive "$TEST_DIR" 2>&1 || true)
    assert_contains "$OUTPUT" "Error: --archive requires an archive directory."
    cleanup_test_env
    echo "Test 13 Passed."
}

# --- Run all tests --- #
echo "Running all tests for Nightly Cosmic Dust Collector..."

test_dry_run_default_age
test_dry_run_specific_age
test_dry_run_empty_files
test_delete_files
test_archive_files
test_no_files_found
test_invalid_directory
test_archive_dir_not_exist
test_archive_and_delete_conflict
test_empty_files_with_age
test_no_arguments
test_age_no_value
test_archive_no_value

echo "All tests completed successfully!"
