#!/bin/bash

# Test script for Nightly Scavenger's Stash Sorter

set -euo pipefail

SCRIPT_PATH="../src/nightly-scavenger-stash-sort.sh"
TEST_DIR=""

# --- Helper Functions ---

# Function to create a temporary test environment
setup_test_env() {
    TEST_DIR=$(mktemp -d -t stash-sort-test-XXXXXX)
    echo "Setting up test environment in: $TEST_DIR"
    cd "$TEST_DIR"

    # Create dummy files
    touch "document.pdf"
    touch "image.jpg"
    touch "archive.zip"
    touch "script.sh"
    touch "audio.mp3"
    touch "video.mp4"
    touch "code.py"
    touch "unknown_file"
    touch "another file with spaces.txt"
    mkdir "empty_subdir" # Should be ignored by find -type f
    echo "Test content" > "document.txt"
    echo "Test content" > "script.sh"
    chmod +x "script.sh" # Make script executable
    echo "Test content" > "my_app.bin"
    chmod +x "my_app.bin"

    # Create a file that's already in its "correct" category
    mkdir -p "documents"
    touch "documents/pre_sorted_doc.pdf"

    echo "Dummy files created."
}

# Function to clean up the temporary test environment
cleanup_test_env() {
    if [[ -n "$TEST_DIR" && -d "$TEST_DIR" ]]; then
        echo "Cleaning up test environment: $TEST_DIR"
        rm -rf "$TEST_DIR"
    fi
}

# Function to assert a condition
assert_eq() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$expected" == "$actual" ]]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message (Expected: '$expected', Actual: '$actual')"
        exit 1
    fi
}

assert_file_exists() {
    local file="$1"
    local message="$2"
    if [[ -f "$file" ]]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message (File '$file' does not exist)"
        exit 1
    fi
}

assert_file_not_exists() {
    local file="$1"
    local message="$2"
    if [[ ! -f "$file" ]]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message (File '$file' unexpectedly exists)"
        exit 1
    fi
}

assert_dir_exists() {
    local dir="$1"
    local message="$2"
    if [[ -d "$dir" ]]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message (Directory '$dir' does not exist)"
        exit 1
    fi
}

# --- Test Cases ---

# Test 1: Help message
test_help_message() {
    echo "--- Running Test: Help Message ---"
    local output=$("$SCRIPT_PATH" --help)
    assert_eq "Usage: nightly-scavenger-stash-sort.sh [OPTIONS] <source_directory>" "$(echo "$output" | head -n 1)" "Help message starts correctly"
    echo ""
}

# Test 2: Dry run mode
test_dry_run() {
    echo "--- Running Test: Dry Run Mode ---"
    setup_test_env
    local output=$("$SCRIPT_PATH" --dry-run .)

    assert_file_exists "document.pdf" "File 'document.pdf' still exists in source after dry run"
    assert_file_not_exists "images/image.jpg" "# Mock rationale: This file should not exist yet. The dry run should not create it. This is a check that the dry run didn't move it." "File 'image.jpg' not moved to 'images' during dry run"
    assert_dir_exists "documents" "Documents directory exists (pre-sorted)"
    assert_file_exists "documents/pre_sorted_doc.pdf" "Pre-sorted doc still exists"

    # Check dry run output for expected messages
    echo "$output" | grep -q "DRY RUN: Would create directory: .*documents" || { echo "FAIL: Dry run output missing 'Would create documents' message"; exit 1; }
    echo "$output" | grep -q "DRY RUN: Would move 'image.jpg' to .*images/" || { echo "FAIL: Dry run output missing 'Would move image.jpg' message"; exit 1; }
    echo "$output" | grep -q "DRY RUN: Would move 'unknown_file' to .*other_finds/" || { echo "FAIL: Dry run output missing 'Would move unknown_file' message"; exit 1; }
    echo "PASS: Dry run output contains expected messages."

    cleanup_test_env
    echo ""
}

