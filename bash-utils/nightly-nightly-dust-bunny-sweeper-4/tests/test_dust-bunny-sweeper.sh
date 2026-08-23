#!/bin/bash

# Automated tests for nightly-dust-bunny-sweeper

# --- Test Setup ---
TEST_DIR="$(mktemp -d)"
TEST_TRASH_DIR="$(mktemp -d)"
SCRIPT_PATH="$(dirname "$0")"/../src/dust-bunny-sweeper.sh

# Mock rationale: We don't want to actually delete files during tests.
# This function replaces the real 'rm' command to simulate deletion
# by moving files to a 'TRASH' directory within the test environment.
# It also logs the 'deletion' to stderr for capture.
mock_rm() {
    for file in "$@"; do
        if [[ -f "$file" ]]; then
            echo "MOCK_RM: Deleting $file" >&2
            mv "$file" "$TEST_TRASH_DIR/"
        fi
    done
}

# Export mock function and variable
export -f mock_rm
export RM_CMD="mock_rm"

# Function to clean up test environment
cleanup() {
    rm -rf "$TEST_DIR" "$TEST_TRASH_DIR"
}
trap cleanup EXIT

# Function to create dummy files with specific modification times
create_dummy_files() {
    local dir="$1"
    local old_days_1="$2"
    local old_days_2="$3"
    local old_days_3="$4"
    local recent_days="$5"

    touch -d "${old_days_1} days ago" "$dir/old_file_1.txt"
    touch -d "${old_days_2} days ago" "$dir/old_file_2.log"
    touch -d "${old_days_3} days ago" "$dir/file with spaces.conf"
    touch -d "${recent_days} days ago" "$dir/recent_file.txt"
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
        echo "FAIL: Expected '$haystack' NOT to contain '$needle'"
        exit 1
    fi
}

assert_file_exists() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        echo "FAIL: Expected file '$file' to exist."
        exit 1
    fi
}

assert_file_not_exists() {
    local file="$1"
    if [[ -f "$file" ]]; then
        echo "FAIL: Expected file '$file' NOT to exist."
        exit 1
    fi
}

run_test() {
    local test_name="$1"
    local expected_status="$2"
    local read_input="$3"
    shift 3

    echo "Running test: $test_name"
    # Clear test directory for each test
    rm -rf "$TEST_DIR"/*
    rm -rf "$TEST_TRASH_DIR"/*

    # Create dummy files for the test (40, 35, 40, 5 days old)
    create_dummy_files "$TEST_DIR" 40 35 40 5

    # Run the script, piping read_input for confirmation, capturing stdout and stderr
    # Mock rationale: We pipe 'read' input to simulate user confirmation and capture stderr for mock_rm logs.
    OUTPUT=$(echo "$read_input" | "$SCRIPT_PATH" "$@" 2>&1 )
    STATUS=$?

    if [[ "$STATUS" -ne "$expected_status" ]]; then
        echo "FAIL: $test_name - Expected exit status $expected_status, got $STATUS."
        echo "Output:\n$OUTPUT\n"
        exit 1
    fi
    echo "PASS: $test_name"
    return 0
}

# --- Test Cases ---

# Test 1: List files older than 30 days (default age)
run_test "List default age" 0 "" "$TEST_DIR"
assert_contains "$OUTPUT" "old_file_1.txt"
assert_contains "$OUTPUT" "old_file_2.log"
assert_contains "$OUTPUT" "file with spaces.conf"
assert_not_contains "$OUTPUT" "recent_file.txt"
assert_contains "$OUTPUT" "To sweep these dust bunnies away, run with the --delete flag."

# Test 2: List files older than 35 days
run_test "List custom age (35 days)" 0 "" "-a" 35 "$TEST_DIR"
assert_contains "$OUTPUT" "old_file_1.txt"
assert_not_contains "$OUTPUT" "old_file_2.log" # 35 days old, not >35
assert_contains "$OUTPUT" "file with spaces.conf"
assert_not_contains "$OUTPUT" "recent_file.txt"

# Test 3: List files, no dust bunnies found
run_test "No dust bunnies found" 0 "" "-a" 50 "$TEST_DIR"
assert_contains "$OUTPUT" "No digital dust bunnies found."
assert_not_contains "$OUTPUT" "old_file_1.txt"

# Test 4: Delete files with confirmation (user says 'y')
run_test "Delete with confirmation (y)" 0 "y" "-d" "$TEST_DIR"
assert_contains "$OUTPUT" "Sweeping away the digital dust bunnies..."
assert_contains "$OUTPUT" "MOCK_RM: Deleting $TEST_DIR/old_file_1.txt"
assert_contains "$OUTPUT" "MOCK_RM: Deleting $TEST_DIR/old_file_2.log"
assert_contains "$OUTPUT" "MOCK_RM: Deleting $TEST_DIR/file with spaces.conf"
assert_file_not_exists "$TEST_DIR/old_file_1.txt"
assert_file_not_exists "$TEST_DIR/old_file_2.log"
assert_file_not_exists "$TEST_DIR/file with spaces.conf"
assert_file_exists "$TEST_DIR/recent_file.txt"
assert_file_exists "$TEST_TRASH_DIR/old_file_1.txt"

# Test 5: Delete files with confirmation (user says 'n')
run_test "Delete with confirmation (n)" 0 "n" "-d" "$TEST_DIR"
assert_contains "$OUTPUT" "Sweep aborted. Digital dust bunnies live to see another day."
assert_not_contains "$OUTPUT" "MOCK_RM: Deleting"
assert_file_exists "$TEST_DIR/old_file_1.txt"
assert_file_exists "$TEST_DIR/old_file_2.log"
assert_file_exists "$TEST_DIR/file with spaces.conf"
assert_file_exists "$TEST_DIR/recent_file.txt"

# Test 6: Force delete files (no confirmation)
run_test "Force delete" 0 "" "-d" "-f" "$TEST_DIR"
assert_contains "$OUTPUT" "Sweeping away the digital dust bunnies..."
assert_contains "$OUTPUT" "MOCK_RM: Deleting $TEST_DIR/old_file_1.txt"
assert_contains "$OUTPUT" "MOCK_RM: Deleting $TEST_DIR/old_file_2.log"
assert_contains "$OUTPUT" "MOCK_RM: Deleting $TEST_DIR/file with spaces.conf"
assert_file_not_exists "$TEST_DIR/old_file_1.txt"
assert_file_not_exists "$TEST_DIR/old_file_2.log"
assert_file_not_exists "$TEST_DIR/file with spaces.conf"
assert_file_exists "$TEST_DIR/recent_file.txt"
assert_file_exists "$TEST_TRASH_DIR/old_file_1.txt"

# Test 7: Invalid directory
run_test "Invalid directory" 1 "" "/non/existent/path/to/nowhere"
assert_contains "$OUTPUT" "Error: Directory '/non/existent/path/to/nowhere' not found or is not a directory."

# Test 8: No directory argument
run_test "No directory argument" 1 ""
assert_contains "$OUTPUT" "Error: No directory specified."
assert_contains "$OUTPUT" "Usage:"

# Test 9: Invalid age argument (non-numeric)
run_test "Invalid age argument (non-numeric)" 1 "" "-a" "abc" "$TEST_DIR"
assert_contains "$OUTPUT" "Error: --age must be a positive integer."

# Test 10: Invalid age argument (missing value)
run_test "Invalid age argument (missing value)" 1 "" "-a" "$TEST_DIR"
assert_contains "$OUTPUT" "Error: --age requires a numeric argument."

echo "All tests passed!"
