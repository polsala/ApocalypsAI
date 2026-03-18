#!/bin/bash

# Test suite for Nightly Digital Dust Duster

SCRIPT_PATH="./src/dust_duster.sh"
TEST_DIR="test_temp_dir"

# Mock rationale: The tests create a temporary directory structure and populate it with files
# using standard shell commands like `mkdir`, `touch`, and `echo`. This simulates a real
# filesystem environment without interacting with the actual system or requiring external
# network access. The `find` command within the script operates purely on this
# isolated, deterministic test environment. File modification times are explicitly set
# using `touch -d` to ensure consistent test results regardless of when the tests are run.

# Setup function
setup() {
    mkdir -p "$TEST_DIR/subdir1" "$TEST_DIR/subdir2"
    
    # Create files with specific modification dates and sizes
    # Current date - 100 days (old file), small size (~14 bytes)
    echo "small content" > "$TEST_DIR/old_file_small.txt"
    touch -d "100 days ago" "$TEST_DIR/old_file_small.txt"
    
    # Current date - 100 days, larger file (2KB)
    head -c 2048 /dev/urandom > "$TEST_DIR/old_file_large.bin"
    touch -d "100 days ago" "$TEST_DIR/old_file_large.bin"

    # Current date - 50 days (medium age file), small size (~16 bytes)
    echo "medium content" > "$TEST_DIR/subdir1/medium_file.log"
    touch -d "50 days ago" "$TEST_DIR/subdir1/medium_file.log"

    # Current date - 5 days (recent file), small size (~16 bytes)
    echo "recent content" > "$TEST_DIR/subdir2/recent_file.conf"
    touch -d "5 days ago" "$TEST_DIR/subdir2/recent_file.conf"

    # File with spaces in name, old (120 days), small size (~20 bytes)
    echo "content with spaces" > "$TEST_DIR/file with spaces.txt"
    touch -d "120 days ago" "$TEST_DIR/file with spaces.txt"

    # Large file, but recent (5 days), size ~5KB
    head -c 5000 /dev/urandom > "$TEST_DIR/recent_large.data"
    touch -d "5 days ago" "$TEST_DIR/recent_large.data"

    # Small file, very old (200 days), tiny size (~5 bytes)
    echo "tiny" > "$TEST_DIR/very_old_tiny.log"
    touch -d "200 days ago" "$TEST_DIR/very_old_tiny.log"
}

# Teardown function
teardown() {
    rm -rf "$TEST_DIR"
}

# Test function template
run_test() {
    local test_name="$1"
    local command="$2"
    local expected_output_regex="$3"
    local expected_exit_code="${4:-0}" # Default exit code is 0

    echo "Running test: $test_name"
    output=$(eval "$command" 2>&1)
    exit_code=$?

    if [ "$exit_code" -ne "$expected_exit_code" ]; then
        echo "FAIL: $test_name - Expected exit code $expected_exit_code, got $exit_code" >&2
        echo "Output:" >&2
        echo "$output" >&2
        return 1
    fi

    if [ -n "$expected_output_regex" ] && ! echo "$output" | grep -Eq "$expected_output_regex"; then
        echo "FAIL: $test_name - Output did not match expected regex." >&2
        echo "Expected regex: $expected_output_regex" >&2
        echo "Output:" >&2
        echo "$output" >&2
        return 1
    fi

    echo "PASS: $test_name"
    return 0
}

# --- Test Cases ---

# Test 1: No arguments - should show usage
test_no_args() {
    run_test "No arguments" "$SCRIPT_PATH" "Usage: ./src/dust_duster.sh <directory> <age_in_days> \[min_size_in_kb\]" 1
}

# Test 2: Invalid directory
test_invalid_dir() {
    run_test "Invalid directory" "$SCRIPT_PATH /nonexistent_dir 10" "Error: Directory '/nonexistent_dir' not found." 1
}

# Test 3: Invalid age (non-numeric)
test_invalid_age_non_numeric() {
    run_test "Invalid age (non-numeric)" "$SCRIPT_PATH $TEST_DIR abc" "Error: Age in days must be a positive integer." 1
}

# Test 4: Invalid age (zero)
test_invalid_age_zero() {
    run_test "Invalid age (zero)" "$SCRIPT_PATH $TEST_DIR 0" "Error: Age in days must be a positive integer." 1
}

# Test 5: Find files older than 60 days (should find old_file_small, old_file_large, file with spaces, very_old_tiny)
test_find_old_files() {
    local expected_regex="old_file_small.txt.*old_file_large.bin.*file with spaces.txt.*very_old_tiny.log"
    run_test "Find files older than 60 days" "$SCRIPT_PATH $TEST_DIR 60" "$expected_regex"
}

# Test 6: Find files older than 150 days (should find file with spaces, very_old_tiny)
test_find_very_old_files() {
    local expected_regex="file with spaces.txt.*very_old_tiny.log"
    local unexpected_regex="old_file_small.txt|old_file_large.bin|medium_file.log|recent_file.conf|recent_large.data"
    
    output=$($SCRIPT_PATH "$TEST_DIR" 150)
    exit_code=$?

    if [ "$exit_code" -ne 0 ]; then
        echo "FAIL: Test 6 - Expected exit code 0, got $exit_code" >&2
        echo "Output:" >&2
        echo "$output" >&2
        return 1
    fi

    if ! echo "$output" | grep -Eq "$expected_regex"; then
        echo "FAIL: Test 6 - Output did not contain expected files." >&2
        echo "Expected regex: $expected_regex" >&2
        echo "Output:" >&2
        echo "$output" >&2
        return 1
    fi

    if echo "$output" | grep -Eq "$unexpected_regex"; then
        echo "FAIL: Test 6 - Output contained unexpected files." >&2
        echo "Unexpected regex: $unexpected_regex" >&2
        echo "Output:" >&2
        echo "$output" >&2
        return 1
    fi
    echo "PASS: Test 6 - Find files older than 150 days"
    return 0
}


