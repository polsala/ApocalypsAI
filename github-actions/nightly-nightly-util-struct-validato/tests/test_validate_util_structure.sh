#!/bin/bash

# Mock rationale: This test script directly invokes the validation logic
# (`validate_util_structure.sh`) with various simulated directory structures.
# It doesn't interact with GitHub APIs or external services, making it
# deterministic and offline. Temporary directories are created and cleaned up
# to isolate test runs.

SCRIPT_TO_TEST="./src/validate_util_structure.sh"

# Function to create a temporary directory for a test case
create_test_dir() {
  local name="$1"
  TEST_DIR=$(mktemp -d "/tmp/test_util_struct_validator_$name.XXXXXX")
  echo "$TEST_DIR"
}

# Function to clean up temporary directories
cleanup() {
  if [ -d "$TEST_DIR" ]; then
    rm -rf "$TEST_DIR"
  fi
}
trap cleanup EXIT # Ensure cleanup on exit

echo "Running tests for validate_util_structure.sh"

# Test Case 1: Valid structure
echo "Test Case 1: Valid structure"
TEST_DIR=$(create_test_dir "valid")
mkdir -p "$TEST_DIR/src" "$TEST_DIR/tests"
touch "$TEST_DIR/README.md" "$TEST_DIR/src/main.sh" "$TEST_DIR/tests/test.sh"
if bash "$SCRIPT_TO_TEST" "$TEST_DIR"; then
  echo "PASS: Valid structure correctly passed."
else
  echo "FAIL: Valid structure incorrectly failed."
  exit 1
fi
cleanup

# Test Case 2: Missing README.md
echo "Test Case 2: Missing README.md"
TEST_DIR=$(create_test_dir "no_readme")
mkdir -p "$TEST_DIR/src" "$TEST_DIR/tests"
touch "$TEST_DIR/src/main.sh" "$TEST_DIR/tests/test.sh"
if ! bash "$SCRIPT_TO_TEST" "$TEST_DIR"; then
  echo "PASS: Missing README.md correctly failed."
else
  echo "FAIL: Missing README.md incorrectly passed."
  exit 1
fi
cleanup

# Test Case 3: Missing src/ directory
echo "Test Case 3: Missing src/ directory"
TEST_DIR=$(create_test_dir "no_src_dir")
mkdir -p "$TEST_DIR/tests"
touch "$TEST_DIR/README.md" "$TEST_DIR/tests/test.sh"
if ! bash "$SCRIPT_TO_TEST" "$TEST_DIR"; then
  echo "PASS: Missing src/ directory correctly failed."
else
  echo "FAIL: Missing src/ directory incorrectly passed."
  exit 1
fi
cleanup

# Test Case 4: Empty src/ directory
echo "Test Case 4: Empty src/ directory"
TEST_DIR=$(create_test_dir "empty_src")
mkdir -p "$TEST_DIR/src" "$TEST_DIR/tests"
touch "$TEST_DIR/README.md" "$TEST_DIR/tests/test.sh"
if ! bash "$SCRIPT_TO_TEST" "$TEST_DIR"; then
  echo "PASS: Empty src/ directory correctly failed."
else
  echo "FAIL: Empty src/ directory incorrectly passed."
  exit 1
fi
cleanup

# Test Case 5: Missing tests/ directory
echo "Test Case 5: Missing tests/ directory"
TEST_DIR=$(create_test_dir "no_tests_dir")
mkdir -p "$TEST_DIR/src"
touch "$TEST_DIR/README.md" "$TEST_DIR/src/main.sh"
if ! bash "$SCRIPT_TO_TEST" "$TEST_DIR"; then
  echo "PASS: Missing tests/ directory correctly failed."
else
  echo "FAIL: Missing tests/ directory incorrectly passed."
  exit 1
fi
cleanup

# Test Case 6: Empty tests/ directory
echo "Test Case 6: Empty tests/ directory"
TEST_DIR=$(create_test_dir "empty_tests")
mkdir -p "$TEST_DIR/src" "$TEST_DIR/tests"
touch "$TEST_DIR/README.md" "$TEST_DIR/src/main.sh"
if ! bash "$SCRIPT_TO_TEST" "$TEST_DIR"; then
  echo "PASS: Empty tests/ directory correctly failed."
else
  echo "FAIL: Empty tests/ directory incorrectly passed."
  exit 1
fi
cleanup

# Test Case 7: Non-existent utility path
echo "Test Case 7: Non-existent utility path"
TEST_DIR="/tmp/non_existent_path_$(date +%s%N)" # Ensure it doesn't exist
if ! bash "$SCRIPT_TO_TEST" "$TEST_DIR"; then
  echo "PASS: Non-existent utility path correctly failed."
else
  echo "FAIL: Non-existent utility path incorrectly passed."
  exit 1
fi
# No cleanup needed as it was never created

echo "All tests completed."
