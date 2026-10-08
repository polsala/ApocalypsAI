#!/bin/bash

# Test script for src/detect_drift.sh

# Mock rationale: This test creates a temporary git repository and manipulates file timestamps
# and commit history to simulate various scenarios. This allows for deterministic and offline
# testing of the detect_drift.sh script without relying on an actual GitHub repository or network access.

set -euo pipefail

# Define colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

TEST_DIR=$(mktemp -d)
REPO_PATH="$TEST_DIR/test_repo"
SCRIPT_PATH="$(dirname "$(dirname "$(realpath "$0")")")"/src/detect_drift.sh

echo "Running tests in $TEST_DIR"

cleanup() {
    echo "Cleaning up $TEST_DIR"
    rm -rf "$TEST_DIR"
}

trap cleanup EXIT

# --- Test Helper Functions ---
assert_output() {
    local test_name="$1"
    local expected_drift_detected="$2"
    local expected_drift_files="$3"
    local actual_output="$4"

    local actual_drift_detected=$(echo "$actual_output" | grep "DRIFT_DETECTED=" | cut -d'=' -f2)
    local actual_drift_files=$(echo "$actual_output" | grep "DRIFT_FILES=" | cut -d'=' -f2-)

    echo "  Test: $test_name"
    echo "    Expected DRIFT_DETECTED: $expected_drift_detected, Actual: $actual_drift_detected"
    echo "    Expected DRIFT_FILES: '$expected_drift_files', Actual: '$actual_drift_files'"

    if [[ "$actual_drift_detected" == "$expected_drift_detected" ]] && \
       [[ "$actual_drift_files" == "$expected_drift_files" ]]; then
        echo -e "  ${GREEN}PASS${NC}: $test_name"
    else
        echo -e "  ${RED}FAIL${NC}: $test_name"
        echo "  Full output:"
        echo "$actual_output"
        exit 1
    fi
}

# --- Test Cases ---

# Test 1: No drift
test_no_drift() {
    echo "--- Running Test: No Drift ---"
    mkdir -p "$REPO_PATH"
    cd "$REPO_PATH"

    git init -b main > /dev/null
    echo "initial content" > file1.txt
    git add file1.txt
    git commit -m "Initial commit" > /dev/null

    # Run the script
    local output=$("$SCRIPT_PATH" "$REPO_PATH")
    assert_output "No drift" "false" "" "$output"
    cd - > /dev/null
    rm -rf "$REPO_PATH" # Clean up for next test
}

# Test 2: Single file with drift
test_single_file_drift() {
    echo "--- Running Test: Single File Drift ---"
    mkdir -p "$REPO_PATH"
    cd "$REPO_PATH"

    git init -b main > /dev/null
    echo "initial content" > file1.txt
    git add file1.txt
    git commit -m "Initial commit" > /dev/null

    # Modify file after commit without committing
    sleep 1 # Ensure mtime is strictly greater
    echo "modified content" > file1.txt
    
    local output=$("$SCRIPT_PATH" "$REPO_PATH")
    assert_output "Single file drift" "true" "file1.txt\n" "$output"
    cd - > /dev/null
    rm -rf "$REPO_PATH"
}

# Test 3: Multiple files with drift
test_multiple_files_drift() {
    echo "--- Running Test: Multiple Files Drift ---"
    mkdir -p "$REPO_PATH"
    cd "$REPO_PATH"

    git init -b main > /dev/null
    echo "content1" > file1.txt
    echo "content2" > file2.txt
    git add .
    git commit -m "Initial commit" > /dev/null

    sleep 1
    echo "modified content1" > file1.txt
    sleep 1
    echo "modified content2" > file2.txt

    local output=$("$SCRIPT_PATH" "$REPO_PATH")
    assert_output "Multiple files drift" "true" "file1.txt\nfile2.txt\n" "$output"
    cd - > /dev/null
    rm -rf "$REPO_PATH"
}

# Test 4: File modified and then committed (no drift)
test_committed_file_no_drift() {
    echo "--- Running Test: Committed File No Drift ---"
    mkdir -p "$REPO_PATH"
    cd "$REPO_PATH"

    git init -b main > /dev/null
    echo "initial content" > file1.txt
    git add file1.txt
    git commit -m "Initial commit" > /dev/null

    sleep 1
    echo "modified content" > file1.txt
    git add file1.txt
    git commit -m "Second commit" > /dev/null # mtime should now be <= commit_time

    local output=$("$SCRIPT_PATH" "$REPO_PATH")
    assert_output "Committed file no drift" "false" "" "$output"
    cd - > /dev/null
    rm -rf "$REPO_PATH"
}

# Test 5: New untracked file (should not be reported as drift)
test_untracked_file() {
    echo "--- Running Test: Untracked File ---"
    mkdir -p "$REPO_PATH"
    cd "$REPO_PATH"

    git init -b main > /dev/null
    echo "initial content" > file1.txt
    git add file1.txt
    git commit -m "Initial commit" > /dev/null

    echo "new untracked content" > untracked_file.txt # Not added to git

    local output=$("$SCRIPT_PATH" "$REPO_PATH")
    assert_output "Untracked file" "false" "" "$output" # Should not detect untracked files
    cd - > /dev/null
    rm -rf "$REPO_PATH"
}

# Test 6: File with spaces in name
test_file_with_spaces() {
    echo "--- Running Test: File with Spaces ---"
    mkdir -p "$REPO_PATH"
    cd "$REPO_PATH"

    git init -b main > /dev/null
    echo "content" > "file with spaces.txt"
    git add "file with spaces.txt"
    git commit -m "Commit file with spaces" > /dev/null

    sleep 1
    echo "modified content" > "file with spaces.txt"

    local output=$("$SCRIPT_PATH" "$REPO_PATH")
    assert_output "File with spaces drift" "true" "file with spaces.txt\n" "$output"
    cd - > /dev/null
    rm -rf "$REPO_PATH"
}

# Test 7: Drift in a subdirectory
test_subdirectory_drift() {
    echo "--- Running Test: Subdirectory Drift ---"
    mkdir -p "$REPO_PATH/subdir"
    cd "$REPO_PATH"

    git init -b main > /dev/null
    echo "content" > subdir/file_in_subdir.txt
    git add .
    git commit -m "Commit file in subdir" > /dev/null

    sleep 1
    echo "modified content" > subdir/file_in_subdir.txt

    local output=$("$SCRIPT_PATH" "$REPO_PATH")
    assert_output "Subdirectory file drift" "true" "subdir/file_in_subdir.txt\n" "$output"
    cd - > /dev/null
    rm -rf "$REPO_PATH"
}


# Run all tests
test_no_drift
test_single_file_drift
test_multiple_files_drift
test_committed_file_no_drift
test_untracked_file
test_file_with_spaces
test_subdirectory_drift

echo -e "\n${GREEN}All tests passed!${NC}"
