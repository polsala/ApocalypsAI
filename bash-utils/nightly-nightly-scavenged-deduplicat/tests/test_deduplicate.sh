#!/bin/bash

# Mock rationale:
# The tests create temporary files with known content and structure within an isolated test directory.
# The actual `sha256sum` (or `md5sum`) and `rm` commands are used, so no direct mocking of these system commands is needed.
# The effects of `rm` are confined to the temporary directory, ensuring deterministic and offline execution without affecting the host system.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
DEDUPLICATE_SCRIPT="$SCRIPT_DIR/deduplicate.sh"

# Function to create a temporary directory and clean it up on exit
setup_test_env() {
    TEST_DIR=$(mktemp -d -t deduplicator-test-XXXXXXXX)
    echo "Created test directory: $TEST_DIR"
    cd "$TEST_DIR"
}

cleanup_test_env() {
    echo "Cleaning up test directory: $TEST_DIR"
    rm -rf "$TEST_DIR"
}

# Test case 1: Dry run with no duplicates
test_no_duplicates_dry_run() {
    echo "\n--- Running test: No duplicates (dry run) ---"
    setup_test_env

    mkdir -p dir1 dir2
    echo "unique content 1" > dir1/file1.txt
    echo "unique content 2" > dir2/file2.log

    OUTPUT=$("$DEDUPLICATE_SCRIPT" --dry-run dir1 dir2 2>&1)
    echo "$OUTPUT"

    if echo "$OUTPUT" | grep -q "No duplicate files found"; then
        echo "PASS: No duplicates (dry run) - Correctly reported no duplicates."
    else
        echo "FAIL: No duplicates (dry run) - Expected 'No duplicate files found', got:\n$OUTPUT"
        exit 1
    fi

    cleanup_test_env
}

# Test case 2: Dry run with duplicates
test_duplicates_dry_run() {
    echo "\n--- Running test: Duplicates (dry run) ---"
    setup_test_env

    mkdir -p dirA dirB
    echo "duplicate content" > dirA/file_a.txt
    echo "duplicate content" > dirB/file_b.txt
    echo "unique content" > dirA/unique.txt

    OUTPUT=$("$DEDUPLICATE_SCRIPT" --dry-run dirA dirB 2>&1)
    echo "$OUTPUT"

    if echo "$OUTPUT" | grep -q "Duplicate files found" && \
       echo "$OUTPUT" | grep -q "Group with hash" && \
       echo "$OUTPUT" | grep -q "Keeping: $TEST_DIR/dirA/file_a.txt (Original)" && \
       echo "$OUTPUT" | grep -q "Duplicate: $TEST_DIR/dirB/file_b.txt" && \
       echo "$OUTPUT" | grep -q "(Dry run: would purge $TEST_DIR/dirB/file_b.txt)"; then
        echo "PASS: Duplicates (dry run) - Correctly identified duplicates and showed dry run message."
    else
        echo "FAIL: Duplicates (dry run) - Expected duplicate identification and dry run message, got:\n$OUTPUT"
        ls -R "$TEST_DIR"
        exit 1
    fi

    # Verify files still exist
    if [ -f dirA/file_a.txt ] && [ -f dirB/file_b.txt ] && [ -f dirA/unique.txt ]; then
        echo "PASS: Duplicates (dry run) - Files still exist after dry run."
    else
        echo "FAIL: Duplicates (dry run) - Files were unexpectedly modified or deleted during dry run."
        ls -R "$TEST_DIR"
        exit 1
    fi

    cleanup_test_env
}

# Test case 3: Delete duplicates
test_delete_duplicates() {
    echo "\n--- Running test: Delete duplicates ---"
    setup_test_env

    mkdir -p dirX dirY
    echo "content to be deleted" > dirX/original.dat
    echo "content to be deleted" > dirY/copy.dat
    echo "another unique file" > dirX/another.txt

    OUTPUT=$("$DEDUPLICATE_SCRIPT" --delete dirX dirY 2>&1)
    echo "$OUTPUT"

    if echo "$OUTPUT" | grep -q "Duplicate files found" && \
       echo "$OUTPUT" | grep -q "Purging: $TEST_DIR/dirY/copy.dat" && \
       echo "$OUTPUT" | grep -q "Purged successfully." && \
       echo "$OUTPUT" | grep -q "Total duplicate files purged: 1"; then
        echo "PASS: Delete duplicates - Correctly identified and purged one duplicate."
    else
        echo "FAIL: Delete duplicates - Expected purge message, got:\n$OUTPUT"
        exit 1
    fi

    # Verify files
    if [ -f dirX/original.dat ] && [ ! -f dirY/copy.dat ] && [ -f dirX/another.txt ]; then
        echo "PASS: Delete duplicates - Duplicate file was deleted, original and unique files remain."
    else
        echo "FAIL: Delete duplicates - File system state incorrect after deletion."
        ls -R "$TEST_DIR"
        exit 1
    fi

    cleanup_test_env
}

