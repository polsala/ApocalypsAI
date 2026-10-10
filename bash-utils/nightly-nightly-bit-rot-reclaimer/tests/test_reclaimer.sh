#!/bin/bash

# Test suite for nightly-bit-rot-reclaimer

# Set up a temporary test directory
TEST_DIR="$(mktemp -d)"
SCRIPT_PATH="$(dirname "$0")"/../src/reclaimer.sh

# Mock rationale: `stat` command output format can vary between systems (Linux vs macOS).
# For deterministic tests, we'll simplify the output verification to focus on file paths
# and ensure the `find` logic correctly identifies files based on age/size.
# The human-readable size/date formatting is assumed to work correctly if `stat` is present.

# Helper function to create a file with specific modification time and size
create_test_file() {
    local filename="$1"
    local mod_date="$2" # YYYY-MM-DD
    local size_bytes="$3"

    # Create file with specified size
    dd if=/dev/zero of="$filename" bs=1 count="$size_bytes" > /dev/null 2>&1
    # Set modification date
    touch -d "$mod_date" "$filename"
}

# Helper function to run the script and capture output
run_reclaimer() {
    (cd "$TEST_DIR" && "$SCRIPT_PATH" "$@")
}

# Test counter
TEST_COUNT=0
PASSED_COUNT=0

# Assertion function
assert_contains() {
    TEST_COUNT=$((TEST_COUNT + 1))
    local output="$1"
    local expected_string="$2"
    local test_name="$3"
    if echo "$output" | grep -qF "$expected_string"; then
        echo "✓ Test Passed: $test_name"
        PASSED_COUNT=$((PASSED_COUNT + 1))
    else
        echo "✗ Test Failed: $test_name"
        echo "  Expected to contain: '$expected_string'"
        echo "  Actual output:" >&2
        echo "$output" >&2
    fi
}

assert_not_contains() {
    TEST_COUNT=$((TEST_COUNT + 1))
    local output="$1"
    local unexpected_string="$2"
    local test_name="$3"
    if ! echo "$output" | grep -qF "$unexpected_string"; then
        echo "✓ Test Passed: $test_name"
        PASSED_COUNT=$((PASSED_COUNT + 1))
    else
        echo "✗ Test Failed: $test_name"
        echo "  Expected NOT to contain: '$unexpected_string'"
        echo "  Actual output:" >&2
        echo "$output" >&2
    fi
}

# --- Test Cases ---

# Test 1: Default parameters (age 365 days, size 100MB)
setup_test_1() {
    mkdir -p "$TEST_DIR/subdir"
    create_test_file "$TEST_DIR/old_large.log" "2022-01-01" $((101 * 1024 * 1024)) # 101MB, ~2 years old
    create_test_file "$TEST_DIR/old_small.txt" "2022-01-01" $((10 * 1024)) # 10KB, ~2 years old
    create_test_file "$TEST_DIR/new_large.bin" "$(date +%Y-%m-%d)" $((101 * 1024 * 1024)) # 101MB, today
    create_test_file "$TEST_DIR/new_small.csv" "$(date +%Y-%m-%d)" $((10 * 1024)) # 10KB, today
    create_test_file "$TEST_DIR/subdir/another_old_large.zip" "2022-01-01" $((200 * 1024 * 1024)) # 200MB, ~2 years old
}

run_test_1() {
    setup_test_1
    local output=$(run_reclaimer)
    assert_contains "$output" "old_large.log" "Test 1.1: Default - Should find old_large.log"
    assert_contains "$output" "old_small.txt" "Test 1.2: Default - Should find old_small.txt (due to age)"
    assert_contains "$output" "subdir/another_old_large.zip" "Test 1.3: Default - Should find subdir/another_old_large.zip"
    assert_not_contains "$output" "new_large.bin" "Test 1.4: Default - Should NOT find new_large.bin (too new)"
    assert_not_contains "$output" "new_small.csv" "Test 1.5: Default - Should NOT find new_small.csv (too new and too small)"
}

# Test 2: Custom age (e.g., 90 days)
setup_test_2() {
    create_test_file "$TEST_DIR/recent_old.data" "$(date -d '91 days ago' +%Y-%m-%d)" $((1 * 1024 * 1024)) # 1MB, 91 days old
    create_test_file "$TEST_DIR/very_recent.data" "$(date -d '89 days ago' +%Y-%m-%d)" $((1 * 1024 * 1024)) # 1MB, 89 days old
}

