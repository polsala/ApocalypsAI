#!/bin/bash

# Test script for nightly-digital-dust-bunny-sweeper

# Setup a temporary test environment
TEST_DIR=$(mktemp -d)
MOCK_BIN_DIR=$(mktemp -d)
export PATH="$MOCK_BIN_DIR:$PATH" # Prepend mock bin to PATH

# Mock rationale: We need to control the output of 'find' and 'rm'/'rmdir'
# to ensure deterministic tests without modifying the actual filesystem.

# -- MOCK find --
# Mock find will output predefined lists of files/directories.
# It will read from a temporary file to simulate different scenarios.
cat << 'EOF' > "$MOCK_BIN_DIR/find"
#!/bin/bash
# Mock rationale: Simulates 'find' command for deterministic testing.
# Reads from a predefined mock output file.
if [[ "$*" == *"-type f -mtime +"* ]]; then
    cat "$TEST_DIR/mock_find_files.txt"
elif [[ "$*" == *"-type d -empty"* ]]; then
    cat "$TEST_DIR/mock_find_dirs.txt"
else
    # Fallback for unexpected find calls
    echo "MOCK_FIND_ERROR: Unexpected find call: $*" >&2
    exit 1
fi
EOF
chmod +x "$MOCK_BIN_DIR/find"

# -- MOCK rm --
# Mock rm will log its arguments to a file instead of actually deleting.
cat << 'EOF' > "$MOCK_BIN_DIR/rm"
#!/bin/bash
# Mock rationale: Simulates 'rm' command for deterministic testing.
# Logs arguments to a file instead of actual deletion.
echo "MOCK_RM: $*" >> "$TEST_DIR/mock_rm_log.txt"
exit 0
EOF
chmod +x "$MOCK_BIN_DIR/rm"

# -- MOCK rmdir --
# Mock rmdir will log its arguments to a file instead of actually deleting.
cat << 'EOF' > "$MOCK_BIN_DIR/rmdir"
#!/bin/bash
# Mock rationale: Simulates 'rmdir' command for deterministic testing.
# Logs arguments to a file instead of actual deletion.
echo "MOCK_RMDIR: $*" >> "$TEST_DIR/mock_rm_log.txt"
exit 0
EOF
chmod +x "$MOCK_BIN_DIR/rmdir"

# Path to the script under test
SCRIPT_PATH="$(dirname "$0")"/../src/dust_bunny_sweeper.sh

# Test counter
TEST_COUNT=0
PASSED_COUNT=0

run_test() {
    TEST_COUNT=$((TEST_COUNT + 1))
    local test_name="$1"
    local expected_output_regex="$2"
    local expected_rm_log_regex="$3"
    local script_args="$4"
    local expected_exit_code="$5"

    echo "--- Running Test: $test_name ---"

    # Clear mock logs and setup mock find outputs for this test
    > "$TEST_DIR/mock_rm_log.txt"
    > "$TEST_DIR/mock_find_files.txt"
    > "$TEST_DIR/mock_find_dirs.txt"

    # Execute the script
    OUTPUT=$(bash "$SCRIPT_PATH" $script_args 2>&1)
    EXIT_CODE=$?
    RM_LOG=$(cat "$TEST_DIR/mock_rm_log.txt")

    # Check exit code
    if [[ "$EXIT_CODE" -ne "$expected_exit_code" ]]; then
        echo "FAIL: $test_name - Expected exit code $expected_exit_code, got $EXIT_CODE"
        echo "Output: $OUTPUT"
        echo "RM Log: $RM_LOG"
        return 1
    fi

    # Check output
    if [[ ! "$OUTPUT" =~ $expected_output_regex ]]; then
        echo "FAIL: $test_name - Output mismatch."
        echo "Expected regex: $expected_output_regex"
        echo "Actual output:"
        echo "$OUTPUT"
        return 1
    fi

    # Check rm log
    if [[ ! "$RM_LOG" =~ $expected_rm_log_regex ]]; then
        echo "FAIL: $test_name - RM log mismatch."
        echo "Expected regex: $expected_rm_log_regex"
        echo "Actual RM log:"
        echo "$RM_LOG"
        return 1
    fi

    echo "PASS: $test_name"
    PASSED_COUNT=$((PASSED_COUNT + 1))
    return 0
}

