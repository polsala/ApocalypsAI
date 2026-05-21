#!/bin/bash

# Nightly Digital Dust Sweeper Tests

# Mock rationale:
# We create a temporary directory structure with files and directories
# having specific modification times. This allows us to deterministically
# test the script's filtering logic without relying on the actual system
# clock or modifying real user files. The 'touch -d' command is used to
# set precise timestamps.

TEST_DIR="test_temp_dust_bunnies"
SCRIPT_PATH="./src/dust_sweeper.sh"

# --- Helper Functions ---
setup_test_env() {
    mkdir -p "$TEST_DIR"
    # Create files/dirs with specific modification times
    # Current date - 100 days (older than default 90)
    touch -d "100 days ago" "$TEST_DIR/old_file_1.txt"
    mkdir -p "$TEST_DIR/old_dir_1"
    touch -d "100 days ago" "$TEST_DIR/old_dir_1"
    touch -d "100 days ago" "$TEST_DIR/old_dir_1/nested_old_file.log"

    # Current date - 50 days (younger than default 90)
    touch -d "50 days ago" "$TEST_DIR/recent_file.txt"
    mkdir -p "$TEST_DIR/recent_dir"
    touch -d "50 days ago" "$TEST_DIR/recent_dir"

    # Current date - 10 days (very recent)
    touch -d "10 days ago" "$TEST_DIR/very_recent_file.txt"

    # File exactly 90 days old (should NOT be included by +90)
    touch -d "90 days ago" "$TEST_DIR/exactly_90_days_file.txt"
}

cleanup_test_env() {
    rm -rf "$TEST_DIR"
}

assert_contains() {
    local expected="$1"
    local actual="$2"
    if ! echo "$actual" | grep -qF "$expected"; then
        echo "FAIL: Expected output to contain '$expected', but it did not."
        echo "Actual output:"
        echo "$actual"
        exit 1
    fi
}

assert_not_contains() {
    local unexpected="$1"
    local actual="$2"
    if echo "$actual" | grep -qF "$unexpected"; then
        echo "FAIL: Expected output NOT to contain '$unexpected', but it did."
        echo "Actual output:"
        echo "$actual"
        exit 1
    fi
}

# --- Test Cases ---

# Test 1: Default age (90 days)
test_default_age() {
    echo "Running Test 1: Default age (90 days)"
    setup_test_env
    OUTPUT=$("$SCRIPT_PATH" "$TEST_DIR")
    
    assert_contains "old_file_1.txt" "$OUTPUT"
    assert_contains "old_dir_1" "$OUTPUT"
    assert_contains "nested_old_file.log" "$OUTPUT" # Should find nested old file

    assert_not_contains "recent_file.txt" "$OUTPUT"
    assert_not_contains "recent_dir" "$OUTPUT"
    assert_not_contains "very_recent_file.txt" "$OUTPUT"
    assert_not_contains "exactly_90_days_file.txt" "$OUTPUT" # +90 means > 90 days

    cleanup_test_env
    echo "Test 1 Passed."
}

# Test 2: Custom age (e.g., 60 days)
test_custom_age() {
    echo "Running Test 2: Custom age (60 days)"
    setup_test_env
    OUTPUT=$("$SCRIPT_PATH" "$TEST_DIR" 60) # Should include 100-day old files, but not 50-day old ones
    
    assert_contains "old_file_1.txt" "$OUTPUT"
    assert_contains "old_dir_1" "$OUTPUT"
    assert_contains "nested_old_file.log" "$OUTPUT"

    assert_not_contains "recent_file.txt" "$OUTPUT" # 50 days old, not > 60
    assert_not_contains "recent_dir" "$OUTPUT"
    assert_not_contains "very_recent_file.txt" "$OUTPUT"
    assert_not_contains "exactly_90_days_file.txt" "$OUTPUT" # Still not > 60

    cleanup_test_env
    echo "Test 2 Passed."
}

# Test 3: Custom age (e.g., 30 days) - should include 50-day old files
test_custom_age_lower() {
    echo "Running Test 3: Custom age (30 days)"
    setup_test_env
    OUTPUT=$("$SCRIPT_PATH" "$TEST_DIR" 30) # Should include 100-day and 50-day old files
    
    assert_contains "old_file_1.txt" "$OUTPUT"
    assert_contains "old_dir_1" "$OUTPUT"
    assert_contains "nested_old_file.log" "$OUTPUT"
    assert_contains "recent_file.txt" "$OUTPUT" # Now 50 days old is > 30
    assert_contains "recent_dir" "$OUTPUT"

    assert_not_contains "very_recent_file.txt" "$OUTPUT" # 10 days old, not > 30
    assert_not_contains "exactly_90_days_file.txt" "$OUTPUT" # Still not > 30

    cleanup_test_env
    echo "Test 3 Passed."
}

# Test 4: Invalid path
test_invalid_path() {
    echo "Running Test 4: Invalid path"
    cleanup_test_env # Ensure no test dir exists
    OUTPUT=$("$SCRIPT_PATH" "non_existent_path" 2>&1) # Redirect stderr to stdout
    assert_contains "Error: Target path 'non_existent_path' is not a valid directory." "$OUTPUT"
    echo "Test 4 Passed."
}

# Test 5: Invalid age (non-numeric)
test_invalid_age_non_numeric() {
    echo "Running Test 5: Invalid age (non-numeric)"
    setup_test_env
    OUTPUT=$("$SCRIPT_PATH" "$TEST_DIR" "abc" 2>&1)
    assert_contains "Error: Age in days must be a positive integer." "$OUTPUT"
    cleanup_test_env
    echo "Test 5 Passed."
}

# Test 6: Invalid age (zero)
test_invalid_age_zero() {
    echo "Running Test 6: Invalid age (zero)"
    setup_test_env
    OUTPUT=$("$SCRIPT_PATH" "$TEST_DIR" 0 2>&1)
    assert_contains "Error: Age in days must be a positive integer." "$OUTPUT"
    cleanup_test_env
    echo "Test 6 Passed."
}

# Test 7: No arguments
test_no_arguments() {
    echo "Running Test 7: No arguments"
    OUTPUT=$("$SCRIPT_PATH" 2>&1)
    assert_contains "Usage: $SCRIPT_PATH <path> [age_in_days]" "$OUTPUT"
    echo "Test 7 Passed."
}


# Run all tests
echo "Starting Nightly Digital Dust Sweeper Tests..."
test_default_age
test_custom_age
test_custom_age_lower
test_invalid_path
test_invalid_age_non_numeric
test_invalid_age_zero
test_no_arguments
echo "All Nightly Digital Dust Sweeper Tests Passed!"