# Test case 4: Hash algorithm selection (md5)
test_hash_algo_md5() {
    echo "\n--- Running test: Hash algorithm MD5 ---"
    setup_test_env

    mkdir -p data
    echo "md5 test content" > data/file1.txt
    echo "md5 test content" > data/file2.txt

    OUTPUT=$("$DEDUPLICATE_SCRIPT" --dry-run --hash-algo md5 data 2>&1)
    echo "$OUTPUT"

    if echo "$OUTPUT" | grep -q "Using hash algorithm: md5sum" && \
       echo "$OUTPUT" | grep -q "Duplicate files found" && \
       echo "$OUTPUT" | grep -q "Keeping: $TEST_DIR/data/file1.txt (Original)" && \
       echo "$OUTPUT" | grep -q "Duplicate: $TEST_DIR/data/file2.txt"; then
        echo "PASS: Hash algorithm MD5 - Correctly used md5sum and found duplicates."
    else
        echo "FAIL: Hash algorithm MD5 - Expected md5sum usage and duplicate identification, got:\n$OUTPUT"
        exit 1
    fi

    cleanup_test_env
}

# Test case 5: Minimum size filter
test_min_size() {
    echo "\n--- Running test: Minimum size filter ---"
    setup_test_env

    mkdir -p sized_files
    # File smaller than 10 bytes
    echo "small" > sized_files/small_file.txt # 6 bytes
    # File larger than 10 bytes, duplicate
    printf '%s' "this is a larger file content" > sized_files/large_file1.txt # 29 bytes
    printf '%s' "this is a larger file content" > sized_files/large_file2.txt # 29 bytes

    OUTPUT=$("$DEDUPLICATE_SCRIPT" --dry-run --min-size 10c sized_files 2>&1) # 10c means 10 bytes
    echo "$OUTPUT"

    if echo "$OUTPUT" | grep -q "Minimum file size: 10c" && \
       echo "$OUTPUT" | grep -q "Duplicate files found" && \
       echo "$OUTPUT" | grep -q "Keeping: $TEST_DIR/sized_files/large_file1.txt (Original)" && \
       echo "$OUTPUT" | grep -q "Duplicate: $TEST_DIR/sized_files/large_file2.txt" && \
       ! echo "$OUTPUT" | grep -q "small_file.txt"; then # small_file.txt should not be processed
        echo "PASS: Minimum size filter - Correctly filtered by size and found duplicates."
    else
        echo "FAIL: Minimum size filter - Expected size filtering and duplicate identification, got:\n$OUTPUT"
        exit 1
    fi

    cleanup_test_env
}

# Test case 6: No directories provided
test_no_dirs() {
    echo "\n--- Running test: No directories provided ---"
    setup_test_env

    OUTPUT=$("$DEDUPLICATE_SCRIPT" 2>&1 || true) # Allow script to exit with error
    echo "$OUTPUT"

    if echo "$OUTPUT" | grep -q "Error: No directories specified." && \
       echo "$OUTPUT" | grep -q "Usage:"; then
        echo "PASS: No directories provided - Correctly showed error and usage."
    else
        echo "FAIL: No directories provided - Expected error message, got:\n$OUTPUT"
        exit 1
    fi

    cleanup_test_env
}

# Test case 7: Invalid directory provided
test_invalid_dir() {
    echo "\n--- Running test: Invalid directory provided ---"
    setup_test_env

    OUTPUT=$("$DEDUPLICATE_SCRIPT" --dry-run /non/existent/path 2>&1 || true) # Allow script to exit with error
    echo "$OUTPUT"

    if echo "$OUTPUT" | grep -q "Error: Directory '/non/existent/path' not found."; then
        echo "PASS: Invalid directory provided - Correctly showed error."
    else
        echo "FAIL: Invalid directory provided - Expected error message, got:\n$OUTPUT"
        exit 1
    fi

    cleanup_test_env
}

# Run all tests
echo "Starting all tests for nightly-scavenged-deduplicator..."
test_no_duplicates_dry_run
test_duplicates_dry_run
test_delete_duplicates
test_hash_algo_md5
test_min_size
test_no_dirs
test_invalid_dir
echo "\nAll tests completed successfully!"
