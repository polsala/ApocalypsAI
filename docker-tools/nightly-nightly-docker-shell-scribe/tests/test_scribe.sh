#!/bin/bash

# Mock rationale: We are testing a shell script that interacts with the filesystem
# and the 'date' command. To make tests deterministic and offline, we will:
# 1. Use a temporary file for COMMAND_LOG_FILE instead of the default.
# 2. Mock the 'date' command to return a fixed timestamp.

# --- Test Setup ---
TEST_LOG_FILE=$(mktemp)
export COMMAND_LOG_FILE="$TEST_LOG_FILE" # Override the default log file for tests

# Mock the date command for deterministic timestamps
MOCKED_DATE_OUTPUT="2023-01-01 12:00:00"
date() {
    echo "$MOCKED_DATE_OUTPUT"
}
export -f date # Export the function so it's available in subshells if needed

# Source the script to be tested
SCRIBE_SCRIPT_PATH="src/scribe.sh"

# --- Helper Functions ---
assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [ "$expected" = "$actual" ]; then
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
    if echo "$haystack" | grep -q "$needle"; then
        echo "PASS: $message"
    else
        echo "FAIL: $message"
        echo "  Expected to contain: '$needle'"
        echo "  Actual content: '$haystack'"
        exit 1
    fi
}

assert_empty_file() {
    local file="$1"
    local message="$2"
    if [ ! -s "$file" ]; then # -s checks if file exists and has size > 0
        echo "PASS: $message"
    else
        echo "FAIL: $message"
        echo "  File '$file' was not empty."
        cat "$file"
        exit 1
    fi
}

assert_not_empty_file() {
    local file="$1"
    local message="$2"
    if [ -s "$file" ]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message"
        echo "  File '$file' was empty."
        exit 1
    fi
}

# --- Test Cases ---

echo "Running tests for scribe.sh..."

# Test 1: Record a single command
echo "--- Test 1: Record a single command ---"
"$SCRIBE_SCRIPT_PATH" record "echo 'Hello World'" > /dev/null
assert_not_empty_file "$TEST_LOG_FILE" "Log file should not be empty after recording"
LOG_CONTENT=$(cat "$TEST_LOG_FILE")
assert_equals "[$MOCKED_DATE_OUTPUT] echo 'Hello World'" "$LOG_CONTENT" "Recorded command should match"
echo ""

# Test 2: Record multiple commands
echo "--- Test 2: Record multiple commands ---"
"$SCRIBE_SCRIPT_PATH" record "ls -la" > /dev/null
LOG_CONTENT=$(cat "$TEST_LOG_FILE")
EXPECTED_CONTENT="[$MOCKED_DATE_OUTPUT] echo 'Hello World'\n[$MOCKED_DATE_OUTPUT] ls -la"
assert_equals "$EXPECTED_CONTENT" "$LOG_CONTENT" "Multiple recorded commands should match"
echo ""

# Test 3: Replay commands
echo "--- Test 3: Replay commands ---"
REPLAY_OUTPUT=$("$SCRIBE_SCRIPT_PATH" replay)
assert_contains "$REPLAY_OUTPUT" "[Temporal Echo]: [$MOCKED_DATE_OUTPUT] echo 'Hello World'" "Replay output should contain first command"
assert_contains "$REPLAY_OUTPUT" "[Temporal Echo]: [$MOCKED_DATE_OUTPUT] ls -la" "Replay output should contain second command"
assert_contains "$REPLAY_OUTPUT" "--- Temporal Echoes from the Vault ---" "Replay output should have header"
assert_contains "$REPLAY_OUTPUT" "--------------------------------------" "Replay output should have footer"
echo ""

# Test 4: Clear commands
echo "--- Test 4: Clear commands ---"
"$SCRIBE_SCRIPT_PATH" clear > /dev/null
assert_empty_file "$TEST_LOG_FILE" "Log file should be empty after clearing"
echo ""

# Test 5: Replay when empty
echo "--- Test 5: Replay when empty ---"
REPLAY_OUTPUT=$("$SCRIBE_SCRIPT_PATH" replay)
assert_contains "$REPLAY_OUTPUT" "The temporal vault is empty. No echoes to replay." "Replay empty vault message"
echo ""

# Test 6: Invalid argument
echo "--- Test 6: Invalid argument ---"
INVALID_OUTPUT=$("$SCRIBE_SCRIPT_PATH" invalid_arg 2>&1)
assert_contains "$INVALID_OUTPUT" "Usage: scribe.sh [record \"<command>\" | replay | clear]" "Invalid argument usage message"
echo ""

# Test 7: Record without command
echo "--- Test 7: Record without command ---"
INVALID_OUTPUT=$("$SCRIBE_SCRIPT_PATH" record 2>&1)
assert_contains "$INVALID_OUTPUT" "Usage: scribe.sh record \"<command_to_record>\"" "Record without command usage message"
echo ""

# --- Cleanup ---
rm "$TEST_LOG_FILE"
unset -f date # Unset the mocked date function
echo "All tests passed!"