# --- Test Cases ---

# Test 1: List mode, no files/dirs
echo "" > "$TEST_DIR/mock_find_files.txt" # Empty file
echo "" > "$TEST_DIR/mock_find_dirs.txt" # Empty file
run_test "List mode - No findings" \
    "No ancient digital lint found.*No vacant digital spaces detected." \
    "^$" \
    "-d $TEST_DIR -a 30 -c list" \
    0

# Test 2: List mode, with old files and empty dirs
echo "$TEST_DIR/old_file_1.txt\n$TEST_DIR/subdir/old_file_2.log" > "$TEST_DIR/mock_find_files.txt"
echo "$TEST_DIR/empty_dir_1\n$TEST_DIR/subdir/empty_dir_2" > "$TEST_DIR/mock_find_dirs.txt"
run_test "List mode - With findings" \
    "File: $TEST_DIR/old_file_1.txt.*File: $TEST_DIR/subdir/old_file_2.log.*Directory: $TEST_DIR/empty_dir_1.*Directory: $TEST_DIR/subdir/empty_dir_2" \
    "^$" \
    "-d $TEST_DIR -a 30 -c list" \
    0

# Test 3: Delete mode, with old files and empty dirs
echo "$TEST_DIR/old_file_1.txt\n$TEST_DIR/subdir/old_file_2.log" > "$TEST_DIR/mock_find_files.txt"
echo "$TEST_DIR/empty_dir_1\n$TEST_DIR/subdir/empty_dir_2" > "$TEST_DIR/mock_find_dirs.txt"
run_test "Delete mode - With findings" \
    "\[SWEEPED\] $TEST_DIR/old_file_1.txt.* \[SWEEPED\] $TEST_DIR/subdir/old_file_2.log.* \[SWEEPED\] $TEST_DIR/empty_dir_1.* \[SWEEPED\] $TEST_DIR/subdir/empty_dir_2" \
    "MOCK_RM: -f $TEST_DIR/old_file_1.txt\nMOCK_RM: -f $TEST_DIR/subdir/old_file_2.log\nMOCK_RMDIR: $TEST_DIR/empty_dir_1\nMOCK_RMDIR: $TEST_DIR/subdir/empty_dir_2" \
    "-d $TEST_DIR -a 30 -c delete" \
    0

# Test 4: Invalid directory
run_test "Invalid directory" \
    "Error: Target directory '/nonexistent' does not exist." \
    "^$" \
    "-d /nonexistent -a 30 -c list" \
    1

# Test 5: Default arguments (current directory, 30 days, list)
# Mock find needs to output relative paths if target_dir is "."
echo "./old_file.txt" > "$TEST_DIR/mock_find_files.txt"
echo "./empty_dir" > "$TEST_DIR/mock_find_dirs.txt"
(cd "$TEST_DIR" && run_test "Default arguments" \
    "Scanning '\.' for temporal detritus older than 30 days.*File: \./old_file.txt.*Directory: \./empty_dir" \
    "^$" \
    "" \
    0)

# Test 6: Empty directory passed as target_dir in delete mode
# Ensure the target directory itself is not removed if it becomes empty
echo "" > "$TEST_DIR/mock_find_files.txt"
echo "$TEST_DIR" > "$TEST_DIR/mock_find_dirs.txt" # Mock find returns the target dir itself as empty
run_test "Delete mode - Target dir itself is empty" \
    "No ancient digital lint found.*No vacant digital spaces detected." \
    "^$" \
    "-d $TEST_DIR -a 30 -c delete" \
    0

# Cleanup
rm -rf "$TEST_DIR" "$MOCK_BIN_DIR"

echo "--- Test Summary ---"
echo "Total Tests: $TEST_COUNT"
echo "Passed: $PASSED_COUNT"
echo "Failed: $((TEST_COUNT - PASSED_COUNT))"

if [[ "$PASSED_COUNT" -eq "$TEST_COUNT" ]]; then
    echo "All tests passed!"
    exit 0
else
    echo "Some tests failed."
    exit 1
fi
