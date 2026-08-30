#!/bin/bash

# Source the script to be tested
SCRIPT_TO_TEST="src/dust_bunny_sweeper.sh"

# --- Test Utilities ---
# Simple assertion function
assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$expected" == "$actual" ]]; then
        echo "✅ Test Passed: $message"
    else
        echo "❌ Test Failed: $message"
        echo "   Expected: '$expected'"
        echo "   Actual:   '$actual'"
        exit 1
    fi
}

# Function to run the script with mocked commands
run_test_script() {
    local args="$@"
    # Clear logs before each run
    > "$MOCKED_COMMAND_LOG"
    # Run the script in a subshell to isolate mocks
    (
        # Mock rationale: Prevent actual file system changes and capture command calls.
        # Mock 'find' to return predefined files
        find() {
            echo "$MOCK_FIND_OUTPUT"
        }
        # Mock 'mkdir' to prevent actual directory creation
        mkdir() {
            echo "MOCKED_MKDIR $@" >> "$MOCKED_COMMAND_LOG"
            return 0 # Always succeed
        }
        # Mock 'rmdir' to prevent actual directory removal
        rmdir() {
            echo "MOCKED_RMDIR $@" >> "$MOCKED_COMMAND_LOG"
            return 0 # Always succeed
        }
        # Mock 'mv' to log its arguments
        mv() {
            echo "MOCKED_MV $@" >> "$MOCKED_COMMAND_LOG"
            return 0 # Always succeed
        }
        # Mock 'read' for interactive input
        read() {
            # Simulate 'y' or 'n' for interactive prompts
            if [[ "$1" == "-p" ]]; then
                echo "$MOCK_READ_INPUT"
            fi
        }
        # Mock 'date' to return a fixed value for deterministic dustbin naming
        date() {
            echo "20230101000000" # Mock rationale: Ensure deterministic dustbin name for testing
        }
        # Execute the script
        bash "$SCRIPT_TO_TEST" "$args"
    )
    return $?
}

# --- Test Setup ---
TEST_DIR=$(mktemp -d)
MOCKED_COMMAND_LOG="$TEST_DIR/mocked_commands.log"
MOCK_FIND_OUTPUT=""
MOCK_READ_INPUT="y" # Default to 'y' for interactive prompts

# Cleanup function
cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

echo "--- Running Tests for nightly-digital-dust-bunny-sweeper ---"

# Test 1: No old files found (dry run)
echo "Test 1: No old files found (dry run)"
MOCK_FIND_OUTPUT=""
OUTPUT=$(run_test_script "$TEST_DIR" 2>&1)
assert_equals 0 $? "Script should exit with 0 when no files found"
echo "$OUTPUT" | grep -q "No digital dust bunnies found!"
assert_equals 0 $? "Output should indicate no files found"
assert_equals "" "$(cat "$MOCKED_COMMAND_LOG")" "No commands should be mocked"

# Test 2: Old files found, dry run
echo "Test 2: Old files found, dry run"
MOCK_FIND_OUTPUT="$TEST_DIR/old_file1.txt\n$TEST_DIR/old_file2.log"
OUTPUT=$(run_test_script "$TEST_DIR" 2>&1)
assert_equals 0 $? "Script should exit with 0 after dry run"
echo "$OUTPUT" | grep -q "Found these dusty relics:"
assert_equals 0 $? "Output should list found files"
echo "$OUTPUT" | grep -q "This was a dry run."
assert_equals 0 $? "Output should indicate dry run"
assert_equals "" "$(cat "$MOCKED_COMMAND_LOG")" "No commands should be mocked in dry run"

# Test 3: Old files found, interactive sweep (user says 'y')
echo "Test 3: Old files found, interactive sweep (user says 'y')"
MOCK_FIND_OUTPUT="$TEST_DIR/old_file_a.txt\n$TEST_DIR/old_file_b.log"
MOCK_READ_INPUT="y"
OUTPUT=$(run_test_script -s "$TEST_DIR" 2>&1)
assert_equals 0 $? "Script should exit with 0 after interactive sweep"
echo "$OUTPUT" | grep -q "Sweeping away the digital dust bunnies..."
assert_equals 0 $? "Output should indicate sweeping"
grep -q "MOCKED_MKDIR $HOME/.digital_dustbin_20230101000000" "$MOCKED_COMMAND_LOG"
assert_equals 0 $? "mkdir should be called"
grep -q "MOCKED_MV $TEST_DIR/old_file_a.txt $HOME/.digital_dustbin_20230101000000/" "$MOCKED_COMMAND_LOG"
assert_equals 0 $? "mv should be called for old_file_a.txt"
grep -q "MOCKED_MV $TEST_DIR/old_file_b.log $HOME/.digital_dustbin_20230101000000/" "$MOCKED_COMMAND_LOG"
assert_equals 0 $? "mv should be called for old_file_b.log"

# Test 4: Old files found, interactive sweep (user says 'N')
echo "Test 4: Old files found, interactive sweep (user says 'N')"
MOCK_FIND_OUTPUT="$TEST_DIR/old_file_c.txt"
MOCK_READ_INPUT="n"
OUTPUT=$(run_test_script -s "$TEST_DIR" 2>&1)
assert_equals 0 $? "Script should exit with 0 when user declines sweep"
echo "$OUTPUT" | grep -q "Digital dust bunnies spared."
assert_equals 0 $? "Output should indicate files spared"
grep -q "MOCKED_MKDIR $HOME/.digital_dustbin_20230101000000" "$MOCKED_COMMAND_LOG"
assert_equals 0 $? "mkdir should be called"
grep -q "MOCKED_RMDIR $HOME/.digital_dustbin_20230101000000" "$MOCKED_COMMAND_LOG"
assert_equals 0 $? "rmdir should be called to clean up empty dustbin"
! grep -q "MOCKED_MV" "$MOCKED_COMMAND_LOG"
assert_equals 0 $? "mv should NOT be called"

# Test 5: Old files found, force sweep
echo "Test 5: Old files found, force sweep"
MOCK_FIND_OUTPUT="$TEST_DIR/old_file_d.txt"
OUTPUT=$(run_test_script -f "$TEST_DIR" 2>&1)
assert_equals 0 $? "Script should exit with 0 after force sweep"
echo "$OUTPUT" | grep -q "Sweeping away the digital dust bunnies..."
assert_equals 0 $? "Output should indicate sweeping"
grep -q "MOCKED_MKDIR $HOME/.digital_dustbin_20230101000000" "$MOCKED_COMMAND_LOG"
assert_equals 0 $? "mkdir should be called"
grep -q "MOCKED_MV $TEST_DIR/old_file_d.txt $HOME/.digital_dustbin_20230101000000/" "$MOCKED_COMMAND_LOG"
assert_equals 0 $? "mv should be called for old_file_d.txt"

# Test 6: Invalid directory
echo "Test 6: Invalid directory"
OUTPUT=$(run_test_script "/non/existent/dir" 2>&1)
assert_equals 1 $? "Script should exit with 1 for invalid directory"
echo "$OUTPUT" | grep -q "Error: Directory '/non/existent/dir' not found or is not a directory."
assert_equals 0 $? "Output should show error for invalid directory"

echo "--- All tests completed ---"
