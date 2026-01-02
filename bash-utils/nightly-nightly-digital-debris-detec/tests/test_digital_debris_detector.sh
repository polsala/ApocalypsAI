#!/bin/bash

# Mock rationale:
# We need to test file system operations (creating, moving, deleting files)
# and the script's output. Instead of mocking 'find', 'mv', 'rm', etc.,
# which would be overly complex for a bash script, we perform these operations
# in a temporary directory. This allows us to test the script's interaction
# with the file system in an isolated and deterministic manner without
# affecting the actual system. The 'find' command's behavior is standard
# and doesn't require mocking; its output is implicitly tested by checking
# the final state of the temporary directory.

SCRIPT_PATH="./src/digital_debris_detector.sh"
DEBRIS_VAULT_NAME=".digital_debris_vault"

# Helper function for assertions
assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$expected" == "$actual" ]]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message"
        echo "  Expected: '$expected'"
        echo "  Actual:   '$actual'"
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
        echo "FAIL: $message"
        echo "  Expected to contain: '$needle'"
        echo "  Actual:              '$haystack'"
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
        echo "FAIL: $message"
        echo "  Expected NOT to contain: '$needle'"
        echo "  Actual:                  '$haystack'"
        exit 1
    fi
}

# Setup: Create a temporary directory for testing
setup() {
    TEST_DIR=$(mktemp -d -t ddd_test_XXXXXX)
    echo "Test directory: $TEST_DIR"
    # Create some files with different modification times
    # Using GNU date syntax for 'touch -t'
    touch -t $(date +%Y%m%d%H%M.%S -d "2 days ago") "$TEST_DIR/recent_file.txt"
    touch -t $(date +%Y%m%d%H%M.%S -d "40 days ago") "$TEST_DIR/old_file_1.log"
    touch -t $(date +%Y%m%d%H%M.%S -d "40 days ago") "$TEST_DIR/old file 2 with spaces.dat"
    touch -t $(date +%Y%m%d%H%M.%S -d "10 days ago") "$TEST_DIR/another_recent.tmp"
    mkdir -p "$TEST_DIR/subdir"
    touch -t $(date +%Y%m%d%H%M.%S -d "50 days ago") "$TEST_DIR/subdir/very_old.conf"
    chmod +x "$SCRIPT_PATH" # Ensure script is executable
}

# Teardown: Remove the temporary directory
teardown() {
    rm -rf "$TEST_DIR"
    echo "Cleaned up $TEST_DIR"
}

# Test Cases

# Test 1: Report action - finds old files
test_report_action() {
    setup
    echo "Running test_report_action..."
    OUTPUT=$("$SCRIPT_PATH" --days 30 --report "$TEST_DIR")
    assert_contains "$OUTPUT" "old_file_1.log" "Report should list old_file_1.log"
    assert_contains "$OUTPUT" "old file 2 with spaces.dat" "Report should list 'old file 2 with spaces.dat'"
    assert_contains "$OUTPUT" "subdir/very_old.conf" "Report should list subdir/very_old.conf"
    assert_not_contains "$OUTPUT" "recent_file.txt" "Report should not list recent_file.txt"
    assert_not_contains "$OUTPUT" "another_recent.tmp" "Report should not list another_recent.tmp"
    assert_contains "$OUTPUT" "Debris reported." "Report action confirmation message"
    teardown
}

# Test 2: Archive action - moves old files to vault
test_archive_action() {
    setup
    echo "Running test_archive_action..."
    "$SCRIPT_PATH" --days 30 --archive "$TEST_DIR" > /dev/null # Suppress output for cleaner test
    
    VAULT_PATH="$TEST_DIR/$DEBRIS_VAULT_NAME"
    assert_equals "1" "$(find "$VAULT_PATH" -type f -name "old_file_1.log" | wc -l)" "old_file_1.log should be in vault"
    assert_equals "1" "$(find "$VAULT_PATH" -type f -name "old file 2 with spaces.dat" | wc -l)" "'old file 2 with spaces.dat' should be in vault"
    assert_equals "1" "$(find "$VAULT_PATH" -type f -name "very_old.conf" | wc -l)" "very_old.conf should be in vault"
    
    assert_equals "0" "$(find "$TEST_DIR" -maxdepth 1 -type f -name "old_file_1.log" | wc -l)" "old_file_1.log should be moved from root"
    assert_equals "0" "$(find "$TEST_DIR/subdir" -type f -name "very_old.conf" | wc -l)" "very_old.conf should be moved from subdir"

    assert_equals "1" "$(find "$TEST_DIR" -maxdepth 1 -type f -name "recent_file.txt" | wc -l)" "recent_file.txt should remain"
    teardown
}

# Test 3: Vaporize action - deletes old files
test_vaporize_action() {
    setup
    echo "Running test_vaporize_action..."
    "$SCRIPT_PATH" --days 30 --vaporize "$TEST_DIR" > /dev/null # Suppress output
    
    assert_equals "0" "$(find "$TEST_DIR" -type f -name "old_file_1.log" | wc -l)" "old_file_1.log should be vaporized"
    assert_equals "0" "$(find "$TEST_DIR" -type f -name "old file 2 with spaces.dat" | wc -l)" "'old file 2 with spaces.dat' should be vaporized"
    assert_equals "0" "$(find "$TEST_DIR/subdir" -type f -name "very_old.conf" | wc -l)" "very_old.conf should be vaporized"

    assert_equals "1" "$(find "$TEST_DIR" -maxdepth 1 -type f -name "recent_file.txt" | wc -l)" "recent_file.txt should remain"
    teardown
}

# Test 4: No debris found
test_no_debris() {
    setup
    echo "Running test_no_debris..."
    OUTPUT=$("$SCRIPT_PATH" --days 100 "$TEST_DIR")
    assert_contains "$OUTPUT" "No digital debris detected. All clear!" "Should report no debris"
    teardown
}

# Test 5: Invalid directory
test_invalid_directory() {
    echo "Running test_invalid_directory..."
    OUTPUT=$("$SCRIPT_PATH" /nonexistent/path 2>&1) # Redirect stderr to stdout
    assert_contains "$OUTPUT" "Error: Target directory '/nonexistent/path' does not exist or is not a directory." "Should error on invalid directory"
    assert_equals "1" "$?" "Should exit with error code 1"
}

# Test 6: Invalid days argument
test_invalid_days() {
    echo "Running test_invalid_days..."
    setup
    OUTPUT=$("$SCRIPT_PATH" --days abc "$TEST_DIR" 2>&1)
    assert_contains "$OUTPUT" "Error: --days requires a numeric argument." "Should error on non-numeric days"
    assert_equals "1" "$?" "Should exit with error code 1"
    teardown

    setup
    OUTPUT=$("$SCRIPT_PATH" --days 0 "$TEST_DIR" 2>&1)
    assert_contains "$OUTPUT" "Error: Days must be a positive integer." "Should error on zero days"
    assert_equals "1" "$?" "Should exit with error code 1"
    teardown
}

# Run all tests
echo "Starting all tests for Digital Debris Detector..."
test_report_action
test_archive_action
test_vaporize_action
test_no_debris
test_invalid_directory
test_invalid_days
echo "All tests passed!"
