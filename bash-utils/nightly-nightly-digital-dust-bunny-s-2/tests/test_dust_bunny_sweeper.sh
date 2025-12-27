#!/bin/bash

# Test suite for Nightly Digital Dust Bunny Sweeper

SCRIPT_PATH="./src/dust_bunny_sweeper.sh"

# Mock rationale: We create temporary directories and files to simulate a filesystem
# without touching the actual system. This ensures tests are deterministic and isolated.
# We use standard `touch`, `dd`, `mkdir`, `rm -rf` for file system manipulation.

# Helper function to assert conditions
assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$expected" == "$actual" ]]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message (Expected: '$expected', Actual: '$actual')"
        exit 1
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if [[ "$haystack" == *"$needle"* ]]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message (Expected to contain: '$needle', Actual: '$haystack')"
        exit 1
    fi
}

assert_not_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if [[ "$haystack" != *"$needle"* ]]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message (Expected NOT to contain: '$needle', Actual: '$haystack')"
        exit 1
    fi
}

assert_file_exists() {
    local file="$1"
    local message="$2"
    if [[ -f "$file" ]]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message (File '$file' does not exist)"
        exit 1
    fi
}

assert_file_not_exists() {
    local file="$1"
    local message="$2"
    if [[ ! -f "$file" ]]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message (File '$file' unexpectedly exists)"
        exit 1
    fi
}

# Setup for tests
setup() {
    TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXXX)
    TARGET_DIR="$TEST_DIR/target"
    ARCHIVE_DIR="$TEST_DIR/archive"
    mkdir -p "$TARGET_DIR"
    mkdir -p "$ARCHIVE_DIR"
    echo "Setup: Created test directories $TARGET_DIR and $ARCHIVE_DIR"
}

# Teardown after tests
teardown() {
    rm -rf "$TEST_DIR"
    echo "Teardown: Removed test directory $TEST_DIR"
}

# --- Test Cases ---

# Test 1: No arguments - should display help and error
test_no_args() {
    setup
    echo "Running Test 1: No arguments"
    local output=$("$SCRIPT_PATH" 2>&1)
    assert_contains "$output" "Error: Target directory (-d) is required." "No args should show error and help"
    teardown
}

# Test 2: Invalid target directory
test_invalid_target_dir() {
    setup
    echo "Running Test 2: Invalid target directory"
    local output=$("$SCRIPT_PATH" -d "$TEST_DIR/non_existent" -a 1 2>&1)
    assert_contains "$output" "Error: Target directory '$TEST_DIR/non_existent' does not exist or is not a directory." "Invalid target dir should error"
    teardown
}

# Test 3: No criteria (age or size)
test_no_criteria() {
    setup
    echo "Running Test 3: No criteria"
    local output=$("$SCRIPT_PATH" -d "$TARGET_DIR" 2>&1)
    assert_contains "$output" "Error: Either age (-a) or size (-s) criteria must be specified." "No criteria should error"
    teardown
}

# Test 4: Find files older than N days (listing only)
test_find_by_age_list() {
    setup
    echo "Running Test 4: Find files older than N days (listing only)"
    touch "$TARGET_DIR/old_file.txt"
    sleep 1 # Ensure a slight time difference for -a 0 to work reliably

    local output=$("$SCRIPT_PATH" -d "$TARGET_DIR" -a 0 2>&1)
    assert_contains "$output" "Found 1 digital dust bunnies:" "Should find one old file"
    assert_contains "$output" "$TARGET_DIR/old_file.txt" "Output should list old_file.txt"
    assert_file_exists "$TARGET_DIR/old_file.txt" "Old file should still exist in target dir"
    teardown
}

# Test 5: Find files larger than N MB (listing only)
test_find_by_size_list() {
    setup
    echo "Running Test 5: Find files larger than N MB (listing only)"
    # Create a large file (2MB)
    dd if=/dev/zero of="$TARGET_DIR/large_file.bin" bs=1M count=2 2>/dev/null

    local output=$("$SCRIPT_PATH" -d "$TARGET_DIR" -s 1 2>&1) # Find files > 1MB
    assert_contains "$output" "Found 1 digital dust bunnies:" "Should find one large file"
    assert_contains "$output" "$TARGET_DIR/large_file.bin" "Output should list large_file.bin"
    assert_file_exists "$TARGET_DIR/large_file.bin" "Large file should still exist in target dir"
    teardown
}

# Test 6: Archive files older than N days
test_archive_by_age() {
    setup
    echo "Running Test 6: Archive files older than N days"
    touch "$TARGET_DIR/old_file.txt"
    sleep 1 # Ensure a slight time difference for -a 0 to work reliably

    # Mock rationale: We pipe 'y' to stdin to simulate user confirmation.
    # This makes the test deterministic and non-interactive.
    local output=$(echo "y" | "$SCRIPT_PATH" -d "$TARGET_DIR" -a 0 -o "$ARCHIVE_DIR" 2>&1)
    assert_contains "$output" "Sweeping dust bunnies into '$ARCHIVE_DIR'..." "Should indicate sweeping"
    assert_file_not_exists "$TARGET_DIR/old_file.txt" "Old file should be moved from target dir"
    assert_file_exists "$ARCHIVE_DIR/old_file.txt" "Old file should exist in archive dir"
    teardown
}

