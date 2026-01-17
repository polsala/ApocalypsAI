#!/bin/bash

# Test script for nightly-digital-decay-detect

SCRIPT_PATH="../src/detect_decay.sh"
TEST_DIR="test_decay_data"

# Mock rationale: We need to control the filesystem state and file modification times
# to ensure deterministic test results. Creating temporary files and setting their
# modification times allows us to simulate "decay" without relying on the actual
# system's file ages or modifying real user data. This ensures tests are offline and deterministic.

# Setup function
setup() {
    mkdir -p "$TEST_DIR"
    # Create a file modified 100 days ago (older than default 90)
    touch -m -d "100 days ago" "$TEST_DIR/old_file.txt"
    # Create a directory modified 100 days ago
    mkdir -p "$TEST_DIR/old_dir"
    touch -m -d "100 days ago" "$TEST_DIR/old_dir"
    # Create a file modified 50 days ago (newer than default 90)
    touch -m -d "50 days ago" "$TEST_DIR/recent_file.log"
    # Create a directory modified 50 days ago
    mkdir -p "$TEST_DIR/recent_dir"
    touch -m -d "50 days ago" "$TEST_DIR/recent_dir"
    # Create a file with spaces in its name, modified 100 days ago
    touch -m -d "100 days ago" "$TEST_DIR/old file with spaces.doc"
    # Create a file inside an old directory
    touch -m -d "100 days ago" "$TEST_DIR/old_dir/nested_old_file.conf"
}

# Teardown function
teardown() {
    rm -rf "$TEST_DIR"
}

# Generic test runner function for simple regex checks
run_test() {
    local name="$1"
    local command="$2"
    local expected_output_regex="$3"
    local expected_exit_code="${4:-0}"

    echo "--- Running Test: $name ---"
    output=$(eval "$command" 2>&1)
    exit_code=$?

    if [[ $exit_code -ne $expected_exit_code ]]; then
        echo "FAIL: $name - Expected exit code $expected_exit_code, got $exit_code"
        echo "Output: $output"
        return 1
    fi

    if [[ "$output" =~ $expected_output_regex ]]; then
        echo "PASS: $name"
    else
        echo "FAIL: $name"
        echo "Expected regex: $expected_output_regex"
        echo "Actual output:"
        echo "$output"
        return 1
    fi
    return 0
}

# --- Test Cases ---

# Test 1: Default scan, summary report (expect 3 decayed items: 2 files, 1 dir)
test_default_summary() {
    local cmd="$SCRIPT_PATH -p $TEST_DIR"
    local regex="Scanning: $TEST_DIR\nThreshold: 90 days of inactivity\nReport Type: summary\n.*\nFiles showing signs of 'Forgotten Tomes' \(2 found\):\nDirectories resembling 'Ancient Relics' \(1 found\):\n\nTotal 'Digital Decay' items: 3"
    run_test "Default summary report" "$cmd" "$regex"
}

# Test 2: Detailed report (expect specific files/dirs listed, order-independent check)
test_detailed_report() {
    local cmd="$SCRIPT_PATH -p $TEST_DIR -t detailed"
    local output=$(eval "$cmd" 2>&1)
    local exit_code=$?
    local name="Detailed report"

    if [[ $exit_code -ne 0 ]]; then
        echo "FAIL: $name - Expected exit code 0, got $exit_code"
        echo "Output: $output"
        return 1
    fi

    echo "--- Running Test: $name ---"

    # Check for header and summary lines
    if ! echo "$output" | grep -q "Scanning: $TEST_DIR"; then echo "FAIL: $name - Missing scan path"; return 1; fi
    if ! echo "$output" | grep -q "Threshold: 90 days of inactivity"; then echo "FAIL: $name - Missing threshold"; return 1; fi
    if ! echo "$output" | grep -q "Report Type: detailed"; then echo "FAIL: $name - Missing report type"; return 1; fi
    if ! echo "$output" | grep -q "Files showing signs of 'Forgotten Tomes' (2 found):"; then echo "FAIL: $name - Missing file count"; return 1; fi
    if ! echo "$output" | grep -q "Directories resembling 'Ancient Relics' (1 found):"; then echo "FAIL: $name - Missing dir count"; return 1; fi
    if ! echo "$output" | grep -q "Total 'Digital Decay' items: 3"; then echo "FAIL: $name - Missing total count"; return 1; fi

    # Check for specific files/dirs (order-independent)
    if ! echo "$output" | grep -q "  - $TEST_DIR/old_file.txt"; then echo "FAIL: $name - Missing old_file.txt"; return 1; fi
    if ! echo "$output" | grep -q "  - $TEST_DIR/old file with spaces.doc"; then echo "FAIL: $name - Missing 'old file with spaces.doc'"; return 1; fi
    if ! echo "$output" | grep -q "  - $TEST_DIR/old_dir"; then echo "FAIL: $name - Missing old_dir"; return 1; fi

    echo "PASS: $name"
    return 0
}

# Test 3: Custom days (e.g., 60 days, expect all 4 items: 2 files, 2 dirs)
test_custom_days() {
    local cmd="$SCRIPT_PATH -p $TEST_DIR -d 60"
    local regex="Scanning: $TEST_DIR\nThreshold: 60 days of inactivity\nReport Type: summary\n.*\nFiles showing signs of 'Forgotten Tomes' \(2 found\):\nDirectories resembling 'Ancient Relics' \(2 found\):\n\nTotal 'Digital Decay' items: 4"
    run_test "Custom days (60)" "$cmd" "$regex"
}

# Test 4: No decay found (set threshold very high)
test_no_decay() {
    local cmd="$SCRIPT_PATH -p $TEST_DIR -d 120"
    local regex="No significant digital decay detected. Your system is spick and span!"
    run_test "No decay found" "$cmd" "$regex"
}

# Test 5: Invalid path
test_invalid_path() {
    local cmd="$SCRIPT_PATH -p non_existent_dir"
    local regex="Error: Target path 'non_existent_dir' does not exist or is not a directory."
    run_test "Invalid path" "$cmd" "$regex" 1
}

# Test 6: Invalid days (non-numeric)
test_invalid_days_non_numeric() {
    local cmd="$SCRIPT_PATH -d abc"
    local regex="Error: Days must be a positive integer."
    run_test "Invalid days (abc)" "$cmd" "$regex" 1
}

# Test 7: Invalid days (zero)
test_invalid_days_zero() {
    local cmd="$SCRIPT_PATH -d 0"
    local regex="Error: Days must be a positive integer."
    run_test "Invalid days (0)" "$cmd" "$regex" 1
}

# Test 8: Invalid report type
test_invalid_report_type() {
    local cmd="$SCRIPT_PATH -t invalid"
    local regex="Error: Report type must be 'summary' or 'detailed'."
    run_test "Invalid report type" "$cmd" "$regex" 1
}

# Main test execution
main() {
    setup
    local failures=0

    test_default_summary || failures=$((failures + 1))
    test_detailed_report || failures=$((failures + 1))
    test_custom_days || failures=$((failures + 1))
    test_no_decay || failures=$((failures + 1))
    test_invalid_path || failures=$((failures + 1))
    test_invalid_days_non_numeric || failures=$((failures + 1))
    test_invalid_days_zero || failures=$((failures + 1))
    test_invalid_report_type || failures=$((failures + 1))

    teardown

    if [ "$failures" -eq 0 ]; then
        echo "\nAll tests passed!"
        exit 0
    else
        echo "\n$failures test(s) failed."
        exit 1
    fi
}

main
