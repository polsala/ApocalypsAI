#!/bin/bash

# Test script for nightly-digital-garden-weeder

# --- Configuration ---
SCRIPT_PATH="$(dirname "$0")"/../src/weeder.sh
TEST_DIR="/tmp/weeder_test_$(date +%s%N)" # Unique test directory
MOCK_DATE_CMD="date" # Use real date for mtime calculations, but control file creation

# --- Helper Functions ---

# Function to create a dummy file with a specific modification time
create_dummy_file() {
    local path="$1"
    local mtime_offset_days="$2" # e.g., 0 for today, 1 for yesterday, -1 for future
    local content="${3:-test_content}"

    mkdir -p "$(dirname "$path")"
    echo "$content" > "$path"

    # Calculate target date for touch
    # Mock rationale: Using `date` command for `touch -d` is standard.
    # We control the offset to ensure deterministic file ages relative to "now".
    # This avoids mocking `touch` itself, which is a core utility.
    local target_date
    if [[ "$mtime_offset_days" -lt 0 ]]; then
        # Future date (e.g., -1 day means tomorrow)
        target_date=$("$MOCK_DATE_CMD" -d "$mtime_offset_days days" "+%Y%m%d%H%M.%S")
    else
        # Past date (e.g., 1 day means yesterday)
        target_date=$("$MOCK_DATE_CMD" -d "-$mtime_offset_days days" "+%Y%m%d%H%M.%S")
    fi
    touch -t "$target_date" "$path"
}

# Function to clean up test environment
cleanup() {
    echo "Cleaning up test directory: $TEST_DIR"
    rm -rf "$TEST_DIR"
}

# Register cleanup function to run on exit
trap cleanup EXIT

# --- Test Cases ---

run_test() {
    local test_name="$1"
    local command="$2"
    local expected_output_regex="$3"
    local expected_exit_code="${4:-0}"
    local description="$5"

    echo "--- Running Test: $test_name ---"
    echo "Description: $description"
    echo "Command: $command"

    # Run the command and capture output
    OUTPUT=$(eval "$command" 2>&1)
    EXIT_CODE=$?

    echo "Output:"
    echo "$OUTPUT"
    echo "Exit Code: $EXIT_CODE"

    # Check exit code
    if [[ "$EXIT_CODE" -ne "$expected_exit_code" ]]; then
        echo "FAIL: $test_name - Expected exit code $expected_exit_code, got $EXIT_CODE."
        return 1
    fi

    # Check output using regex
    if [[ "$OUTPUT" =~ $expected_output_regex ]]; then
        echo "PASS: $test_name"
        return 0
    else
        echo "FAIL: $test_name - Output did not match expected regex."
        echo "Expected regex: $expected_output_regex"
        return 1
    fi
}

# Initialize test results
TOTAL_TESTS=0
PASSED_TESTS=0

assert_pass() {
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if run_test "$@"; then
        PASSED_TESTS=$((PASSED_TESTS + 1))
    fi
}

assert_fail() {
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if run_test "$1" "$2" "$3" 1 "$4"; then # Expect exit code 1 for failure
        PASSED_TESTS=$((PASSED_TESTS + 1))
    fi
}

# --- Actual Tests ---

echo "Setting up test environment in $TEST_DIR"
mkdir -p "$TEST_DIR"

# Test 1: Dry run, default retention (7 days), no old files
create_dummy_file "$TEST_DIR/recent_file.txt" 0 "recent"
create_dummy_file "$TEST_DIR/medium_old_file.txt" 5 "medium_old"
create_dummy_file "$TEST_DIR/old_file.txt" 8 "old" # This should be found

assert_pass "Dry Run - Default Retention" \
    "$SCRIPT_PATH --dry-run --dirs $TEST_DIR" \
    "Mode: DRY RUN \(no files will be deleted\).*Would delete: $TEST_DIR/old_file.txt.*Dry Run: 1 files would have been deleted" \
    0 \
    "Should identify one old file in dry run with default 7-day retention."

# Test 2: Live run, default retention, delete old files
# Clean up from previous test to ensure fresh state for live run
rm "$TEST_DIR/old_file.txt" # Manually remove the old file identified in dry run
create_dummy_file "$TEST_DIR/old_file_for_live.txt" 8 "old_live"

