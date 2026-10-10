#!/bin/bash

# Test suite for Nightly Resource Scavenger

# --- Test Setup ---
TEST_DIR=$(mktemp -d)
MOCK_RM_LOG="$TEST_DIR/mock_rm.log"
MOCK_FIND_OUTPUT_FILE="$TEST_DIR/mock_find_output.txt"
SCRIPT_TO_TEST="../src/main.sh"

# Mock rationale: We need to control the output of 'find' and prevent actual file deletion by 'rm'
# to ensure deterministic and offline tests. This allows us to verify the script's logic without
# modifying the actual filesystem or relying on system state.

# Mock 'find' to return specific files based on test scenario
mock_find() {
    echo "MOCK FIND CALLED: $@" >> "$MOCK_RM_LOG" # Log find calls for debugging
    # Simulate find output based on a pre-defined file
    if [ -f "$MOCK_FIND_OUTPUT_FILE" ]; then
        cat "$MOCK_FIND_OUTPUT_FILE"
    fi
}

# Mock 'rm' to log deletion attempts instead of actually deleting
mock_rm() {
    echo "MOCK RM CALLED: $@" >> "$MOCK_RM_LOG"
    for arg in "$@"; do
        if [[ "$arg" != "-f" ]]; then # Ignore -f flag
            echo "DELETED: $arg" >> "$MOCK_RM_LOG"
        fi
    done
    return 0 # Always succeed for mock
}

# Override system commands for testing
export -f find
export -f rm

# Function to run a test case
run_test() {
    local test_name="$1"
    local expected_output_regex="$2"
    local expected_rm_log_regex="$3"
    local command_args="${@:4}"

    echo "--- Running Test: $test_name ---"
    
    # Clear mock logs and find output for each test
    > "$MOCK_RM_LOG"
    > "$MOCK_FIND_OUTPUT_FILE"

    # Set up specific find output if provided
    if [ -n "$MOCK_FIND_FILES" ]; then
        echo -e "$MOCK_FIND_FILES" > "$MOCK_FIND_OUTPUT_FILE"
    fi

    # Run the script
    OUTPUT=$($SCRIPT_TO_TEST $command_args 2>&1)
    EXIT_CODE=$?

    # Check output
    if echo "$OUTPUT" | grep -Eq "$expected_output_regex"; then
        echo "  [PASS] Output matches expected regex."
    else
        echo "  [FAIL] Output does NOT match expected regex."
        echo "    Expected regex: $expected_output_regex"
        echo "    Actual output:"
        echo "$OUTPUT"
        TEST_FAILED=true
    fi

    # Check rm log
    if [ -n "$expected_rm_log_regex" ]; then
        if cat "$MOCK_RM_LOG" | grep -Eq "$expected_rm_log_regex"; then
            echo "  [PASS] Mock RM log matches expected regex."
        else
            echo "  [FAIL] Mock RM log does NOT match expected regex."
            echo "    Expected regex: $expected_rm_log_regex"
            echo "    Actual RM log:"
            cat "$MOCK_RM_LOG"
            TEST_FAILED=true
        fi
    else
        echo "  [INFO] No specific RM log regex provided for this test."
    fi

    echo "  Exit Code: $EXIT_CODE"
    echo "------------------------------------"
    echo ""
}

TEST_FAILED=false

# --- Test Cases ---

# Test 1: Dry run, no files found
MOCK_FIND_FILES=""
run_test "Dry Run - No Files" \
         "Mode: Dry Run.*No ancient relics found in '$TEST_DIR'.*Total ancient relics identified: 0.*Total relics actually reclaimed: 0" \
         "" \
         "$TEST_DIR"

# Test 2: Dry run, files found
MOCK_FIND_FILES="$TEST_DIR/old_file1.log\n$TEST_DIR/old_file2.tmp"
run_test "Dry Run - Files Found" \
         "Mode: Dry Run.*Found these potential treasures:.*- $TEST_DIR/old_file1.log.*- $TEST_DIR/old_file2.tmp.*Total ancient relics identified: 2.*Total relics actually reclaimed: 0" \
         "" \
         "$TEST_DIR"

# Test 3: Actual run, files found and "deleted"
MOCK_FIND_FILES="$TEST_DIR/old_file3.log\n$TEST_DIR/old_file4.tmp"
run_test "Actual Run - Files Scavenged" \
         "Mode: Actual Scavenge.*Found these potential treasures:.*- $TEST_DIR/old_file3.log.*- $TEST_DIR/old_file4.tmp.*Reclaimed: $TEST_DIR/old_file3.log.*Reclaimed: $TEST_DIR/old_file4.tmp.*Total ancient relics identified: 2.*Total relics actually reclaimed: 2" \
         "DELETED: $TEST_DIR/old_file3.log.*DELETED: $TEST_DIR/old_file4.tmp" \
         "-r $TEST_DIR"

# Test 4: Invalid directory
MOCK_FIND_FILES="" # Ensure find doesn't return anything for non-existent dir
run_test "Invalid Directory" \
         "Warning: Directory '/nonexistent_dir' does not exist or is not a directory. Skipping.*Total ancient relics identified: 0.*Total relics actually reclaimed: 0" \
         "" \
         "/nonexistent_dir"

# Test 5: Custom age threshold (dry run)
MOCK_FIND_FILES="$TEST_DIR/old_file5.log"
run_test "Dry Run - Custom Age" \
         "Scavenging for files older than 10 days.*Mode: Dry Run.*Found these potential treasures:.*- $TEST_DIR/old_file5.log" \
         "" \
         "-d 10 $TEST_DIR"

# Test 6: No directories provided (should show usage and exit with error)
MOCK_FIND_FILES=""
run_test "No Directories Provided" \
         "Error: No target directories specified.*Usage: $SCRIPT_TO_TEST" \
         "" \
         "" # No directories, expect usage message and error exit.
if [ $EXIT_CODE -eq 0 ]; then
    echo "  [FAIL] Expected non-zero exit code for no directories."
    TEST_FAILED=true
else
    echo "  [PASS] Received non-zero exit code for no directories."
fi


# --- Cleanup ---
rm -rf "$TEST_DIR"

if [ "$TEST_FAILED" = true ]; then
    echo "--- One or more tests FAILED! ---"
    exit 1
else
    echo "--- All tests PASSED! ---"
    exit 0
fi