# Test 7: Archive files larger than N MB (force sweep)
test_archive_by_size_force() {
    setup
    echo "Running Test 7: Archive files larger than N MB (force sweep)"
    dd if=/dev/zero of="$TARGET_DIR/large_file.bin" bs=1M count=2 2>/dev/null

    local output=$("$SCRIPT_PATH" -d "$TARGET_DIR" -s 1 -o "$ARCHIVE_DIR" -f 2>&1)
    assert_contains "$output" "Sweeping dust bunnies into '$ARCHIVE_DIR'..." "Should indicate sweeping (force)"
    assert_file_not_exists "$TARGET_DIR/large_file.bin" "Large file should be moved from target dir"
    assert_file_exists "$ARCHIVE_DIR/large_file.bin" "Large file should exist in archive dir"
    teardown
}

# Test 8: No dust bunnies found
test_no_dust_bunnies() {
    setup
    echo "Running Test 8: No dust bunnies found"
    touch "$TARGET_DIR/recent_small_file.txt" # A file that won't match criteria
    dd if=/dev/zero of="$TARGET_DIR/small_file.bin" bs=1K count=100 2>/dev/null # 100KB file

    local output=$("$SCRIPT_PATH" -d "$TARGET_DIR" -a 1 -s 10 2>&1) # Older than 1 day, larger than 10MB
    assert_contains "$output" "No digital dust bunnies found. Your system is sparkling clean!" "Should report no dust bunnies"
    assert_file_exists "$TARGET_DIR/recent_small_file.txt" "File should remain"
    assert_file_exists "$TARGET_DIR/small_file.bin" "File should remain"
    teardown
}

# Test 9: Archive directory creation
test_archive_dir_creation() {
    setup
    echo "Running Test 9: Archive directory creation"
    rmdir "$ARCHIVE_DIR" # Remove the pre-created archive dir
    touch "$TARGET_DIR/file_to_archive.txt"
    sleep 1

    local output=$(echo "y" | "$SCRIPT_PATH" -d "$TARGET_DIR" -a 0 -o "$ARCHIVE_DIR" 2>&1)
    assert_contains "$output" "Void Archive '$ARCHIVE_DIR' does not exist. Creating it..." "Should report archive dir creation"
    assert_file_exists "$ARCHIVE_DIR/file_to_archive.txt" "File should be moved to newly created archive dir"
    teardown
}

# Test 10: User declines sweep
test_user_declines_sweep() {
    setup
    echo "Running Test 10: User declines sweep"
    touch "$TARGET_DIR/file_to_decline.txt"
    sleep 1

    # Mock rationale: We pipe 'n' to stdin to simulate user declining confirmation.
    local output=$(echo "n" | "$SCRIPT_PATH" -d "$TARGET_DIR" -a 0 -o "$ARCHIVE_DIR" 2>&1)
    assert_contains "$output" "Sweep aborted. Dust bunnies remain." "Should report sweep aborted"
    assert_file_exists "$TARGET_DIR/file_to_decline.txt" "File should remain in target dir"
    assert_file_not_exists "$ARCHIVE_DIR/file_to_decline.txt" "File should not be in archive dir"
    teardown
}

# Test 11: Both age and size criteria
test_both_criteria() {
    setup
    echo "Running Test 11: Both age and size criteria"
    # File 1: Old but small
    touch "$TARGET_DIR/old_small.txt"
    sleep 1 # Make it old enough for -a 0
    # File 2: Recent but large
    dd if=/dev/zero of="$TARGET_DIR/recent_large.bin" bs=1M count=2 2>/dev/null
    # File 3: Old and large
    touch "$TARGET_DIR/old_large.txt"
    sleep 1
    dd if=/dev/zero of="$TARGET_DIR/old_large.txt" bs=1M count=3 conv=notrunc oflag=append 2>/dev/null # Make it large after touch

    # Find files older than 0 days OR larger than 1MB
    local output=$("$SCRIPT_PATH" -d "$TARGET_DIR" -a 0 -s 1 2>&1)
    assert_contains "$output" "Warning: Both age and size criteria specified." "Should show warning for both criteria"
    assert_contains "$output" "Found 3 digital dust bunnies:" "Should find all three files"
    assert_contains "$output" "$TARGET_DIR/old_small.txt" "Should list old_small.txt"
    assert_contains "$output" "$TARGET_DIR/recent_large.bin" "Should list recent_large.bin"
    assert_contains "$output" "$TARGET_DIR/old_large.txt" "Should list old_large.txt"
    teardown
}

# Run all tests
echo "--- Running Nightly Digital Dust Bunny Sweeper Tests ---"
test_no_args
test_invalid_target_dir
test_no_criteria
test_find_by_age_list
test_find_by_size_list
test_archive_by_age
test_archive_by_size_force
test_no_dust_bunnies
test_archive_dir_creation
test_user_declines_sweep
test_both_criteria
echo "--- All Tests Completed ---"