# Test 3: Live run - basic sorting
test_live_run_basic() {
    echo "--- Running Test: Live Run - Basic Sorting ---"
    setup_test_env
    "$SCRIPT_PATH" .

    assert_file_not_exists "document.pdf" "Original 'document.pdf' moved"
    assert_file_exists "documents/document.pdf" "Moved 'document.pdf' to 'documents/'"

    assert_file_not_exists "image.jpg" "Original 'image.jpg' moved"
    assert_file_exists "images/image.jpg" "Moved 'image.jpg' to 'images/'"

    assert_file_not_exists "archive.zip" "Original 'archive.zip' moved"
    assert_file_exists "archives/archive.zip" "Moved 'archive.zip' to 'archives/'"

    assert_file_not_exists "script.sh" "Original 'script.sh' moved"
    assert_file_exists "executables/script.sh" "Moved 'script.sh' to 'executables/'"

    assert_file_not_exists "audio.mp3" "Original 'audio.mp3' moved"
    assert_file_exists "audio/audio.mp3" "Moved 'audio.mp3' to 'audio/'"

    assert_file_not_exists "video.mp4" "Original 'video.mp4' moved"
    assert_file_exists "video/video.mp4" "Moved 'video.mp4' to 'video/'"

    assert_file_not_exists "code.py" "Original 'code.py' moved"
    assert_file_exists "code/code.py" "Moved 'code.py' to 'code/'"

    assert_file_not_exists "unknown_file" "Original 'unknown_file' moved"
    assert_file_exists "other_finds/unknown_file" "Moved 'unknown_file' to 'other_finds/'"

    assert_file_not_exists "another file with spaces.txt" "Original 'another file with spaces.txt' moved"
    assert_file_exists "documents/another file with spaces.txt" "Moved 'another file with spaces.txt' to 'documents/'"

    assert_file_exists "documents/pre_sorted_doc.pdf" "Pre-sorted doc still exists in documents"
    assert_file_not_exists "empty_subdir" "Empty subdirectory should remain untouched" # find -type f ignores directories

    cleanup_test_env
    echo ""
}

# Test 4: Idempotency - running twice
test_idempotency() {
    echo "--- Running Test: Idempotency ---"
    setup_test_env
    "$SCRIPT_PATH" . # First run
    local output=$("$SCRIPT_PATH" .) # Second run

    # Check that files are still in their sorted locations
    assert_file_exists "documents/document.pdf" "Document still in 'documents/' after second run"
    assert_file_exists "images/image.jpg" "Image still in 'images/' after second run"
    assert_file_exists "other_finds/unknown_file" "Unknown file still in 'other_finds/' after second run"

    # Check output for "Skipping" messages
    echo "$output" | grep -q "Skipping 'document.pdf': Already in its correct category 'documents'." || { echo "FAIL: Idempotency test missing 'Skipping document.pdf' message"; exit 1; }
    echo "$output" | grep -q "Skipping 'image.jpg': Already in its correct category 'images'." || { echo "FAIL: Idempotency test missing 'Skipping image.jpg' message"; exit 1; }
    echo "PASS: Idempotency test output contains expected skipping messages."

    cleanup_test_env
    echo ""
}

# Test 5: Non-existent source directory
test_non_existent_dir() {
    echo "--- Running Test: Non-existent Source Directory ---"
    local output=$(! "$SCRIPT_PATH" /non/existent/path 2>&1 || true) # Capture stderr and prevent script exit

    echo "$output" | grep -q "Error: Source directory '/non/existent/path' does not exist or is not a directory." || { echo "FAIL: Non-existent directory error message not found"; exit 1; }
    echo "PASS: Correctly handled non-existent directory."
    echo ""
}

# Test 6: No arguments
test_no_arguments() {
    echo "--- Running Test: No Arguments ---"
    local output=$(! "$SCRIPT_PATH" 2>&1 || true) # Capture stderr and prevent script exit

    echo "$output" | grep -q "Error: Source directory not specified." || { echo "FAIL: No arguments error message not found"; exit 1; }
    echo "PASS: Correctly handled no arguments."
    echo ""
}

# Test 7: File with spaces in name
test_file_with_spaces() {
    echo "--- Running Test: File with Spaces ---"
    setup_test_env
    # "another file with spaces.txt" is already created in setup_test_env
    "$SCRIPT_PATH" .

    assert_file_exists "documents/another file with spaces.txt" "File with spaces moved correctly"
    assert_file_not_exists "another file with spaces.txt" "Original file with spaces removed"

    cleanup_test_env
    echo ""
}

# Test 8: Executable files without common extensions (e.g., `my_app.bin`)
test_executable_bin() {
    echo "--- Running Test: Executable .bin file ---"
    setup_test_env
    # "my_app.bin" is created and made executable in setup_test_env
    "$SCRIPT_PATH" .

    assert_file_not_exists "my_app.bin" "Original 'my_app.bin' moved"
    assert_file_exists "executables/my_app.bin" "Moved 'my_app.bin' to 'executables/'"

    cleanup_test_env
    echo ""
}


# --- Run all tests ---
echo "Starting all tests for Nightly Scavenger's Stash Sorter..."
test_help_message
test_dry_run
test_live_run_basic
test_idempotency
test_non_existent_dir
test_no_arguments
test_file_with_spaces
test_executable_bin
echo "All tests passed!"
