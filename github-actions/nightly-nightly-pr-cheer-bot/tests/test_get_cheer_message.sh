#!/bin/bash

# Test script for src/get_cheer_message.sh

# Create a temporary messages file for testing
TEST_MESSAGES_FILE="test_temp_messages.txt"
echo "Test Message One" > "$TEST_MESSAGES_FILE"
echo "Test Message Two" >> "$TEST_MESSAGES_FILE"
echo "Test Message Three" >> "$TEST_MESSAGES_FILE"

# Mock rationale: To make the test deterministic, we control the RANDOM variable.
# By setting TEST_SEED, the get_cheer_message.sh script will use this seed
# instead of true randomness, allowing us to predict the output.

echo "--- Running Test 1: Deterministic selection (seed 0) ---"
TEST_SEED=0 bash src/get_cheer_message.sh "$TEST_MESSAGES_FILE" > output.txt
EXPECTED_OUTPUT="Test Message One"
if grep -q "$EXPECTED_OUTPUT" output.txt; then
  echo "Test 1 Passed: Correct message selected with seed 0."
else
  echo "Test 1 Failed: Expected '$EXPECTED_OUTPUT', got '$(cat output.txt)'"
  rm "$TEST_MESSAGES_FILE" output.txt
  exit 1
fi

echo "--- Running Test 2: Deterministic selection (seed 1) ---"
TEST_SEED=1 bash src/get_cheer_message.sh "$TEST_MESSAGES_FILE" > output.txt
EXPECTED_OUTPUT="Test Message Two"
if grep -q "$EXPECTED_OUTPUT" output.txt; then
  echo "Test 2 Passed: Correct message selected with seed 1."
else
  echo "Test 2 Failed: Expected '$EXPECTED_OUTPUT', got '$(cat output.txt)'"
  rm "$TEST_MESSAGES_FILE" output.txt
  exit 1
fi

echo "--- Running Test 3: Deterministic selection (seed 2) ---"
TEST_SEED=2 bash src/get_cheer_message.sh "$TEST_MESSAGES_FILE" > output.txt
EXPECTED_OUTPUT="Test Message Three"
if grep -q "$EXPECTED_OUTPUT" output.txt; then
  echo "Test 3 Passed: Correct message selected with seed 2."
else
  echo "Test 3 Failed: Expected '$EXPECTED_OUTPUT', got '$(cat output.txt)'"
  rm "$TEST_MESSAGES_FILE" output.txt
  exit 1
fi

echo "--- Running Test 4: Deterministic selection (seed 3 - wraps around) ---"
TEST_SEED=3 bash src/get_cheer_message.sh "$TEST_MESSAGES_FILE" > output.txt
EXPECTED_OUTPUT="Test Message One" # 3 % 3 = 0
if grep -q "$EXPECTED_OUTPUT" output.txt; then
  echo "Test 4 Passed: Correct message selected with seed 3 (wraps)."
else
  echo "Test 4 Failed: Expected '$EXPECTED_OUTPUT', got '$(cat output.txt)'"
  rm "$TEST_MESSAGES_FILE" output.txt
  exit 1
fi

echo "--- Running Test 5: Empty messages file ---"
EMPTY_MESSAGES_FILE="empty_messages.txt"
touch "$EMPTY_MESSAGES_FILE"
if ! bash src/get_cheer_message.sh "$EMPTY_MESSAGES_FILE" 2> error.txt; then
  if grep -q "Error: No messages found" error.txt; then
    echo "Test 5 Passed: Handles empty messages file correctly."
  else
    echo "Test 5 Failed: Expected 'No messages found' error, got '$(cat error.txt)'"
    rm "$TEST_MESSAGES_FILE" output.txt "$EMPTY_MESSAGES_FILE" error.txt
    exit 1
  fi
else
  echo "Test 5 Failed: Script did not exit with error for empty file."
  rm "$TEST_MESSAGES_FILE" output.txt "$EMPTY_MESSAGES_FILE" error.txt
  exit 1
fi

echo "--- Running Test 6: Non-existent messages file ---"
NON_EXISTENT_FILE="non_existent.txt"
if ! bash src/get_cheer_message.sh "$NON_EXISTENT_FILE" 2> error.txt; then
  if grep -q "Error: Messages file not found" error.txt; then
    echo "Test 6 Passed: Handles non-existent messages file correctly."
  else
    echo "Test 6 Failed: Expected 'file not found' error, got '$(cat error.txt)'"
    rm "$TEST_MESSAGES_FILE" output.txt "$EMPTY_MESSAGES_FILE" error.txt
    exit 1
  fi
else
  echo "Test 6 Failed: Script did not exit with error for non-existent file."
  rm "$TEST_MESSAGES_FILE" output.txt "$EMPTY_MESSAGES_FILE" error.txt
  exit 1
fi


# Clean up temporary files
rm "$TEST_MESSAGES_FILE" output.txt "$EMPTY_MESSAGES_FILE" error.txt
echo "All tests passed for get_cheer_message.sh!"
