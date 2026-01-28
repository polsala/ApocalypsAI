#!/bin/bash

# Source the main script to test its functions, or just run it as a separate process.
# For bash scripts, it's often easier to run the script as a separate process and capture its output/side effects.

SCRIPT_PATH="./src/dust_bunny_sweeper.sh"

# Helper function to create a temporary directory and clean it up on exit
setup_test_env() {
    TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXXXXX)
    ARCHIVE_DIR=$(mktemp -d -t dust-bunny-archive-XXXXXXXX)
    export HOME="$TEST_DIR" # Mock rationale: Set HOME to control default archive path
    echo "Test environment created: $TEST_DIR"
    echo "Archive directory: $ARCHIVE_DIR"
}

cleanup_test_env() {
    if [[ -d "$TEST_DIR" ]]; then
        rm -rf "$TEST_DIR"
        echo "Cleaned up test environment: $TEST_DIR"
    fi
    if [[ -d "$ARCHIVE_DIR" ]]; then
        rm -rf "$ARCHIVE_DIR"
        echo "Cleaned up archive directory: $ARCHIVE_DIR"
    fi
}

# Register cleanup function to run on script exit
trap cleanup_test_env EXIT

# Test counter
TEST_COUNT=0
PASS_COUNT=0

assert_equals() {
    TEST_COUNT=$((TEST_COUNT + 1))
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$expected" == "$actual" ]]; then
        PASS_COUNT=$((PASS_COUNT + 1))
        echo "PASS: $message"
    else
        echo "FAIL: $message"
        echo "  Expected: '$expected'"
        echo "  Actual:   '$actual'"
    fi
}

assert_contains() {
    TEST_COUNT=$((TEST_COUNT + 1))
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if [[ "$haystack" == *"$needle"* ]]; then
        PASS_COUNT=$((PASS_COUNT + 1))
        echo "PASS: $message"
    else
        echo "FAIL: $message"
        echo "  Expected to contain: '$needle'"
        echo "  Actual:              '$haystack'"
    fi
}

assert_not_contains() {
    TEST_COUNT=$((TEST_COUNT + 1))
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if [[ "$haystack" != *"$needle"* ]]; then
        PASS_COUNT=$((PASS_COUNT + 1))
        echo "PASS: $message"
    else
        echo "FAIL: $message"
        echo "  Expected NOT to contain: '$needle'"
        echo "  Actual:                  '$haystack'"
    fi
}

assert_file_exists() {
    TEST_COUNT=$((TEST_COUNT + 1))
    local file="$1"
    local message="$2"
    if [[ -f "$file" ]]; then
        PASS_COUNT=$((PASS_COUNT + 1))
        echo "PASS: $message"
    else
        echo "FAIL: $message"
        echo "  File not found: '$file'"
    fi
}

assert_file_not_exists() {
    TEST_COUNT=$((TEST_COUNT + 1))
    local file="$1"
    local message="$2"
    if [[ ! -f "$file" ]]; then
        PASS_COUNT=$((PASS_COUNT + 1))
        echo "PASS: $message"
    else
        echo "FAIL: $message"
        echo "  File unexpectedly found: '$file'"
    fi
}

# --- Test Cases ---

# Test 1: Basic report, no old files
test_no_old_files() {
    setup_test_env
    local current_file="$TEST_DIR/current_file.txt"
    touch "$current_file"
    local output=$("$SCRIPT_PATH" "$TEST_DIR" -a 1 2>&1)
    assert_contains "$output" "No digital dust bunnies found" "Test 1: No old files found"
    cleanup_test_env
}

# Test 2: Basic report, one old file
test_one_old_file_report() {
    setup_test_env
    local old_file="$TEST_DIR/old_document.pdf"
    touch -t $(date --date="2 days ago" +%Y%m%d%H%M.%S) "$old_file" # Mock rationale: Set file modification time
    local output=$("$SCRIPT_PATH" "$TEST_DIR" -a 1 2>&1)
    assert_contains "$output" "Found the following digital dust bunnies:" "Test 2: Report header present"
    assert_contains "$output" "$old_file" "Test 2: Old file listed in report"
    assert_file_exists "$old_file" "Test 2: Old file still exists after report"
    cleanup_test_env
}

# Test 3: Delete action with confirmation (simulated 'N')
test_delete_cancelled() {
    setup_test_env
    local old_file="$TEST_DIR/old_log.log"
    touch -t $(date --date="2 days ago" +%Y%m%d%H%M.%S) "$old_file" # Mock rationale: Set file modification time
    local output=$(echo "N" | "$SCRIPT_PATH" "$TEST_DIR" -a 1 -m delete 2>&1)
    assert_contains "$output" "Action cancelled by user." "Test 3: Delete cancelled message"
    assert_file_exists "$old_file" "Test 3: Old file still exists after cancelled delete"
    cleanup_test_env
}

