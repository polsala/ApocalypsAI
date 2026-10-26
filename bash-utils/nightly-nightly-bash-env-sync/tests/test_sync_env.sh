#!/bin/bash

# nightly-bash-env-sync - Test Script

# --- Mock Setup ---
# Create a dummy environment file for testing.
# Mock rationale: This file simulates the input to the sync_env.sh script.
TEST_ENV_FILE="mock_env.env"
echo "export TEST_VAR_1=\"hello\"" > "$TEST_ENV_FILE"
echo "export TEST_VAR_2=\"world\"" >> "$TEST_ENV_FILE"
echo "export TEST_VAR_3=\"12345\"" >> "$TEST_ENV_FILE"

# --- Test Cases ---

# Test Case 1: Successful synchronization
run_test_1() {
  echo "Running Test Case 1: Successful synchronization..."
  # Mock rationale: We need to capture the output of the script to verify it.
  # We also need to ensure the script runs without errors.
  OUTPUT=$(bash ../src/sync_env.sh "$TEST_ENV_FILE" 2>&1)
  EXIT_CODE=$?

  if [ $EXIT_CODE -eq 0 ]; then
    echo "  [PASS] Script executed successfully."
  else
    echo "  [FAIL] Script exited with code $EXIT_CODE. Output: $OUTPUT"
    return 1
  fi

  # Mock rationale: Verify that the exported variables are now set in the test environment.
  # We use 'env | grep' to check for the presence and value of the variables.
  if env | grep -q "TEST_VAR_1=hello" && env | grep -q "TEST_VAR_2=world" && env | grep -q "TEST_VAR_3=12345"; then
    echo "  [PASS] Environment variables TEST_VAR_1, TEST_VAR_2, and TEST_VAR_3 are set correctly."
  else
    echo "  [FAIL] Environment variables are not set correctly."
    env | grep TEST_VAR_
    return 1
  fi

  echo "  Test Case 1 Passed."
  return 0
}

# Test Case 2: Missing source file
run_test_2() {
  echo "Running Test Case 2: Missing source file..."
  OUTPUT=$(bash ../src/sync_env.sh "non_existent_file.env" 2>&1)
  EXIT_CODE=$?

  if [ $EXIT_CODE -ne 0 ]; then
    echo "  [PASS] Script exited with non-zero code as expected."
  else
    echo "  [FAIL] Script exited with code 0, but expected an error."
    return 1
  fi

  # Mock rationale: Verify the error message indicates the file was not found or readable.
  if echo "$OUTPUT" | grep -q "Error: Source file 'non_existent_file.env' not found or not readable."; then
    echo "  [PASS] Correct error message displayed."
  else
    echo "  [FAIL] Incorrect error message. Output: $OUTPUT"
    return 1
  fi

  echo "  Test Case 2 Passed."
  return 0
}

# Test Case 3: No argument provided
run_test_3() {
  echo "Running Test Case 3: No argument provided..."
  OUTPUT=$(bash ../src/sync_env.sh 2>&1)
  EXIT_CODE=$?

  if [ $EXIT_CODE -ne 0 ]; then
    echo "  [PASS] Script exited with non-zero code as expected."
  else
    echo "  [FAIL] Script exited with code 0, but expected an error."
    return 1
  fi

  # Mock rationale: Verify the usage message is displayed.
  if echo "$OUTPUT" | grep -q "Usage: ../src/sync_env.sh <source_env_file>"; then
    echo "  [PASS] Correct usage message displayed."
  else
    echo "  [FAIL] Incorrect usage message. Output: $OUTPUT"
    return 1
  fi

  echo "  Test Case 3 Passed."
  return 0
}

# --- Test Execution ---

TOTAL_TESTS=3
PASSED_TESTS=0

run_test_1 && PASSED_TESTS=$((PASSED_TESTS + 1))
run_test_2 && PASSED_TESTS=$((PASSED_TESTS + 1))
run_test_3 && PASSED_TESTS=$((PASSED_TESTS + 1))

# --- Cleanup ---
# Mock rationale: Clean up the dummy environment file after tests.
rm -f "$TEST_ENV_FILE"

# --- Summary ---

echo "--------------------"
echo "Test Summary: $PASSED_TESTS / $TOTAL_TESTS tests passed."

if [ $PASSED_TESTS -eq $TOTAL_TESTS ]; then
  exit 0
else
  exit 1
fi