run_test_2() {
    setup_test_2
    local output=$(run_reclaimer --age 90 --size 0)
    assert_contains "$output" "recent_old.data" "Test 2.1: Custom Age - Should find recent_old.data"
    assert_not_contains "$output" "very_recent.data" "Test 2.2: Custom Age - Should NOT find very_recent.data"
}

# Test 3: Custom size (e.g., 5MB)
setup_test_3() {
    create_test_file "$TEST_DIR/large_file.img" "$(date -d '2 years ago' +%Y-%m-%d)" $((6 * 1024 * 1024)) # 6MB, ~2 years old
    create_test_file "$TEST_DIR/small_file.img" "$(date -d '2 years ago' +%Y-%m-%d)" $((4 * 1024 * 1024)) # 4MB, ~2 years old
}

run_test_3() {
    setup_test_3
    local output=$(run_reclaimer --age 0 --size 5)
    assert_contains "$output" "large_file.img" "Test 3.1: Custom Size - Should find large_file.img"
    assert_not_contains "$output" "small_file.img" "Test 3.2: Custom Size - Should NOT find small_file.img"
}

# Test 4: Custom path
setup_test_4() {
    mkdir -p "$TEST_DIR/custom_path"
    create_test_file "$TEST_DIR/custom_path/old_file.log" "2022-01-01" $((101 * 1024 * 1024)) # 101MB, ~2 years old
    create_test_file "$TEST_DIR/not_in_path.txt" "2022-01-01" $((101 * 1024 * 1024)) # 101MB, ~2 years old
}

run_test_4() {
    setup_test_4
    local output=$(run_reclaimer --path "$TEST_DIR/custom_path")
    assert_contains "$output" "old_file.log" "Test 4.1: Custom Path - Should find old_file.log"
    assert_not_contains "$output" "not_in_path.txt" "Test 4.2: Custom Path - Should NOT find not_in_path.txt"
}

# Test 5: Dry run
run_test_5() {
    local output=$(run_reclaimer --dry-run)
    assert_contains "$output" "Dry run: The following command would be executed:" "Test 5.1: Dry Run - Should indicate dry run"
    assert_contains "$output" "find \"$TEST_DIR\" -type f \( -mtime +365 -o -size +100M \) -print0" "Test 5.2: Dry Run - Should show correct find command"
}

# Test 6: No matching files
setup_test_6() {
    create_test_file "$TEST_DIR/recent_small.txt" "$(date +%Y-%m-%d)" $((10 * 1024)) # 10KB, today
}

run_test_6() {
    setup_test_6
    local output=$(run_reclaimer)
    assert_not_contains "$output" "recent_small.txt" "Test 6.1: No Match - Should not find recent_small.txt"
    assert_contains "$output" "Reclamation Report for" "Test 6.2: No Match - Should still print header"
}

# Test 7: Invalid path
run_test_7() {
    local output=$(run_reclaimer --path "$TEST_DIR/non_existent_dir" 2>&1)
    assert_contains "$output" "Error: Directory '$TEST_DIR/non_existent_dir' not found." "Test 7.1: Invalid Path - Should report error"
}

# --- Main Test Execution ---
echo "Running tests for Nightly Bit Rot Reclaimer..."

# Run all tests
run_test_1
rm -rf "$TEST_DIR"/* # Clean up for next test
run_test_2
rm -rf "$TEST_DIR"/*
run_test_3
rm -rf "$TEST_DIR"/*
run_test_4
rm -rf "$TEST_DIR"/*
run_test_5
rm -rf "$TEST_DIR"/*
run_test_6
rm -rf "$TEST_DIR"/*
run_test_7

# Final cleanup
rm -rf "$TEST_DIR"

echo "\n--- Test Summary ---"
echo "$PASSED_COUNT out of $TEST_COUNT tests passed."

if [ "$PASSED_COUNT" -eq "$TEST_COUNT" ]; then
    echo "All tests passed!"
    exit 0
else
    echo "Some tests failed."
    exit 1
fi