# Test 4: Delete action with force
test_delete_forced() {
    setup_test_env
    local old_file="$TEST_DIR/old_temp.tmp"
    touch -t $(date --date="2 days ago" +%Y%m%d%H%M.%S) "$old_file" # Mock rationale: Set file modification time
    local output=$("$SCRIPT_PATH" "$TEST_DIR" -a 1 -m delete -f 2>&1)
    assert_contains "$output" "Vaporizing dust bunnies (deleting permanently)..." "Test 4: Delete confirmation message"
    assert_file_not_exists "$old_file" "Test 4: Old file deleted"
    cleanup_test_env
}

# Test 5: Archive action with force
test_archive_forced() {
    setup_test_env
    local old_file="$TEST_DIR/old_backup.zip"
    touch -t $(date --date="2 days ago" +%Y%m%d%H%M.%S) "$old_file" # Mock rationale: Set file modification time
    local output=$("$SCRIPT_PATH" "$TEST_DIR" -a 1 -m archive -f -o "$ARCHIVE_DIR" 2>&1)
    assert_contains "$output" "Sweeping dust bunnies to the Digital Void (archiving)..." "Test 5: Archive confirmation message"
    assert_file_not_exists "$old_file" "Test 5: Original file moved"
    assert_file_exists "$ARCHIVE_DIR/$(basename "$old_file")" "Test 5: File exists in archive"
    cleanup_test_env
}

# Test 6: Exclude extensions
test_exclude_extensions() {
    setup_test_env
    local old_file_to_exclude="$TEST_DIR/important.log"
    local old_file_to_sweep="$TEST_DIR/junk.txt"
    touch -t $(date --date="2 days ago" +%Y%m%d%H%M.%S) "$old_file_to_exclude"
    touch -t $(date --date="2 days ago" +%Y%m%d%H%M.%S) "$old_file_to_sweep"
    local output=$("$SCRIPT_PATH" "$TEST_DIR" -a 1 -x "log" 2>&1)
    assert_not_contains "$output" "$old_file_to_exclude" "Test 6: Excluded file not listed"
    assert_contains "$output" "$old_file_to_sweep" "Test 6: Non-excluded file listed"
    cleanup_test_env
}

# Test 7: Invalid directory
test_invalid_directory() {
    setup_test_env
    local output=$("$SCRIPT_PATH" "$TEST_DIR/non_existent_dir" 2>&1)
    assert_contains "$output" "Error: Directory '$TEST_DIR/non_existent_dir' does not exist or is not a directory." "Test 7: Invalid directory error"
    cleanup_test_env
}

# Test 8: No directory provided
test_no_directory_provided() {
    setup_test_env
    local output=$("$SCRIPT_PATH" 2>&1)
    assert_contains "$output" "Error: Please specify a directory to scan." "Test 8: No directory provided error"
    cleanup_test_env
}

# Test 9: Archive to default directory
test_archive_default_dir() {
    setup_test_env
    local old_file="$TEST_DIR/old_default.dat"
    touch -t $(date --date="2 days ago" +%Y%m%d%H%M.%S) "$old_file"
    local output=$(echo "y" | "$SCRIPT_PATH" "$TEST_DIR" -a 1 -m archive 2>&1) # Mock rationale: Simulate user input 'y'
    assert_contains "$output" "Archive directory: '$TEST_DIR/.digital_void_archive'" "Test 9: Default archive dir path shown"
    assert_file_not_exists "$old_file" "Test 9: Original file moved from source"
    assert_file_exists "$TEST_DIR/.digital_void_archive/$(basename "$old_file")" "Test 9: File exists in default archive"
    cleanup_test_env
}


# Run all tests
echo "--- Running Digital Dust Bunny Sweeper Tests ---"
test_no_old_files
test_one_old_file_report
test_delete_cancelled
test_delete_forced
test_archive_forced
test_exclude_extensions
test_invalid_directory
test_no_directory_provided
test_archive_default_dir
echo "--- Test Summary ---"
echo "Total tests: $TEST_COUNT"
echo "Passed: $PASS_COUNT"
echo "Failed: $((TEST_COUNT - PASS_COUNT))"

if [[ "$PASS_COUNT" -eq "$TEST_COUNT" ]]; then
    exit 0
else
    exit 1
fi
