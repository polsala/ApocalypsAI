#!/bin/bash

# Test setup
TEST_DIR=$(mktemp -d)
ARCHIVE_DIR=$(mktemp -d)
SCRIPT_PATH="./src/forage.sh"

# Mock rationale: We create a temporary directory structure and files with specific
# modification times using 'touch -d' to simulate different file ages. This allows
# 'find' to operate on a controlled environment, making tests deterministic and offline.
setup_test_environment() {
    # Create files with different ages
    touch -d "2 days ago" "$TEST_DIR/recent_file.txt"
    touch -d "100 days ago" "$TEST_DIR/old_file_1.log"
    mkdir -p "$TEST_DIR/subdir"
    touch -d "120 days ago" "$TEST_DIR/subdir/old_file_2.conf"
    touch -d "50 days ago" "$TEST_DIR/subdir/recent_config.cfg"
    mkdir -p "$TEST_DIR/empty_dir"
}

cleanup_test_environment() {
    rm -rf "$TEST_DIR" "$ARCHIVE_DIR"
}

# Test 1: List files older than 90 days
test_list_old_files() {
    echo "Running Test 1: List files older than 90 days"
    setup_test_environment

    # Run the script and capture output
    OUTPUT=$("$SCRIPT_PATH" -d "$TEST_DIR" -a 90)

    # Assertions
    if echo "$OUTPUT" | grep -q "$TEST_DIR/old_file_1.log" && \
       echo "$OUTPUT" | grep -q "$TEST_DIR/subdir/old_file_2.conf" && \
       ! echo "$OUTPUT" | grep -q "$TEST_DIR/recent_file.txt" && \
       ! echo "$OUTPUT" | grep -q "$TEST_DIR/subdir/recent_config.cfg"; then
        echo "Test 1 PASSED"
    else
        echo "Test 1 FAILED: Expected old files not found or recent files included."
        echo "Output: $OUTPUT"
        cleanup_test_environment
        exit 1
    fi
    cleanup_test_environment
}

# Test 2: Move files older than 90 days
test_move_old_files() {
    echo "Running Test 2: Move files older than 90 days"
    setup_test_environment

    # Run the script to move files
    "$SCRIPT_PATH" -d "$TEST_DIR" -a 90 -m "$ARCHIVE_DIR" > /dev/null

    # Assertions: Check if files are moved
    if [[ ! -f "$TEST_DIR/old_file_1.log" ]] && \
       [[ ! -f "$TEST_DIR/subdir/old_file_2.conf" ]] && \
       [[ -f "$ARCHIVE_DIR/old_file_1.log" ]] && \
       [[ -f "$ARCHIVE_DIR/old_file_2.conf" ]] && \
       [[ -f "$TEST_DIR/recent_file.txt" ]] && \
       [[ -f "$TEST_DIR/subdir/recent_config.cfg" ]]; then
        echo "Test 2 PASSED"
    else
        echo "Test 2 FAILED: Files not moved correctly."
        ls -l "$TEST_DIR" "$ARCHIVE_DIR"
        cleanup_test_environment
        exit 1
    fi
    cleanup_test_environment
}

# Test 3: No forgotten files
test_no_forgotten_files() {
    echo "Running Test 3: No forgotten files"
    TEST_DIR_EMPTY=$(mktemp -d)
    touch -d "10 days ago" "$TEST_DIR_EMPTY/recent_only.txt"

    OUTPUT=$("$SCRIPT_PATH" -d "$TEST_DIR_EMPTY" -a 90)

    if echo "$OUTPUT" | grep -q "No forgotten digital relics found"; then
        echo "Test 3 PASSED"
    else
        echo "Test 3 FAILED: Expected 'no forgotten files' message not found."
        echo "Output: $OUTPUT"
        rm -rf "$TEST_DIR_EMPTY"
        exit 1
    fi
    rm -rf "$TEST_DIR_EMPTY"
}

# Test 4: Invalid archive directory (should create it)
test_create_archive_dir() {
    echo "Running Test 4: Create archive directory if it doesn't exist"
    setup_test_environment
    NON_EXISTENT_ARCHIVE_DIR="$TEST_DIR/new_archive_location"

    "$SCRIPT_PATH" -d "$TEST_DIR" -a 90 -m "$NON_EXISTENT_ARCHIVE_DIR" > /dev/null

    if [[ -d "$NON_EXISTENT_ARCHIVE_DIR" ]] && \
       [[ -f "$NON_EXISTENT_ARCHIVE_DIR/old_file_1.log" ]]; then
        echo "Test 4 PASSED"
    else
        echo "Test 4 FAILED: Archive directory not created or files not moved."
        ls -l "$TEST_DIR" "$NON_EXISTENT_ARCHIVE_DIR"
        cleanup_test_environment
        exit 1
    fi
    cleanup_test_environment
}


# Run all tests
test_list_old_files
test_move_old_files
test_no_forgotten_files
test_create_archive_dir

echo "All tests completed."
