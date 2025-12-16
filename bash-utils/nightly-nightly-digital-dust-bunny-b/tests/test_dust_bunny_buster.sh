#!/bin/bash

# tests/test_dust_bunny_buster.sh

# Path to the script under test
SCRIPT_TO_TEST="../src/dust_bunny_buster.sh"

# Temporary directory for tests
TEST_DIR=""

# Helper function for assertions
assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [ "$expected" = "$actual" ]; then
        echo "✅ Test Passed: $message"
    else
        echo "❌ Test Failed: $message"
        echo "   Expected: '$expected'"
        echo "   Actual:   '$actual'"
        exit 1
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if echo "$haystack" | grep -qF "$needle"; then
        echo "✅ Test Passed: $message"
    else
        echo "❌ Test Failed: $message"
        echo "   Expected to contain: '$needle'"
        echo "   Actual haystack: '$haystack'"
        exit 1
    fi
}

assert_not_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if ! echo "$haystack" | grep -qF "$needle"; then
        echo "✅ Test Passed: $message"
    else
        echo "❌ Test Failed: $message"
        echo "   Expected NOT to contain: '$needle'"
        echo "   Actual haystack: '$haystack'"
        exit 1
    fi
}

assert_file_exists() {
    local file="$1"
    local message="$2"
    if [ -e "$file" ]; then
        echo "✅ Test Passed: $message"
    else
        echo "❌ Test Failed: $message"
        echo "   File expected to exist: '$file'"
        exit 1
    fi
}

assert_file_not_exists() {
    local file="$1"
    local message="$2"
    if [ ! -e "$file" ]; then
        echo "✅ Test Passed: $message"
    else
        echo "❌ Test Failed: $message"
        echo "   File expected NOT to exist: '$file'"
        exit 1
    fi
}

# Setup test environment
setup_test_env() {
    TEST_DIR=$(mktemp -d -t dust-buster-test-XXXXXX)
    echo "Created test directory: $TEST_DIR"

    # Create files/directories with different ages
    # Mock rationale: The test environment is created with specific files and timestamps
    # to simulate a real filesystem. This allows deterministic testing of `find -mtime` logic.

    # Current date
    touch "$TEST_DIR/current_file.txt"
    mkdir "$TEST_DIR/current_dir"

    # 1 day old (should NOT be deleted with default -a 7)
    touch -d "1 day ago" "$TEST_DIR/recent_file.log"
    mkdir "$TEST_DIR/recent_dir"
    touch -d "1 day ago" "$TEST_DIR/recent_dir/inside.txt"

    # 8 days old (should be deleted with default -a 7)
    touch -d "8 days ago" "$TEST_DIR/old_file.tmp"
    mkdir "$TEST_DIR/old_dir"
    touch -d "8 days ago" "$TEST_DIR/old_dir/nested_old.txt"

    # 10 days old (should be deleted with default -a 7)
    touch -d "10 days ago" "$TEST_DIR/very_old_report.csv"
    mkdir "$TEST_DIR/very_old_empty_dir"

    # File with spaces in name
    touch -d "9 days ago" "$TEST_DIR/old file with spaces.txt"

    # File with special characters
    touch -d "9 days ago" "$TEST_DIR/old_file_!@#$.zip"
}

# Cleanup test environment
cleanup_test_env() {
    if [ -d "$TEST_DIR" ]; then
        rm -rf "$TEST_DIR"
        echo "Cleaned up test directory: $TEST_DIR"
    fi
}

# --- Test Cases ---

# Test 1: Dry run, default age (7 days)
test_dry_run_default_age() {
    echo "--- Running Test 1: Dry run, default age (7 days) ---"
    setup_test_env

    OUTPUT=$("$SCRIPT_TO_TEST" -d "$TEST_DIR" -a 7)
    
    assert_contains "$OUTPUT" "old_file.tmp" "Dry run should list old_file.tmp"
    assert_contains "$OUTPUT" "old_dir" "Dry run should list old_dir"
    assert_contains "$OUTPUT" "very_old_report.csv" "Dry run should list very_old_report.csv"
    assert_contains "$OUTPUT" "very_old_empty_dir" "Dry run should list very_old_empty_dir"
    assert_contains "$OUTPUT" "old file with spaces.txt" "Dry run should list file with spaces"
    assert_contains "$OUTPUT" "old_file_!@#$.zip" "Dry run should list file with special chars"

    assert_not_contains "$OUTPUT" "current_file.txt" "Dry run should not list current_file.txt"
    assert_not_contains "$OUTPUT" "recent_file.log" "Dry run should not list recent_file.log"
    assert_not_contains "$OUTPUT" "recent_dir" "Dry run should not list recent_dir"
    assert_contains "$OUTPUT" "This was a dry run. No files were deleted." "Dry run message should be present"

    assert_file_exists "$TEST_DIR/old_file.tmp" "File should still exist after dry run"
    assert_file_exists "$TEST_DIR/old_dir" "Directory should still exist after dry run"

    cleanup_test_env
    echo ""
}