assert_pass "Live Run - Default Retention" \
    "$SCRIPT_PATH --dirs $TEST_DIR" \
    "Mode: LIVE RUN \(files WILL be deleted\).*Deleted: $TEST_DIR/old_file_for_live.txt.*Live Run: 1 files deleted" \
    0 \
    "Should delete one old file in live run with default 7-day retention."

# Verify file is actually deleted
if [[ -f "$TEST_DIR/old_file_for_live.txt" ]]; then
    echo "FAIL: Live Run - File was not actually deleted."
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
else
    echo "PASS: Live Run - File confirmed deleted."
    PASSED_TESTS=$((PASSED_TESTS + 1))
fi

# Test 3: Dry run, custom retention (3 days), multiple old files
create_dummy_file "$TEST_DIR/recent_file_2.txt" 0 "recent2"
create_dummy_file "$TEST_DIR/old_file_3days_1.txt" 4 "old3_1"
create_dummy_file "$TEST_DIR/old_file_3days_2.txt" 5 "old3_2"

assert_pass "Dry Run - Custom Retention (3 days)" \
    "$SCRIPT_PATH --dry-run --days 3 --dirs $TEST_DIR" \
    "Mode: DRY RUN \(no files will be deleted\).*Would delete: $TEST_DIR/old_file_3days_1.txt.*Would delete: $TEST_DIR/old_file_3days_2.txt.*Dry Run: 2 files would have been deleted" \
    0 \
    "Should identify two old files with 3-day retention."

# Test 4: Live run, custom retention (3 days), delete multiple old files
rm "$TEST_DIR/old_file_3days_1.txt" "$TEST_DIR/old_file_3days_2.txt" # Clean up
create_dummy_file "$TEST_DIR/old_file_3days_1_live.txt" 4 "old3_1_live"
create_dummy_file "$TEST_DIR/old_file_3days_2_live.txt" 5 "old3_2_live"

assert_pass "Live Run - Custom Retention (3 days)" \
    "$SCRIPT_PATH --days 3 --dirs $TEST_DIR" \
    "Mode: LIVE RUN \(files WILL be deleted\).*Deleted: $TEST_DIR/old_file_3days_1_live.txt.*Deleted: $TEST_DIR/old_file_3days_2_live.txt.*Live Run: 2 files deleted" \
    0 \
    "Should delete two old files with 3-day retention."

# Verify files are actually deleted
if [[ -f "$TEST_DIR/old_file_3days_1_live.txt" || -f "$TEST_DIR/old_file_3days_2_live.txt" ]]; then
    echo "FAIL: Live Run - Custom Retention - Files were not actually deleted."
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
else
    echo "PASS: Live Run - Custom Retention - Files confirmed deleted."
    PASSED_TESTS=$((PASSED_TESTS + 1))
fi

# Test 5: Invalid --days argument
assert_fail "Invalid Days Argument" \
    "$SCRIPT_PATH --days abc --dirs $TEST_DIR" \
    "Error: --days argument must be a positive integer." \
    1 \
    "Should fail with invalid --days argument."

# Test 6: --dirs with non-existent directory (should warn and skip)
assert_pass "Non-Existent Directory" \
    "$SCRIPT_PATH --dry-run --dirs $TEST_DIR/non_existent_dir" \
    "Warning: Directory '$TEST_DIR/non_existent_dir' does not exist or is not a directory. Skipping." \
    0 \
    "Should warn and skip non-existent directory."

# Test 7: No files to delete
rm -rf "$TEST_DIR" # Clean up everything
mkdir -p "$TEST_DIR"
create_dummy_file "$TEST_DIR/only_recent.txt" 0 "recent"

assert_pass "No Files to Delete" \
    "$SCRIPT_PATH --dry-run --days 1 --dirs $TEST_DIR" \
    "Processing directory: $TEST_DIR\n\n--- Summary ---\nDry Run: 0 files would have been deleted" \
    0 \
    "Should report 0 files deleted when none match criteria."

# --- Final Summary ---
echo ""
echo "--- Test Summary ---"
echo "Total Tests: $TOTAL_TESTS"
echo "Passed: $PASSED_TESTS"
echo "Failed: $((TOTAL_TESTS - PASSED_TESTS))"
echo "--------------------"

if [[ "$PASSED_TESTS" -eq "$TOTAL_TESTS" ]]; then
    exit 0
else
    exit 1
fi
