#!/bin/bash
set -euo pipefail

# Mock rationale: We are mocking the file system and external commands to ensure deterministic testing.
# The 'yamllint' command is mocked to return specific exit codes and output.

# Create a temporary directory for tests
TEST_DIR=$(mktemp -d)

# --- Mocking Functions ---

# Mock yamllint command
mock_yamllint() {
  local exit_code=$1
  local output="$2"
  echo "Mock yamllint called with: $@"
  echo "$output"
  return $exit_code
}

# Mock find command
mock_find() {
  local files_to_return="$1"
  echo "Mock find called with: $@"
  echo "$files_to_return"
}

# Mock apt-get install (to simulate installation if needed, though we pre-install in Dockerfile for this action)
mock_apt_get_install() {
  echo "Mock apt-get install called with: $@"
  return 0
}

# Override actual commands with mocks
_orig_yamllint() { :; }; _orig_find() { :; }; _orig_apt_get_install() { :; }

# --- Test Cases ---

# Test Case 1: Successful linting
run_test_success() {
  echo "--- Running Test Case 1: Successful Linting ---"
  mkdir -p "$TEST_DIR/.github/workflows"
  echo "valid workflow content" > "$TEST_DIR/.github/workflows/main.yml"
  echo "another valid workflow" > "$TEST_DIR/.github/workflows/deploy.yml"

  # Mock find to return the files in the test directory
  # Mock yamllint to succeed (exit code 0)
  YAMLLINT_MOCK_EXIT_CODE=0
  YAMLLINT_MOCK_OUTPUT=""
  FIND_MOCK_FILES="$TEST_DIR/.github/workflows/main.yml\0$TEST_DIR/.github/workflows/deploy.yml"

  # Temporarily replace commands with mocks
  _orig_yamllint=$(command -v yamllint)
  _orig_find=$(command -v find)
  _orig_apt_get_install=$(command -v apt-get)

  command -v yamllint >/dev/null 2>&1 || alias yamllint='mock_yamllint'
  command -v find >/dev/null 2>&1 || alias find='mock_find'
  command -v apt-get >/dev/null 2>&1 || alias apt-get='mock_apt_get_install'

  # Execute the entrypoint script within the test directory context
  (cd "$TEST_DIR" && ../src/entrypoint.sh)
  TEST_EXIT_CODE=$?

  # Restore original commands
  if command -v yamllint >/dev/null 2>&1 && [[ $(alias yamllint 2>/dev/null) == *mock_yamllint* ]]; then unalias yamllint; fi
  if command -v find >/dev/null 2>&1 && [[ $(alias find 2>/dev/null) == *mock_find* ]]; then unalias find; fi
  if command -v apt-get >/dev/null 2>&1 && [[ $(alias apt-get 2>/dev/null) == *mock_apt_get_install* ]]; then unalias apt-get; fi

  if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "Test Case 1 PASSED."
  else
    echo "Test Case 1 FAILED. Expected exit code 0, got $TEST_EXIT_CODE."
    exit 1
  fi
}

# Test Case 2: Linting failure
run_test_failure() {
  echo "" # Newline for separation
  echo "--- Running Test Case 2: Linting Failure ---"
  mkdir -p "$TEST_DIR/.github/workflows"
  echo "invalid workflow content" > "$TEST_DIR/.github/workflows/bad.yml"

  # Mock find to return the bad file
  # Mock yamllint to fail (exit code 1) and return an error message
  YAMLLINT_MOCK_EXIT_CODE=1
  YAMLLINT_MOCK_OUTPUT="bad.yml:1:1: error: invalid YAML syntax (yaml error)"
  FIND_MOCK_FILES="$TEST_DIR/.github/workflows/bad.yml"

  # Temporarily replace commands with mocks
  _orig_yamllint=$(command -v yamllint)
  _orig_find=$(command -v find)
  _orig_apt_get_install=$(command -v apt-get)

  command -v yamllint >/dev/null 2>&1 || alias yamllint='mock_yamllint'
  command -v find >/dev/null 2>&1 || alias find='mock_find'
  command -v apt-get >/dev/null 2>&1 || alias apt-get='mock_apt_get_install'

  # Execute the entrypoint script within the test directory context
  (cd "$TEST_DIR" && ../src/entrypoint.sh)
  TEST_EXIT_CODE=$?

  # Restore original commands
  if command -v yamllint >/dev/null 2>&1 && [[ $(alias yamllint 2>/dev/null) == *mock_yamllint* ]]; then unalias yamllint; fi
  if command -v find >/dev/null 2>&1 && [[ $(alias find 2>/dev/null) == *mock_find* ]]; then unalias find; fi
  if command -v apt-get >/dev/null 2>&1 && [[ $(alias apt-get 2>/dev/null) == *mock_apt_get_install* ]]; then unalias apt-get; fi

  if [ $TEST_EXIT_CODE -eq 1 ]; then
    echo "Test Case 2 PASSED."
  else
    echo "Test Case 2 FAILED. Expected exit code 1, got $TEST_EXIT_CODE."
    exit 1
  fi
}

# Test Case 3: Custom workflow path
run_test_custom_path() {
  echo "" # Newline for separation
  echo "--- Running Test Case 3: Custom Workflow Path ---"
  mkdir -p "$TEST_DIR/my_workflows"
  echo "valid workflow content" > "$TEST_DIR/my_workflows/custom.yml"

  # Mock find to return the file in the custom path
  # Mock yamllint to succeed
  YAMLLINT_MOCK_EXIT_CODE=0
  YAMLLINT_MOCK_OUTPUT=""
  FIND_MOCK_FILES="$TEST_DIR/my_workflows/custom.yml"

  # Temporarily replace commands with mocks
  _orig_yamllint=$(command -v yamllint)
  _orig_find=$(command -v find)
  _orig_apt_get_install=$(command -v apt-get)

  command -v yamllint >/dev/null 2>&1 || alias yamllint='mock_yamllint'
  command -v find >/dev/null 2>&1 || alias find='mock_find'
  command -v apt-get >/dev/null 2>&1 || alias apt-get='mock_apt_get_install'

  # Execute the entrypoint script with the custom path input
  (cd "$TEST_DIR" && INPUT_WORKFLOW_PATH=my_workflows ../src/entrypoint.sh)
  TEST_EXIT_CODE=$?

  # Restore original commands
  if command -v yamllint >/dev/null 2>&1 && [[ $(alias yamllint 2>/dev/null) == *mock_yamllint* ]]; then unalias yamllint; fi
  if command -v find >/dev/null 2>&1 && [[ $(alias find 2>/dev/null) == *mock_find* ]]; then unalias find; fi
  if command -v apt-get >/dev/null 2>&1 && [[ $(alias apt-get 2>/dev/null) == *mock_apt_get_install* ]]; then unalias apt-get; fi

  if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "Test Case 3 PASSED."
  else
    echo "Test Case 3 FAILED. Expected exit code 0, got $TEST_EXIT_CODE."
    exit 1
  fi
}

# --- Execution ---

# Clean up temporary directory on exit
trap "rm -rf '$TEST_DIR'" EXIT

run_test_success
run_test_failure
run_test_custom_path

echo "All tests completed successfully."
exit 0
