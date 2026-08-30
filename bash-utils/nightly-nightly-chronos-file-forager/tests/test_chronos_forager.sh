#!/bin/bash

# Automated tests for Chronos's File Forager

set -euo pipefail

SCRIPT_PATH="$(dirname "$0")"/../src/chronos_forager.sh

# Function to run a test
run_test() {
    local test_name="$1"
    local command="$2"
    local expected_output_regex="$3"
    local expected_exit_code="$4"
    local actual_output
    local actual_exit_code

    echo -n "Running test: $test_name... "

    # Capture stdout and stderr, and exit code
    # Mock rationale: We are testing the script's output and behavior, not the underlying 'find' or 'rm' commands directly.
    # By redirecting stderr to stdout, we can capture all output for regex matching.
    # The core logic of 'find' and 'rm' is assumed to work correctly by the OS.
    # We control the environment (temp directory, file ages) to make the test deterministic.
    actual_output=$(eval "$command" 2>&1)
    actual_exit_code=$?

    if [[ "$actual_exit_code" -ne "$expected_exit_code" ]]; then
        echo "FAIL (Exit Code Mismatch)"
        echo "  Expected exit code: $expected_exit_code"
        echo "  Actual exit code: $actual_exit_code"
        echo "  Output: $actual_output"
        return 1
    fi

    if [[ -n "$expected_output_regex" && ! "$actual_output" =~ $expected_output_regex ]]; then
        echo "FAIL (Output Mismatch)"
        echo "  Expected output (regex): $expected_output_regex"
        echo "  Actual output: $actual_output"
        return 1
    fi

    echo "PASS"
    return 0
}

# Setup a temporary directory for tests
TEST_DIR=$(mktemp -d -t chronos-forager-XXXXXX)
cleanup() {
    echo "Cleaning up temporary directory: $TEST_DIR"
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

# Create test files with specific modification times
# Mock rationale: Using 'touch -d' to set specific modification times makes the tests deterministic and independent of the current system time.
# This simulates files of different ages without relying on actual time passing.

# File 1: 10 days old
touch -d "10 days ago" "$TEST_DIR/old_file_1.txt"
# File 2: 5 days old
touch -d "5 days ago" "$TEST_DIR/old_file_2.txt"
# File 3: 1 day old
touch -d "1 day ago" "$TEST_DIR/recent_file_1.txt"
# File 4: Just created
touch "$TEST_DIR/current_file.txt"
# File 5: 15 days old with spaces
touch -d "15 days ago" "$TEST_DIR/old file with spaces.log"

# --- Test Cases ---

# Test 1: Dry-run, find files older than 7 days
run_test \
    "Dry-run: find > 7 days" \
    "$SCRIPT_PATH \"$TEST_DIR\" 7 dry-run" \
    "old_file_1.txt.*old file with spaces.log" \
    0

# Test 2: Dry-run, find files older than 2 days (should include 10, 5, 15 days old files)
run_test \
    "Dry-run: find > 2 days" \
    "$SCRIPT_PATH \"$TEST_DIR\" 2" \
    "old_file_1.txt.*old_file_2.txt.*old file with spaces.log" \
    0

# Test 3: Dry-run, find files older than 0 days (should include all but current)
run_test \
    "Dry-run: find > 0 days" \
    "$SCRIPT_PATH \"$TEST_DIR\" 0" \
    "old_file_1.txt.*old_file_2.txt.*recent_file_1.txt.*old file with spaces.log" \
    0

# Test 4: Dry-run, find files older than 20 days (should find nothing)
run_test \
    "Dry-run: find > 20 days (none)" \
    "$SCRIPT_PATH \"$TEST_DIR\" 20 dry-run" \
    "Chronos is foraging in: '$TEST_DIR' for files older than 20 day(s).*Dry-run complete. No changes made." \
    0

# Test 5: Delete files older than 7 days (requires user confirmation, mock 'yes')
# Mock rationale: To make the 'delete' test deterministic and non-interactive, we pipe 'yes' to the script.
# This simulates a user confirming the deletion without actual manual input.
run_test \
    "Delete: remove > 7 days" \
    "yes | $SCRIPT_PATH \"$TEST_DIR\" 7 delete" \
    "Removing '$TEST_DIR/old_file_1.txt'.*Removing '$TEST_DIR/old file with spaces.log'.*Deletion complete." \
    0

# Verify files are actually deleted after Test 5
if [[ -f "$TEST_DIR/old_file_1.txt" || -f "$TEST_DIR/old file with spaces.log" ]]; then
    echo "FAIL: Files not deleted after 'delete' test." >&2
    exit 1
else
    echo "Verification: Files deleted successfully. PASS"
fi

# Test 6: Invalid directory
run_test \
    "Invalid directory" \
    "$SCRIPT_PATH /nonexistent/path 1 dry-run" \
    "Error: Directory '/nonexistent/path' not found or is not a directory." \
    1

# Test 7: Invalid age (non-integer)
run_test \
    "Invalid age (non-integer)" \
    "$SCRIPT_PATH \"$TEST_DIR\" abc dry-run" \
    "Error: Age in days must be a non-negative integer." \
    1

# Test 8: Invalid age (negative)
run_test \
    "Invalid age (negative)" \
    "$SCRIPT_PATH \"$TEST_DIR\" -5 dry-run" \
    "Error: Age in days must be a non-negative integer." \
    1

# Test 9: Invalid action
run_test \
    "Invalid action" \
    "$SCRIPT_PATH \"$TEST_DIR\" 1 invalid-action" \
    "Error: Invalid action specified. Must be 'dry-run' or 'delete'." \
    1

# Test 10: Delete with 'no' confirmation
# Recreate a file for this test
touch -d "10 days ago" "$TEST_DIR/another_old_file.txt"
run_test \
    "Delete: 'no' confirmation" \
    "echo 'n' | $SCRIPT_PATH \"$TEST_DIR\" 5 delete" \
    "Deletion cancelled." \
    0

# Verify file is NOT deleted after 'no' confirmation
if [[ ! -f "$TEST_DIR/another_old_file.txt" ]]; then
    echo "FAIL: File deleted despite 'no' confirmation." >&2
    exit 1
else
    echo "Verification: File not deleted after 'no' confirmation. PASS"
fi

echo "All tests completed."
