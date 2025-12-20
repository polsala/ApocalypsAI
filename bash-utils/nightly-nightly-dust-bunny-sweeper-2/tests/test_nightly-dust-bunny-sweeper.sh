#!/bin/bash

# Test script for nightly-dust-bunny-sweeper.sh

# --- Test Setup ---
TEST_DIR=$(mktemp -d)
SCRIPT_PATH="./src/nightly-dust-bunny-sweeper.sh"
MOCK_LOG_FILE="$TEST_DIR/mock_commands.log"

# Mock rationale: We need to prevent actual file system modifications during tests
# and instead record what commands would have been executed.
# This ensures tests are deterministic and safe.

# Override find, rm, rmdir for testing
find() {
    echo "# Mock rationale: Overriding 'find' to control test output." >> "$MOCK_LOG_FILE"
    local target_dir="$1" # Capture the target directory passed to find
    shift # Remove target_dir from arguments
    
    # Check for file search pattern
    if [[ "$@" == *"-type f -mtime +"* ]]; then
        echo "$target_dir/old_file.txt"
        echo "$target_dir/subdir/another_old_file.log"
    # Check for empty directory search pattern
    elif [[ "$@" == *"-type d -empty"* ]]; then
        echo "$target_dir/empty_dir"
        echo "$target_dir/subdir/empty_nested_dir"
        # Add the target_dir itself, as the script is supposed to filter it out if it becomes empty
        echo "$target_dir" 
    else
        # Fallback for other find calls if any, though our script only uses specific ones
        command find "$@"
    fi
}

rm() {
    echo "# Mock rationale: Overriding 'rm' to log deletion attempts." >> "$MOCK_LOG_FILE"
    echo "MOCK_RM_CALL: $@" >> "$MOCK_LOG_FILE"
}

rmdir() {
    echo "# Mock rationale: Overriding 'rmdir' to log deletion attempts." >> "$MOCK_LOG_FILE"
    echo "MOCK_RMDIR_CALL: $@" >> "$MOCK_LOG_FILE"
}

# --- Test Functions ---

run_test() {
    local test_name="$1"
    local command="$2"
    local expected_output_regex="$3"
    local expected_mock_log_regex="$4"
    local exit_code_expected="${5:-0}"

    echo "--- Running Test: $test_name ---"
    
    # Clear mock log for each test
    > "$MOCK_LOG_FILE"

    # Execute the script and capture output
    OUTPUT=$($command 2>&1)
    EXIT_CODE=$?

    # Check exit code
    if [ "$EXIT_CODE" -ne "$exit_code_expected" ]; then
        echo "FAIL: $test_name - Expected exit code $exit_code_expected, got $EXIT_CODE"
        echo "Output: $OUTPUT"
        return 1
    fi

    # Check output against regex
    if ! echo "$OUTPUT" | grep -Eq "$expected_output_regex"; then
        echo "FAIL: $test_name - Output mismatch."
        echo "Expected regex: $expected_output_regex"
        echo "Actual output: $OUTPUT"
        return 1
    fi

    # Check mock log against regex if provided
    if [ -n "$expected_mock_log_regex" ]; then
        MOCK_LOG_CONTENT=$(cat "$MOCK_LOG_FILE")
        if ! echo "$MOCK_LOG_CONTENT" | grep -Eq "$expected_mock_log_regex"; then
            echo "FAIL: $test_name - Mock log mismatch."
            echo "Expected regex: $expected_mock_log_regex"
            echo "Actual mock log: $MOCK_LOG_CONTENT"
            return 1
        fi
    fi

    echo "PASS: $test_name"
    return 0
}

# --- Actual Tests ---

# Test 1: No arguments (should show usage and exit with error)
run_test "No arguments" \
    "$SCRIPT_PATH" \
    "Usage: .* -d <directory>" \
    "" \
    1

# Test 2: Missing directory argument (should show usage and exit with error)
run_test "Missing directory argument" \
    "$SCRIPT_PATH --clean" \
    "Error: Target directory must be specified." \
    "" \
    1

# Test 3: Non-existent directory (should exit with error)
run_test "Non-existent directory" \
    "$SCRIPT_PATH -d /nonexistent/path" \
    "Error: Directory '/nonexistent/path' does not exist." \
    "" \
    1

# Test 4: List mode - finds old files and empty dirs
run_test "List mode - finds old files and empty dirs" \
    "$SCRIPT_PATH -d $TEST_DIR" \
    "Searching for ancient scrolls.*- File: $TEST_DIR/old_file.txt.*- File: $TEST_DIR/subdir/another_old_file.log.*Searching for forgotten chambers.*- Directory: $TEST_DIR/empty_dir.*- Directory: $TEST_DIR/subdir/empty_nested_dir" \
    "find" # Just ensure find was called

# Test 5: Clean mode - calls rm and rmdir
run_test "Clean mode - calls rm and rmdir" \
    "$SCRIPT_PATH -d $TEST_DIR --clean" \
    "Sweeping away ancient scrolls.*Sealing forgotten chambers" \
    "MOCK_RM_CALL: -v $TEST_DIR/old_file.txt $TEST_DIR/subdir/another_old_file.log.*MOCK_RMDIR_CALL: -v $TEST_DIR/subdir/empty_nested_dir $TEST_DIR/empty_dir"

# Test 6: Custom age - list mode
run_test "Custom age - list mode" \
    "$SCRIPT_PATH -d $TEST_DIR --age 10" \
    "Sweeping in '$TEST_DIR' \(files older than 10 days\)" \
    "find"

# --- Cleanup ---
rm -rf "$TEST_DIR"