# Test 2: Purge with confirmation, default age (7 days)
test_purge_with_confirmation_default_age() {
    echo "--- Running Test 2: Purge with confirmation, default age (7 days) ---"
    setup_test_env

    # Simulate 'y' input for confirmation
    OUTPUT=$(echo "y" | "$SCRIPT_TO_TEST" -d "$TEST_DIR" -a 7 -p)

    assert_contains "$OUTPUT" "Initiating Digital Dust Bunny Purge..." "Purge message should be present"
    assert_contains "$OUTPUT" "Digital Dust Bunny Purge complete!" "Completion message should be present"

    assert_file_not_exists "$TEST_DIR/old_file.tmp" "old_file.tmp should be deleted"
    assert_file_not_exists "$TEST_DIR/old_dir" "old_dir should be deleted"
    assert_file_not_exists "$TEST_DIR/very_old_report.csv" "very_old_report.csv should be deleted"
    assert_file_not_exists "$TEST_DIR/very_old_empty_dir" "very_old_empty_dir should be deleted"
    assert_file_not_exists "$TEST_DIR/old file with spaces.txt" "file with spaces should be deleted"
    assert_file_not_exists "$TEST_DIR/old_file_!@#$.zip" "file with special chars should be deleted"

    assert_file_exists "$TEST_DIR/current_file.txt" "current_file.txt should remain"
    assert_file_exists "$TEST_DIR/recent_file.log" "recent_file.log should remain"
    assert_file_exists "$TEST_DIR/recent_dir" "recent_dir should remain"
    assert_file_exists "$TEST_DIR/recent_dir/inside.txt" "file inside recent_dir should remain"

    cleanup_test_env
    echo ""
}

# Test 3: Force purge, default age (7 days)
test_force_purge_default_age() {
    echo "--- Running Test 3: Force purge, default age (7 days) ---"
    setup_test_env

    OUTPUT=$("$SCRIPT_TO_TEST" -d "$TEST_DIR" -a 7 -f)

    assert_contains "$OUTPUT" "Initiating Digital Dust Bunny Purge..." "Purge message should be present"
    assert_contains "$OUTPUT" "Digital Dust Bunny Purge complete!" "Completion message should be present"
    assert_not_contains "$OUTPUT" "Do you wish to purge these digital dust bunnies?" "No confirmation prompt in force mode"

    assert_file_not_exists "$TEST_DIR/old_file.tmp" "old_file.tmp should be deleted"
    assert_file_not_exists "$TEST_DIR/old_dir" "old_dir should be deleted"

    cleanup_test_env
    echo ""
}

# Test 4: Dry run, custom age (e.g., 2 days)
test_dry_run_custom_age() {
    echo "--- Running Test 4: Dry run, custom age (2 days) ---"
    setup_test_env

    OUTPUT=$("$SCRIPT_TO_TEST" -d "$TEST_DIR" -a 2)

    assert_contains "$OUTPUT" "recent_file.log" "Dry run with -a 2 should list recent_file.log"
    assert_contains "$OUTPUT" "recent_dir" "Dry run with -a 2 should list recent_dir"
    assert_contains "$OUTPUT" "old_file.tmp" "Dry run with -a 2 should list old_file.tmp"
    assert_contains "$OUTPUT" "very_old_report.csv" "Dry run with -a 2 should list very_old_report.csv"

    assert_not_contains "$OUTPUT" "current_file.txt" "Dry run with -a 2 should not list current_file.txt"
    assert_contains "$OUTPUT" "This was a dry run. No files were deleted." "Dry run message should be present"

    cleanup_test_env
    echo ""
}

# Test 5: Purge with custom age (e.g., 2 days)
test_purge_custom_age() {
    echo "--- Running Test 5: Purge with custom age (2 days) ---"
    setup_test_env

    OUTPUT=$(echo "y" | "$SCRIPT_TO_TEST" -d "$TEST_DIR" -a 2 -p)

    assert_contains "$OUTPUT" "Digital Dust Bunny Purge complete!" "Completion message should be present"

    assert_file_not_exists "$TEST_DIR/recent_file.log" "recent_file.log should be deleted"
    assert_file_not_exists "$TEST_DIR/recent_dir" "recent_dir should be deleted" # This will delete the dir and its contents
    assert_file_not_exists "$TEST_DIR/old_file.tmp" "old_file.tmp should be deleted"
    assert_file_not_exists "$TEST_DIR/very_old_report.csv" "very_old_report.csv should be deleted"

    assert_file_exists "$TEST_DIR/current_file.txt" "current_file.txt should remain"

    cleanup_test_env
    echo ""
}

# Test 6: Invalid directory
test_invalid_directory() {
    echo "--- Running Test 6: Invalid directory ---"
    setup_test_env

    OUTPUT=$("$SCRIPT_TO_TEST" -d "$TEST_DIR/non_existent_dir" 2>&1)
    
    assert_contains "$OUTPUT" "Error: Target directory '$TEST_DIR/non_existent_dir' does not exist or is not a directory." "Error for invalid directory"
    assert_equals "1" "$?" "Script should exit with error code 1"

    cleanup_test_env
    echo ""
}

# Test 7: Invalid age
test_invalid_age() {
    echo "--- Running Test 7: Invalid age ---"
    setup_test_env

    OUTPUT=$("$SCRIPT_TO_TEST" -d "$TEST_DIR" -a "abc" 2>&1)
    
    assert_contains "$OUTPUT" "Error: Age must be a positive integer." "Error for invalid age"
    assert_equals "1" "$?" "Script should exit with error code 1"

    cleanup_test_env
    echo ""
}

# Test 8: No dust bunnies found
test_no_dust_bunnies() {
    echo "--- Running Test 8: No dust bunnies found ---"
    setup_test_env

    # Set age very high so nothing is found
    OUTPUT=$("$SCRIPT_TO_TEST" -d "$TEST_DIR" -a 999)
    
    assert_contains "$OUTPUT" "No digital dust bunnies found! Your system is sparkling clean." "Message for no dust bunnies"
    assert_equals "0" "$?" "Script should exit with success code 0"

    cleanup_test_env
    echo ""
}

# Run all tests
test_dry_run_default_age
test_purge_with_confirmation_default_age
test_force_purge_default_age
test_dry_run_custom_age
test_purge_custom_age
test_invalid_directory
test_invalid_age
test_no_dust_bunnies

echo "All tests completed successfully!"
