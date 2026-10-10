#!/bin/bash

set -euo pipefail

# Mocking function for 'command -v'
mock_command_exists() {
  local cmd="$1"
  shift
  local return_code="$1"
  shift
  local output="$@"
  echo "mock_command_exists: $cmd, return_code: $return_code, output: '$output'"
  if [ "$cmd" = "yamllint" ]; then
    if [ "$return_code" -eq 0 ]; then
      return 0
    else
      return 1
    fi
  else
    return 1 # Default to not found
  fi
}

# Mocking function for 'find'
mock_find() {
  local path="$1"
  shift
  local return_code="$1"
  shift
  local output="$@"
  echo "mock_find: path: '$path', return_code: $return_code, output: '$output'"
  if [ "$path" = ".github/workflows/" ]; then
    if [ "$return_code" -eq 0 ]; then
      echo "$output"
    else
      return 1
    fi
  else
    return 1
  fi
}

# Mocking function for 'grep'
mock_grep() {
  local pattern="$1"
  shift
  local file="$1"
  shift
  local return_code="$1"
  shift
  local output="$@"
  echo "mock_grep: pattern: '$pattern', file: '$file', return_code: $return_code, output: '$output'"
  if [ "$pattern" = "runs-on:" ] && [ "$file" = "tests/mock_workflows/valid_workflow.yml" ]; then
    return 0 # Found
  elif [ "$pattern" = "runs-on:" ] && [ "$file" = "tests/mock_workflows/no_runs_on.yml" ]; then
    return 1 # Not found
  elif [ "$pattern" = "^on \(\\|[^:]\)" ] && [ "$file" = "tests/mock_workflows/typo_workflow.yml" ]; then
    return 0 # Found typo
  elif [ "$pattern" = "^on \(\\|[^:]\)" ] && [ "$file" = "tests/mock_workflows/valid_workflow.yml" ]; then
    return 1 # No typo
  else
    return 1
  fi
}

# Mocking function for 'exit'
mock_exit() {
  local code="$1"
  echo "mock_exit: $code"
  # In a real test, you might want to assert the exit code here
  # For simplicity, we'll just print and continue, or you could throw an error
  if [ "$code" -ne 0 ]; then
    # Simulate failure for tests expecting it
    return $code
  fi
}

# --- Test Setup ---

# Create mock workflow files
mkdir -p tests/mock_workflows

# Valid workflow
cat <<EOF > tests/mock_workflows/valid_workflow.yml
name: Test Workflow

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
EOF

# Workflow with typo in 'on'
cat <<EOF > tests/mock_workflows/typo_workflow.yml
name: Typo Workflow

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
EOF

# Workflow missing 'runs-on'
cat <<EOF > tests/mock_workflows/no_runs_on.yml
name: No Runs On Workflow

on:
  push:
    branches: [ main ]

jobs:
  build:
    steps:
      - name: Checkout
        uses: actions/checkout@v4
EOF

# Empty workflow file
cat <<EOF > tests/mock_workflows/empty.yml
EOF

# --- Test Cases ---

