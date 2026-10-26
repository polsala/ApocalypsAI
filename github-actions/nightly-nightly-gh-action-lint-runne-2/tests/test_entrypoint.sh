#!/bin/bash

# Mock yamllint command
# Mock rationale: We are mocking the 'yamllint' command to simulate its behavior without needing to install it or have actual workflow files present. This allows for deterministic, offline testing of the script's logic, specifically how it handles arguments and interprets exit codes.
_mock_yamllint() {
  echo "Mock yamllint called with: $@"
  # Simulate success for valid files, failure for invalid ones
  if echo "$@" | grep -q 'invalid_workflow.yml'; then
    echo "Mock yamllint: Found errors in invalid_workflow.yml"
    return 1 # Simulate failure
  else
    echo "Mock yamllint: No errors found."
    return 0 # Simulate success
  fi
}

# Override the actual yamllint command with our mock
_YAMLLINT_MOCK=_mock_yamllint

# --- Test Case 1: Default path, no errors --- 
echo "--- Test Case 1: Default path, no errors ---"
# Mock rationale: This test ensures the script correctly uses the default path and calls the mocked yamllint with the expected arguments when no input is provided.
if ./
  ./src/entrypoint.sh ""
  _YAMLLINT_MOCK "$WORKFLOW_PATH"*.yml
then
  echo "Test Case 1 Passed."
else
  echo "Test Case 1 Failed."
  exit 1
fi

# --- Test Case 2: Specific path, no errors --- 
echo "\n--- Test Case 2: Specific path, no errors ---"
# Mock rationale: This test verifies that the script correctly uses a user-provided path and passes it to the mocked yamllint.
if ./
  ./src/entrypoint.sh "./test_workflows/"
  _YAMLLINT_MOCK "./test_workflows/"*.yml
then
  echo "Test Case 2 Passed."
else
  echo "Test Case 2 Failed."
  exit 1
fi

# --- Test Case 3: Specific path, with errors --- 
echo "\n--- Test Case 3: Specific path, with errors ---"
# Mock rationale: This test checks if the script correctly identifies a failure from yamllint and exits with a non-zero status code, indicating an error.
if ./
  ./src/entrypoint.sh "./test_workflows/"
  _YAMLLINT_MOCK "./test_workflows/"*.yml
then
  echo "Test Case 3 Failed (expected failure).
  exit 1
else
  echo "Test Case 3 Passed (correctly failed).
fi

# --- Test Case 4: Empty directory (should pass) --- 
echo "\n--- Test Case 4: Empty directory (should pass) ---"
# Mock rationale: This test ensures that if the specified directory contains no YAML files, the script does not error out and yamllint is not called in a way that would cause a failure.
if ./
  ./src/entrypoint.sh "./empty_dir/"
  _YAMLLINT_MOCK "./empty_dir/"*.yml
then
  echo "Test Case 4 Passed."
else
  echo "Test Case 4 Failed."
  exit 1
fi

echo "\nAll tests completed."
