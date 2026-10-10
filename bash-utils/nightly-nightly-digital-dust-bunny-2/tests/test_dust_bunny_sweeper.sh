#!/bin/bash

# Test script for nightly-digital-dust-bunny

# --- Test Setup ---
TEST_DIR=$(mktemp -d)
SCRIPT_PATH="$(dirname "$0")"/../src/dust_bunny_sweeper.sh
REPORT_FILE="${TEST_DIR}/report.txt"

# Mock rationale: Using temporary files and actual system commands (find, du, md5sum, stat, date, dd, touch)
# is deterministic and offline. It simulates real-world conditions without external dependencies.
# We create specific file states (large, old, duplicate) to trigger the script's logic.
# The 'stat' command behavior is conditionally handled for Linux/macOS within the main script,
# ensuring tests are robust across common environments.

# Create test files
create_test_files() {
    # Large file (e.g., 60MB, >50MB threshold)
    dd if=/dev/zero of="${TEST_DIR}/large_file.bin" bs=1M count=60 >/dev/null 2>&1

    # Old file (e.g., 200 days old, >180 days threshold)
    # Use a fixed date in the past for determinism, handling both GNU and BSD date syntaxes
    touch -t $(date -v-200d +%Y%m%d%H%M.%S 2>/dev/null || date -d "200 days ago" +%Y%m%d%H%M.%S) "${TEST_DIR}/old_log.txt"

    # Duplicate files
    echo "content for duplicate A" > "${TEST_DIR}/duplicate_a.txt"
    echo "content for duplicate A" > "${TEST_DIR}/copy_of_duplicate_a.txt"
    echo "content for duplicate B" > "${TEST_DIR}/duplicate_b.txt"
    echo "content for duplicate B" > "${TEST_DIR}/another_copy_of_duplicate_b.txt"

    # Normal file (should not be reported)
    echo "normal content" > "${TEST_DIR}/normal_file.txt"
    dd if=/dev/zero of="${TEST_DIR}/small_recent_file.bin" bs=1M count=10 >/dev/null 2>&1
}

# --- Test Functions ---

run_test() {
    local test_name="$1"
    local expected_output_regex="$2"
    local unexpected_output_regex="$3"
    local script_args="$4"

    echo "Running test: $test_name"
    
    # Run the script and capture output
    bash "$SCRIPT_PATH" $script_args "$TEST_DIR" > "$REPORT_FILE" 2>&1
    local exit_code=$?
    local output=$(cat "$REPORT_FILE")

    if [ $exit_code -ne 0 ]; then
        echo "FAIL: Script exited with non-zero status $exit_code for $test_name."
        echo "Output:"
        echo "$output"
        return 1
    fi

    if [[ "$output" =~ $expected_output_regex ]]; then
        echo "PASS: Expected output found for $test_name."
    else
        echo "FAIL: Expected output NOT found for $test_name."
        echo "Expected regex: '$expected_output_regex'"
        echo "Actual output:"
        echo "$output"
        return 1
    fi

    if [ -n "$unexpected_output_regex" ] && [[ "$output" =~ $unexpected_output_regex ]]; then
        echo "FAIL: Unexpected output found for $test_name."
        echo "Unexpected regex: '$unexpected_output_regex'"
        echo "Actual output:"
        echo "$output"
        return 1
    else
        echo "PASS: Unexpected output NOT found for $test_name."
    fi
    return 0
}

# --- Main Test Execution ---

echo "Starting tests for nightly-digital-dust-bunny..."

# Clean up any previous test artifacts
cleanup() {
    rm -rf "$TEST_DIR"
    echo "Cleaned up test directory: $TEST_DIR"
}
trap cleanup EXIT # Ensure cleanup runs on exit

create_test_files

# Test 1: Basic scan, check for all categories
run_test "Full scan with default thresholds" \
    "### Large Files.*large_file.bin.*### Old Files.*old_log.txt.*### Duplicate Files.*duplicate_a.txt.*copy_of_duplicate_a.txt.*duplicate_b.txt.*another_copy_of_duplicate_b.txt" \
    "normal_file.txt|small_recent_file.bin" \
    ""
if [ $? -ne 0 ]; then exit 1; fi

# Test 2: Custom large file threshold (e.g., 70MB, large_file.bin should not be reported)
run_test "Custom large file threshold (70MB)" \
    "### Large Files.*\(No large files found\)" \
    "large_file.bin" \
    "-s 70"
if [ $? -ne 0 ]; then exit 1; fi

# Test 3: Custom old file threshold (e.g., 100 days, old_log.txt should still be reported)
run_test "Custom old file threshold (100 days)" \
    "### Old Files.*old_log.txt" \
    "" \
    "-o 100"
if [ $? -ne 0 ]; then exit 1; fi

# Test 4: Help message
HELP_OUTPUT=$(bash "$SCRIPT_PATH" -h 2>&1)
if [[ "$HELP_OUTPUT" =~ "Usage: $0 [OPTIONS] [DIRECTORY]" ]]; then
    echo "PASS: Help message displayed correctly."
else
    echo "FAIL: Help message not displayed correctly."
    echo "Output:"
    echo "$HELP_OUTPUT"
    exit 1
fi

# Test 5: Invalid directory
INVALID_DIR_OUTPUT=$(bash "$SCRIPT_PATH" /non/existent/path/to/dir 2>&1)
if [[ "$INVALID_DIR_OUTPUT" =~ "Error: Directory '/non/existent/path/to/dir' not found." ]]; then
    echo "PASS: Handles invalid directory correctly."
else
    echo "FAIL: Did not handle invalid directory correctly."
    echo "Output:"
    echo "$INVALID_DIR_OUTPUT"
    exit 1
fi

echo "All tests completed."