# Test 7: Find files older than 60 days and larger than 1KB (1024 bytes)
# Only old_file_large.bin (2KB, 100 days old) should match.
test_find_old_and_large_files() {
    local expected_regex="old_file_large.bin"
    local unexpected_regex="old_file_small.txt|medium_file.log|recent_file.conf|file with spaces.txt|recent_large.data|very_old_tiny.log"

    output=$($SCRIPT_PATH "$TEST_DIR" 60 1) # 1KB
    exit_code=$?

    if [ "$exit_code" -ne 0 ]; then
        echo "FAIL: Test 7 - Expected exit code 0, got $exit_code" >&2
        echo "Output:" >&2
        echo "$output" >&2
        return 1
    fi

    if ! echo "$output" | grep -Eq "$expected_regex"; then
        echo "FAIL: Test 7 - Output did not contain expected large file." >&2
        echo "Expected regex: $expected_regex" >&2
        echo "Output:" >&2
        echo "$output" >&2
        return 1
    fi

    if echo "$output" | grep -Eq "$unexpected_regex"; then
        echo "FAIL: Test 7 - Output contained unexpected small files." >&2
        echo "Unexpected regex: $unexpected_regex" >&2
        echo "Output:" >&2
        echo "$output" >&2
        return 1
    fi
    echo "PASS: Test 7 - Find files older than 60 days and larger than 1KB"
    return 0
}

# Test 8: No matching files
test_no_matches() {
    local expected_regex="Digital dust duster complete. Happy scavenging!"
    local unexpected_regex="Path:"

    output=$($SCRIPT_PATH "$TEST_DIR" 10 10000) # Older than 10 days, larger than 10MB (no such file)
    exit_code=$?

    if [ "$exit_code" -ne 0 ]; then
        echo "FAIL: Test 8 - Expected exit code 0, got $exit_code" >&2
        echo "Output:" >&2
        echo "$output" >&2
        return 1
    fi

    if ! echo "$output" | grep -Eq "$expected_regex"; then
        echo "FAIL: Test 8 - Output did not contain completion message." >&2
        echo "Expected regex: $expected_regex" >&2
        echo "Output:" >&2
        echo "$output" >&2
        return 1
    fi

    if echo "$output" | grep -Eq "$unexpected_regex"; then
        echo "FAIL: Test 8 - Output contained unexpected file paths." >&2
        echo "Unexpected regex: $unexpected_regex" >&2
        echo "Output:" >&2
        echo "$output" >&2
        return 1
    fi
    echo "PASS: Test 8 - No matching files"
    return 0
}

# Test 9: Invalid min_size_in_kb (non-numeric)
test_invalid_size_non_numeric() {
    run_test "Invalid size (non-numeric)" "$SCRIPT_PATH $TEST_DIR 10 abc" "Error: Minimum size in KB must be a positive integer." 1
}

# Test 10: Invalid min_size_in_kb (zero)
test_invalid_size_zero() {
    run_test "Invalid size (zero)" "$SCRIPT_PATH $TEST_DIR 10 0" "Error: Minimum size in KB must be a positive integer." 1
}

# Test 11: File with spaces in name is correctly reported
test_file_with_spaces() {
    local expected_regex="file with spaces.txt"
    run_test "File with spaces in name" "$SCRIPT_PATH $TEST_DIR 100" "$expected_regex"
}

# --- Main test execution ---
total_tests=0
failed_tests=0

echo "--- Starting Nightly Digital Dust Duster Tests ---"

teardown # Clean up any previous test runs
setup    # Set up test environment

test_no_args && ((total_tests++)) || ((failed_tests++))
test_invalid_dir && ((total_tests++)) || ((failed_tests++))
test_invalid_age_non_numeric && ((total_tests++)) || ((failed_tests++))
test_invalid_age_zero && ((total_tests++)) || ((failed_tests++))
test_find_old_files && ((total_tests++)) || ((failed_tests++))
test_find_very_old_files && ((total_tests++)) || ((failed_tests++))
test_find_old_and_large_files && ((total_tests++)) || ((failed_tests++))
test_no_matches && ((total_tests++)) || ((failed_tests++))
test_invalid_size_non_numeric && ((total_tests++)) || ((failed_tests++))
test_invalid_size_zero && ((total_tests++)) || ((failed_tests++))
test_file_with_spaces && ((total_tests++)) || ((failed_tests++))

teardown # Clean up after tests

echo "--- Test Summary ---"
echo "Total tests run: $total_tests"
echo "Tests passed: $((total_tests - failed_tests))"
echo "Tests failed: $failed_tests"

if [ "$failed_tests" -eq 0 ]; then
    echo "All tests passed successfully!"
    exit 0
else
    echo "Some tests failed."
    exit 1
fi
