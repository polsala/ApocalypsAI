#!/bin/bash

# Test suite for nightly-error-whisperer

# Define the path to the script
SCRIPT_PATH="./src/error_whisperer.sh"

# Helper function for assertions
assert_equals() {
    local expected="$1"
    local actual="$2"
    local test_name="$3"

    if [ "$expected" == "$actual" ]; then
        echo "✅ Test passed: $test_name"
        return 0
    else
        echo "❌ Test failed: $test_name"
        echo "   Expected: '$expected'"
        echo "   Actual:   '$actual'"
        return 1
    fi
}

# Ensure the script is executable
chmod +x "$SCRIPT_PATH"

# Test Case 1: Command not found
TEST_INPUT="bash: non_existent_command: command not found"
EXPECTED_OUTPUT="Oops! It seems that command went on a coffee break. Did you spell it right, or is it hiding in your PATH?"
# Mock rationale: Simulating stdin input for the script.
ACTUAL_OUTPUT=$(echo "$TEST_INPUT" | "$SCRIPT_PATH")
assert_equals "$EXPECTED_OUTPUT" "$ACTUAL_OUTPUT" "Command not found (pipe)"

# Test Case 2: Permission denied
TEST_INPUT="rm: cannot remove '/root/secret_file': Permission denied"
EXPECTED_OUTPUT="The digital bouncer says 'No entry!' Perhaps you need a magic 'sudo' spell or to check your access rights?"
# Mock rationale: Simulating stdin input for the script.
ACTUAL_OUTPUT=$(echo "$TEST_INPUT" | "$SCRIPT_PATH")
assert_equals "$EXPECTED_OUTPUT" "$ACTUAL_OUTPUT" "Permission denied (pipe)"

# Test Case 3: No such file or directory
TEST_INPUT="cat: /path/to/non_existent_file: No such file or directory"
EXPECTED_OUTPUT="The file you're looking for seems to have wandered off. Is it in the right folder, or did it change its name?"
# Mock rationale: Simulating stdin input for the script.
ACTUAL_OUTPUT=$(echo "$TEST_INPUT" | "$SCRIPT_PATH")
assert_equals "$EXPECTED_OUTPUT" "$ACTUAL_OUTPUT" "No such file or directory (pipe)"

# Test Case 4: Syntax error
TEST_INPUT="Error: syntax error at line 5"
EXPECTED_OUTPUT="Your code is speaking in riddles! A tiny typo might be causing a grand misunderstanding. Time for a quick proofread?"
# Mock rationale: Simulating stdin input for the script.
ACTUAL_OUTPUT=$(echo "$TEST_INPUT" | "$SCRIPT_PATH")
assert_equals "$EXPECTED_OUTPUT" "$ACTUAL_OUTPUT" "Syntax error (pipe)"

# Test Case 5: Connection refused
TEST_INPUT="ssh: connect to host localhost port 22: Connection refused"
EXPECTED_OUTPUT="The server isn't picking up the phone. Is it running, or is there a firewall dragon guarding the path?"
# Mock rationale: Simulating stdin input for the script.
ACTUAL_OUTPUT=$(echo "$TEST_INPUT" | "$SCRIPT_PATH")
assert_equals "$EXPECTED_OUTPUT" "$ACTUAL_OUTPUT" "Connection refused (pipe)"

# Test Case 6: Disk space
TEST_INPUT="No space left on device"
EXPECTED_OUTPUT="Your digital attic is full! Time to declutter and make some space for new adventures."
# Mock rationale: Simulating stdin input for the script.
ACTUAL_OUTPUT=$(echo "$TEST_INPUT" | "$SCRIPT_PATH")
assert_equals "$EXPECTED_OUTPUT" "$ACTUAL_OUTPUT" "Disk space (pipe)"

# Test Case 7: Out of memory
TEST_INPUT="Memory allocation failed"
EXPECTED_OUTPUT="Your computer's brain is feeling a bit overwhelmed. Maybe close a few tabs or give it a moment to rest?"
# Mock rationale: Simulating stdin input for the script.
ACTUAL_OUTPUT=$(echo "$TEST_INPUT" | "$SCRIPT_PATH")
assert_equals "$EXPECTED_OUTPUT" "$ACTUAL_OUTPUT" "Out of memory (pipe)"

# Test Case 8: Unknown error
TEST_INPUT="FATAL: Unhandled exception 0xDEADBEEF"
EXPECTED_OUTPUT="The digital spirits are a bit muddled. While I ponder this mystery, perhaps a deep breath and a quick search will reveal its secrets?"
# Mock rationale: Simulating stdin input for the script.
ACTUAL_OUTPUT=$(echo "$TEST_INPUT" | "$SCRIPT_PATH")
assert_equals "$EXPECTED_OUTPUT" "$ACTUAL_OUTPUT" "Unknown error (pipe)"

# Test Case 9: Command not found (as argument)
TEST_INPUT_ARG="command not found: python"
EXPECTED_OUTPUT="Oops! It seems that command went on a coffee break. Did you spell it right, or is it hiding in your PATH?"
# Mock rationale: Simulating command-line argument input for the script.
ACTUAL_OUTPUT=$("$SCRIPT_PATH" "$TEST_INPUT_ARG")
assert_equals "$EXPECTED_OUTPUT" "$ACTUAL_OUTPUT" "Command not found (argument)"

# Test Case 10: Case insensitivity
TEST_INPUT="COMMAND NOT FOUND"
EXPECTED_OUTPUT="Oops! It seems that command went on a coffee break. Did you spell it right, or is it hiding in your PATH?"
# Mock rationale: Simulating stdin input for the script.
ACTUAL_OUTPUT=$(echo "$TEST_INPUT" | "$SCRIPT_PATH")
assert_equals "$EXPECTED_OUTPUT" "$ACTUAL_OUTPUT" "Command not found (case insensitive)"

# Test Case 11: Partial match for "no such file or directory"
TEST_INPUT="Error: file not found in /tmp"
EXPECTED_OUTPUT="The file you're looking for seems to have wandered off. Is it in the right folder, or did it change its name?"
# Mock rationale: Simulating stdin input for the script.
ACTUAL_OUTPUT=$(echo "$TEST_INPUT" | "$SCRIPT_PATH")
assert_equals "$EXPECTED_OUTPUT" "$ACTUAL_OUTPUT" "File not found (partial match)"

# Test Case 12: Empty input (should fall to default)
TEST_INPUT=""
EXPECTED_OUTPUT="The digital spirits are a bit muddled. While I ponder this mystery, perhaps a deep breath and a quick search will reveal its secrets?"
# Mock rationale: Simulating empty stdin input for the script.
ACTUAL_OUTPUT=$(echo "$TEST_INPUT" | "$SCRIPT_PATH")
assert_equals "$EXPECTED_OUTPUT" "$ACTUAL_OUTPUT" "Empty input"

# Test Case 13: No input (should prompt, but for testing, we'll simulate an empty pipe which is handled by cat)
# The script's logic for interactive vs. piped input means that if nothing is piped, `cat` will wait.
# For a non-interactive test, an empty pipe will result in an empty `input_error` which then falls to the default.
# This test case is covered by Test Case 12.
# To test the interactive prompt, one would need a more complex mocking setup (e.g., expect/send).
# For deterministic, offline tests, we stick to piped or argument input.

echo "All tests completed."
