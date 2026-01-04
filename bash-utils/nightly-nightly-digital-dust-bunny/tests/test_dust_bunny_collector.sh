#!/bin/bash

# Automated tests for Nightly Digital Dust Bunny Collector

set -euo pipefail

# --- Test Setup ---

# Create temporary directories for testing
TEST_ROOT_DIR=$(mktemp -d -t dust-bunny-test-XXXXXX)
TEST_TARGET_DIR="$TEST_ROOT_DIR/target"
TEST_ARCHIVE_DIR="$TEST_ROOT_DIR/archive"

mkdir -p "$TEST_TARGET_DIR"
mkdir -p "$TEST_ARCHIVE_DIR"

# Source the script to be tested
SCRIPT_TO_TEST="$(dirname "$0")"/../src/dust_bunny_collector.sh

# --- Mocking --- 
# Mock rationale: We need to control file operations to ensure determinism and avoid affecting the actual filesystem.
# By redefining 'realpath' and 'mv', we can simulate their behavior and verify interactions without unintended side effects.

# Mock realpath to ensure consistent absolute paths for testing purposes.
# Mock rationale: realpath behavior can vary or be unavailable. This mock provides a controlled, deterministic absolute path resolution.
_mocked_realpath_calls=()
realpath() {
    _mocked_realpath_calls+=("$1")
    # For testing, we'll just return the input as an absolute path if it's not already.
    # This simplifies testing by ensuring consistent path formats.
    if [[ "$1" == /* ]]; then
        echo "$1"
    else
        echo "$(pwd)/$1"
    fi
}
export -f realpath

# Mock mv to log calls and perform the actual move for state verification.
# Mock rationale: Capturing 'mv' calls allows us to verify the script's intended actions.
# Performing the actual move within the test environment allows for state-based assertions on the filesystem.
_mocked_mv_calls=()
mv() {
    _mocked_mv_calls+=("$*")
    # Perform the actual move using the system's mv for state-based assertions
    /bin/mv "$@"
}
export -f mv

# Mock command -v for realpath check in the main script
# Mock rationale: To control the script's behavior regarding realpath availability during tests.
command() {
    if [[ "$1" == "-v" && "$2" == "realpath" ]]; then
        # Simulate realpath being available for these tests
        return 0
    else
        # Call the actual command for other cases
        /usr/bin/command "$@"
    fi
}
export -f command

# --- Helper Functions ---

# Function to clean up temporary directories
cleanup() {
    if [[ -d "$TEST_ROOT_DIR" ]]; then
        rm -rf "$TEST_ROOT_DIR"
    fi
}

# Register cleanup function to run on exit
trap cleanup EXIT

# Function to assert equality
assert_eq() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$expected" != "$actual" ]]; then
        echo "FAIL: $message"
        echo "  Expected: '$expected'"
        echo "  Actual:   '$actual'"
        exit 1
    else
        echo "PASS: $message"
    fi
}

# Function to assert file existence
assert_file_exists() {
    local file="$1"
    local message="$2"
    if [[ ! -f "$file" ]]; then
        echo "FAIL: $message - File '$file' does not exist."
        exit 1
    else
        echo "PASS: $message - File '$file' exists."
    fi
}

# Function to assert file non-existence
assert_file_not_exists() {
    local file="$1"
    local message="$2"
    if [[ -f "$file" ]]; then
        echo "FAIL: $message - File '$file' unexpectedly exists."
        exit 1
    else
        echo "PASS: $message - File '$file' does not exist."
    fi
}

# --- Test Cases ---

# Test 1: No dust bunnies found
echo "\n--- Running Test Case 1: No dust bunnies found ---"

# Create a recent file (e.g., modified today)
touch "$TEST_TARGET_DIR/recent_file.txt"

# Run the script, capture output. Age 10 days, so recent file is not moved.
OUTPUT=$(bash "$SCRIPT_TO_TEST" "$TEST_TARGET_DIR" "$TEST_ARCHIVE_DIR" 10)

assert_file_exists "$TEST_TARGET_DIR/recent_file.txt" "Recent file should remain in target dir"
assert_file_not_exists "$TEST_ARCHIVE_DIR/recent_file.txt" "Recent file should not be in archive dir"
assert_eq "0" "$(find "$TEST_ARCHIVE_DIR" -type f | wc -l)" "Archive directory should be empty"

if ! echo "$OUTPUT" | grep -q "No dust bunnies found"; then
    echo "FAIL: Test 1 - Expected 'No dust bunnies found' in output."
    echo "Output: $OUTPUT"
    exit 1
else
    echo "PASS: Test 1 - Output contains 'No dust bunnies found'."
fi

# Reset for next test
cleanup
mkdir -p "$TEST_TARGET_DIR"
mkdir -p "$TEST_ARCHIVE_DIR"

# Test 2: Single dust bunny found and moved
echo "\n--- Running Test Case 2: Single dust bunny found and moved ---"

# Create an old file (e.g., modified on Feb 1st, 2024) and a recent file (Mar 1st, 2024)
OLD_FILE="$TEST_TARGET_DIR/old_log.txt"
touch -t 202402010000 "$OLD_FILE" 
RECENT_FILE="$TEST_TARGET_DIR/recent_report.pdf"
touch -t 202403010000 "$RECENT_FILE"

# Run the script with age 10 days (so the Feb 1st file is older than 10 days relative to current date, assuming current date is after Feb 11th)
OUTPUT=$(bash "$SCRIPT_TO_TEST" "$TEST_TARGET_DIR" "$TEST_ARCHIVE_DIR" 10)

assert_file_not_exists "$OLD_FILE" "Old file should be moved from target dir"
assert_file_exists "$TEST_ARCHIVE_DIR/old_log.txt" "Old file should exist in archive dir"
assert_file_exists "$RECENT_FILE" "Recent file should remain in target dir"
assert_file_not_exists "$TEST_ARCHIVE_DIR/recent_report.pdf" "Recent file should not be in archive dir"
assert_eq "1" "$(find "$TEST_ARCHIVE_DIR" -type f | wc -l)" "Archive directory should contain one file"

if ! echo "$OUTPUT" | grep -q "Moved: 'old_log.txt' -> '$TEST_ARCHIVE_DIR/old_log.txt'"; then
    echo "FAIL: Test 2 - Expected move message for old_log.txt."
    echo "Output: $OUTPUT"
    exit 1
else
    echo "PASS: Test 2 - Output contains move message for old_log.txt'."
fi

# Reset for next test
cleanup
mkdir -p "$TEST_TARGET_DIR"
mkdir -p "$TEST_ARCHIVE_DIR"

# Test 3: Multiple dust bunnies with subdirectories
echo "\n--- Running Test Case 3: Multiple dust bunnies with subdirectories ---"

mkdir -p "$TEST_TARGET_DIR/logs/app1"
mkdir -p "$TEST_TARGET_DIR/data"

touch -t 202401010000 "$TEST_TARGET_DIR/logs/app1/error.log"
touch -t 202401150000 "$TEST_TARGET_DIR/logs/app1/access.log"
touch -t 202402010000 "$TEST_TARGET_DIR/data/temp.csv"
touch -t 202403050000 "$TEST_TARGET_DIR/recent_config.ini"

# Run the script with age 20 days (so all but recent_config.ini are older than 20 days relative to current date)
OUTPUT=$(bash "$SCRIPT_TO_TEST" "$TEST_TARGET_DIR" "$TEST_ARCHIVE_DIR" 20)

assert_file_not_exists "$TEST_TARGET_DIR/logs/app1/error.log" "error.log should be moved"
assert_file_exists "$TEST_ARCHIVE_DIR/logs/app1/error.log" "error.log should be in archive"

assert_file_not_exists "$TEST_TARGET_DIR/logs/app1/access.log" "access.log should be moved"
assert_file_exists "$TEST_ARCHIVE_DIR/logs/app1/access.log" "access.log should be in archive"

assert_file_not_exists "$TEST_TARGET_DIR/data/temp.csv" "temp.csv should be moved"
assert_file_exists "$TEST_ARCHIVE_DIR/data/temp.csv" "temp.csv should be in archive"

assert_file_exists "$TEST_TARGET_DIR/recent_config.ini" "recent_config.ini should remain"
assert_file_not_exists "$TEST_ARCHIVE_DIR/recent_config.ini" "recent_config.ini should not be in archive"

assert_eq "3" "$(find "$TEST_ARCHIVE_DIR" -type f | wc -l)" "Archive directory should contain three files"

if ! echo "$OUTPUT" | grep -q "Successfully swept 3 digital dust bunnies"; then
    echo "FAIL: Test 3 - Expected summary for 3 dust bunnies."
    echo "Output: $OUTPUT"
    exit 1
else
    echo "PASS: Test 3 - Output contains summary for 3 dust bunnies."
fi

# Reset for next test
cleanup
mkdir -p "$TEST_TARGET_DIR"
mkdir -p "$TEST_ARCHIVE_DIR"

# Test 4: Invalid arguments
echo "\n--- Running Test Case 4: Invalid arguments ---"

# Test missing arguments
OUTPUT_ERR=$(bash "$SCRIPT_TO_TEST" 2>&1 || true)
if ! echo "$OUTPUT_ERR" | grep -q "Usage:"; then
    echo "FAIL: Test 4.1 - Expected usage message for missing args."
    echo "Output: $OUTPUT_ERR"
    exit 1
else
    echo "PASS: Test 4.1 - Usage message displayed for missing args."
fi

# Test invalid target directory
OUTPUT_ERR=$(bash "$SCRIPT_TO_TEST" "/non/existent/dir" "$TEST_ARCHIVE_DIR" 10 2>&1 || true)
if ! echo "$OUTPUT_ERR" | grep -q "Error: Target directory"; then
    echo "FAIL: Test 4.2 - Expected error for non-existent target dir."
    echo "Output: $OUTPUT_ERR"
    exit 1
else
    echo "PASS: Test 4.2 - Error message displayed for non-existent target dir."
fi

# Test invalid age
OUTPUT_ERR=$(bash "$SCRIPT_TO_TEST" "$TEST_TARGET_DIR" "$TEST_ARCHIVE_DIR" "abc" 2>&1 || true)
if ! echo "$OUTPUT_ERR" | grep -q "Error: Age in days must be a non-negative integer."; then
    echo "FAIL: Test 4.3 - Expected error for invalid age."
    echo "Output: $OUTPUT_ERR"
    exit 1
else
    echo "PASS: Test 4.3 - Error message displayed for invalid age."
fi

# Test negative age
OUTPUT_ERR=$(bash "$SCRIPT_TO_TEST" "$TEST_TARGET_DIR" "$TEST_ARCHIVE_DIR" -5 2>&1 || true)
if ! echo "$OUTPUT_ERR" | grep -q "Error: Age in days must be a non-negative integer."; then
    echo "FAIL: Test 4.4 - Expected error for negative age."
    echo "Output: $OUTPUT_ERR"
    exit 1
else
    echo "PASS: Test 4.4 - Error message displayed for negative age."
fi

echo "\nAll tests completed."
