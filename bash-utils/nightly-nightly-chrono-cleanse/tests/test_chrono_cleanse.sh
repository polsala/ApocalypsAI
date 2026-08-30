#!/bin/bash

# Tests for Nightly Chrono-Cleanse utility

set -euo pipefail

SCRIPT_PATH="$(dirname "$0")"/../src/chrono_cleanse.sh

# --- Test Utilities ---

# Function to assert success
assert_success() {
    local test_name="$1"
    local exit_code="$2"
    if [[ "$exit_code" -eq 0 ]]; then
        echo "✅ PASS: $test_name"
    else
        echo "❌ FAIL: $test_name (Exit Code: $exit_code)" >&2
        exit 1
    fi
}

# Function to assert failure
assert_failure() {
    local test_name="$1"
    local exit_code="$2"
    if [[ "$exit_code" -ne 0 ]]; then
        echo "✅ PASS: $test_name"
    else
        echo "❌ FAIL: $test_name (Expected non-zero, got $exit_code)" >&2
        exit 1
    fi
}

# --- Test Setup & Teardown ---

TEST_DIR="$(mktemp -d)"

cleanup() {
    echo "Cleaning up test directory: ${TEST_DIR}"
    rm -rf "${TEST_DIR}"
}

trap cleanup EXIT

# Mock rationale: We create a temporary directory structure with files of specific ages.
# This allows 'find' to operate on real files in a controlled, isolated, and deterministic environment,
# eliminating the need to mock the 'find' command itself. The environment *is* the mock.

setup_test_files() {
    local dir="$1"
    mkdir -p "$dir/subdir1"
    mkdir -p "$dir/subdir2"

    # Files older than 30 days
    touch -d "60 days ago" "$dir/old_log_file.log"
    touch -d "35 days ago" "$dir/subdir1/another_old_file.txt"
    touch -d "31 days ago" "$dir/subdir2/old_config.bak"

    # Files newer than 30 days
    touch -d "20 days ago" "$dir/recent_report.pdf"
    touch -d "5 days ago" "$dir/subdir1/current_data.csv"
    touch "$dir/new_file.tmp"

    # File with spaces in name
    touch -d "40 days ago" "$dir/file with spaces.log"

    # Ensure script is executable
    chmod +x "${SCRIPT_PATH}"
}

# --- Test Cases ---

echo "Running Nightly Chrono-Cleanse Tests..."

# Test 1: Dry run - default age (30 days)
TEST_NAME="Dry Run - Default Age (30 days)"
setup_test_files "${TEST_DIR}/test1"
OUTPUT=$( "${SCRIPT_PATH}" -n -d "${TEST_DIR}/test1" 2>&1 )
EXIT_CODE=$?
assert_success "$TEST_NAME" "$EXIT_CODE"

if ! echo "$OUTPUT" | grep -q "old_log_file.log"; then
    echo "❌ FAIL: $TEST_NAME - Expected 'old_log_file.log' in dry run output." >&2
    echo "Output:" >&2
    echo "$OUTPUT" >&2
    exit 1
fi
if ! echo "$OUTPUT" | grep -q "another_old_file.txt"; then
    echo "❌ FAIL: $TEST_NAME - Expected 'another_old_file.txt' in dry run output." >&2
    exit 1
fi
if ! echo "$OUTPUT" | grep -q "old_config.bak"; then
    echo "❌ FAIL: $TEST_NAME - Expected 'old_config.bak' in dry run output." >&2
    exit 1
fi
if ! echo "$OUTPUT" | grep -q "file with spaces.log"; then
    echo "❌ FAIL: $TEST_NAME - Expected 'file with spaces.log' in dry run output." >&2
    exit 1
fi
if echo "$OUTPUT" | grep -q "recent_report.pdf"; then
    echo "❌ FAIL: $TEST_NAME - Did not expect 'recent_report.pdf' in dry run output." >&2
    exit 1
fi
if [[ ! -f "${TEST_DIR}/test1/old_log_file.log" ]]; then
    echo "❌ FAIL: $TEST_NAME - File 'old_log_file.log' was deleted during dry run." >&2
    exit 1
fi

# Test 2: Actual run - default age (30 days)
TEST_NAME="Actual Run - Default Age (30 days)"
setup_test_files "${TEST_DIR}/test2"
OUTPUT=$( "${SCRIPT_PATH}" -d "${TEST_DIR}/test2" 2>&1 )
EXIT_CODE=$?
assert_success "$TEST_NAME" "$EXIT_CODE"