run_test() {
  local test_name="$1"
  echo "--- Running Test: $test_name ---"
  # Reset mocks for each test
  command_exists_orig() { command -v "$@"; }
  find_orig() { find "$@"; }
  grep_orig() { grep "$@"; }
  exit_orig() { exit "$@"; }

  # Override built-in commands with mocks
  command -v() { mock_command_exists "$@"; }
  find() { mock_find "$@"; }
  grep() { mock_grep "$@"; }
  exit() { mock_exit "$@"; }

  # Execute the script with specific inputs
  if [ "$test_name" = "test_valid_workflow" ]; then
    INPUT_WORKFLOW_PATH=tests/mock_workflows/
    INPUT_VERBOSE=true
    # Mock yamllint to succeed
    mock_command_exists yamllint 0
    mock_find tests/mock_workflows "$WORKFLOW_FILES" "tests/mock_workflows/valid_workflow.yml"
    mock_grep "runs-on:" "tests/mock_workflows/valid_workflow.yml" 0
    mock_grep "^on \(\\|[^:]\)" "tests/mock_workflows/valid_workflow.yml" 1
    # Expect success
    if ./src/main.sh; then
      echo "Test Passed: $test_name"
    else
      echo "Test Failed: $test_name - Script exited with non-zero status."
    fi
  elif [ "$test_name" = "test_typo_workflow" ]; then
    INPUT_WORKFLOW_PATH=tests/mock_workflows/
    INPUT_VERBOSE=true
    # Mock yamllint to succeed
    mock_command_exists yamllint 0
    mock_find tests/mock_workflows "$WORKFLOW_FILES" "tests/mock_workflows/typo_workflow.yml"
    mock_grep "runs-on:" "tests/mock_workflows/typo_workflow.yml" 0
    mock_grep "^on \(\\|[^:]\)" "tests/mock_workflows/typo_workflow.yml" 0 # Simulate typo found
    # Expect failure
    if ! ./src/main.sh; then
      echo "Test Passed: $test_name"
    else
      echo "Test Failed: $test_name - Script did not exit with non-zero status."
    fi
  elif [ "$test_name" = "test_no_runs_on" ]; then
    INPUT_WORKFLOW_PATH=tests/mock_workflows/
    INPUT_VERBOSE=true
    # Mock yamllint to succeed
    mock_command_exists yamllint 0
    mock_find tests/mock_workflows "$WORKFLOW_FILES" "tests/mock_workflows/no_runs_on.yml"
    mock_grep "runs-on:" "tests/mock_workflows/no_runs_on.yml" 1 # Simulate runs-on not found
    mock_grep "^on \(\\|[^:]\)" "tests/mock_workflows/no_runs_on.yml" 1
    # Expect success (as 'runs-on' check is a warning)
    if ./src/main.sh; then
      echo "Test Passed: $test_name"
    else
      echo "Test Failed: $test_name - Script exited with non-zero status."
    fi
  elif [ "$test_name" = "test_no_workflows_found_fail" ]; then
    INPUT_WORKFLOW_PATH=tests/nonexistent_path/
    INPUT_FAIL_IF_NO_WORKFLOWS=true
    INPUT_VERBOSE=true
    # Mock find to return nothing
    mock_find tests/nonexistent_path "$WORKFLOW_FILES" ""
    # Expect failure
    if ! ./src/main.sh; then
      echo "Test Passed: $test_name"
    else
      echo "Test Failed: $test_name - Script did not exit with non-zero status."
    fi
  elif [ "$test_name" = "test_no_workflows_found_skip" ]; then
    INPUT_WORKFLOW_PATH=tests/nonexistent_path/
    INPUT_FAIL_IF_NO_WORKFLOWS=false
    INPUT_VERBOSE=true
    # Mock find to return nothing
    mock_find tests/nonexistent_path "$WORKFLOW_FILES" ""
    # Expect success (script should exit cleanly)
    if ./src/main.sh; then
      echo "Test Passed: $test_name"
    else
      echo "Test Failed: $test_name - Script exited with non-zero status."
    fi
  elif [ "$test_name" = "test_yamllint_fails" ]; then
    INPUT_WORKFLOW_PATH=tests/mock_workflows/
    INPUT_VERBOSE=true
    # Mock yamllint to fail
    mock_command_exists yamllint 1
    mock_find tests/mock_workflows "$WORKFLOW_FILES" "tests/mock_workflows/valid_workflow.yml"
    # Expect failure due to yamllint
    if ! ./src/main.sh; then
      echo "Test Passed: $test_name"
    else
      echo "Test Failed: $test_name - Script did not exit with non-zero status."
    fi
  fi

  # Restore original commands
  command -v() { command_exists_orig "$@"; }
  find() { find_orig "$@"; }
  grep() { grep_orig "$@"; }
  exit() { exit_orig "$@"; }
}

# Run all tests
run_test "test_valid_workflow"
run_test "test_typo_workflow"
run_test "test_no_runs_on"
run_test "test_no_workflows_found_fail"
run_test "test_no_workflows_found_skip"
run_test "test_yamllint_fails"

echo "All tests completed."