if [[ -f "${TEST_DIR}/test2/old_log_file.log" ]]; then
    echo "❌ FAIL: $TEST_NAME - File 'old_log_file.log' was not deleted." >&2
    exit 1
fi
if [[ -f "${TEST_DIR}/test2/subdir1/another_old_file.txt" ]]; then
    echo "❌ FAIL: $TEST_NAME - File 'another_old_file.txt' was not deleted." >&2
    exit 1
fi
if [[ -f "${TEST_DIR}/test2/subdir2/old_config.bak" ]]; then
    echo "❌ FAIL: $TEST_NAME - File 'old_config.bak' was not deleted." >&2
    exit 1
fi
if [[ -f "${TEST_DIR}/test2/file with spaces.log" ]]; then
    echo "❌ FAIL: $TEST_NAME - File 'file with spaces.log' was not deleted." >&2
    exit 1
fi
if [[ ! -f "${TEST_DIR}/test2/recent_report.pdf" ]]; then
    echo "❌ FAIL: $TEST_NAME - File 'recent_report.pdf' was unexpectedly deleted." >&2
    exit 1
fi

# Test 3: Actual run - custom age (7 days)
TEST_NAME="Actual Run - Custom Age (7 days)"
setup_test_files "${TEST_DIR}/test3"
OUTPUT=$( "${SCRIPT_PATH}" -a 7 -d "${TEST_DIR}/test3" 2>&1 )
EXIT_CODE=$?
assert_success "$TEST_NAME" "$EXIT_CODE"

# All files except 'new_file.tmp' and 'current_data.csv' should be gone
if [[ -f "${TEST_DIR}/test3/old_log_file.log" ]]; then exit 1; fi
if [[ -f "${TEST_DIR}/test3/subdir1/another_old_file.txt" ]]; then exit 1; fi
if [[ -f "${TEST_DIR}/test3/subdir2/old_config.bak" ]]; then exit 1; fi
if [[ -f "${TEST_DIR}/test3/recent_report.pdf" ]]; then exit 1; fi
if [[ -f "${TEST_DIR}/test3/file with spaces.log" ]]; then exit 1; fi

if [[ ! -f "${TEST_DIR}/test3/new_file.tmp" ]]; then
    echo "❌ FAIL: $TEST_NAME - File 'new_file.tmp' was unexpectedly deleted." >&2
    exit 1
fi
if [[ ! -f "${TEST_DIR}/test3/subdir1/current_data.csv" ]]; then
    echo "❌ FAIL: $TEST_NAME - File 'current_data.csv' was unexpectedly deleted." >&2
    exit 1
fi

# Test 4: Invalid directory
TEST_NAME="Invalid Directory Handling"
OUTPUT=$( "${SCRIPT_PATH}" -d "${TEST_DIR}/nonexistent_dir" 2>&1 )
EXIT_CODE=$?
assert_success "$TEST_NAME" "$EXIT_CODE" # Should exit 0 but print warning
if ! echo "$OUTPUT" | grep -q "Warning: Directory '${TEST_DIR}/nonexistent_dir' does not exist"; then
    echo "❌ FAIL: $TEST_NAME - Expected warning for nonexistent directory." >&2
    echo "Output:" >&2
    echo "$OUTPUT" >&2
    exit 1
fi

# Test 5: No directories provided
TEST_NAME="No Directories Provided"
OUTPUT=$( "${SCRIPT_PATH}" 2>&1 )
EXIT_CODE=$?
assert_failure "$TEST_NAME" "$EXIT_CODE"
if ! echo "$OUTPUT" | grep -q "Error: At least one directory must be specified with -d."; then
    echo "❌ FAIL: $TEST_NAME - Expected error for missing directory." >&2
    echo "Output:" >&2
    echo "$OUTPUT" >&2
    exit 1
fi

# Test 6: Invalid age argument
TEST_NAME="Invalid Age Argument"
OUTPUT=$( "${SCRIPT_PATH}" -a abc -d "${TEST_DIR}/test6" 2>&1 )
EXIT_CODE=$?
assert_failure "$TEST_NAME" "$EXIT_CODE"
if ! echo "$OUTPUT" | grep -q "Error: -a requires a positive integer for age in days."; then
    echo "❌ FAIL: $TEST_NAME - Expected error for invalid age." >&2
    echo "Output:" >&2
    echo "$OUTPUT" >&2
    exit 1
fi

echo "\nAll Nightly Chrono-Cleanse tests completed successfully!"
