#!/bin/bash

# Mock rationale: This script uses Docker Compose to simulate the environment and dependencies.
# It creates mock files and directories to test the entrypoint script's behavior without external dependencies.

set -euo pipefail

# --- Mock Setup ---

# Create a temporary directory for testing
TEST_DIR=$(mktemp -d)

# Create mock files
# A valid YAML file
mkdir -p "$TEST_DIR/.github/workflows"
cat <<EOF > "$TEST_DIR/.github/workflows/valid_workflow.yml"
name: Valid Workflow

on: push

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
EOF

# An invalid YAML file (missing colon)
cat <<EOF > "$TEST_DIR/.github/workflows/invalid_yaml.yml"
name: Invalid Workflow

on push

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
EOF

# A workflow file with a common mistake (e.g., incorrect step syntax)
cat <<EOF > "$TEST_DIR/.github/workflows/invalid_action_syntax.yml"
name: Invalid Action Syntax Workflow

on: push

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      - name: Run a command
        run: echo "Hello"
      - name: Incorrect step format
        uses: some/action
        with:
          arg1: val1
          arg2: val2
EOF

# A file that should be excluded
cat <<EOF > "$TEST_DIR/.github/workflows/excluded_file.yml"
name: Excluded File

on: pull_request

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
EOF

# --- Test Cases ---

echo "Running tests..."

# Test Case 1: All valid files, no exclusions
echo "--- Test Case 1: All valid files, no exclusions ---"
(cd "$TEST_DIR" && docker run --rm -v "$(pwd)":/app -w /app polsala/ApocalypsAI/nightly-gh-action-lint-runner:latest --paths ".github/workflows/" --fail_on_error true)
if [ $? -eq 0 ]; then
  echo "Test Case 1 PASSED"
else
  echo "Test Case 1 FAILED"
  exit 1
fi

# Test Case 2: Invalid YAML file, should fail
echo "\n--- Test Case 2: Invalid YAML file, should fail ---"
(cd "$TEST_DIR" && docker run --rm -v "$(pwd)":/app -w /app polsala/ApocalypsAI/nightly-gh-action-lint-runner:latest --paths ".github/workflows/invalid_yaml.yml" --fail_on_error true)
if [ $? -ne 0 ]; then
  echo "Test Case 2 PASSED"
else
  echo "Test Case 2 FAILED"
  exit 1
fi

# Test Case 3: Invalid Action syntax, should fail
echo "\n--- Test Case 3: Invalid Action syntax, should fail ---"
(cd "$TEST_DIR" && docker run --rm -v "$(pwd)":/app -w /app polsala/ApocalypsAI/nightly-gh-action-lint-runner:latest --paths ".github/workflows/invalid_action_syntax.yml" --fail_on_error true)
if [ $? -ne 0 ]; then
  echo "Test Case 3 PASSED"
else
  echo "Test Case 3 FAILED"
  exit 1
fi

# Test Case 4: Exclude a file that would otherwise fail (e.g., invalid YAML)
echo "\n--- Test Case 4: Exclude a file that would otherwise fail ---"
(cd "$TEST_DIR" && docker run --rm -v "$(pwd)":/app -w /app polsala/ApocalypsAI/nightly-gh-action-lint-runner:latest --paths ".github/workflows/" --exclude_paths ".github/workflows/invalid_yaml.yml" --fail_on_error true)
if [ $? -eq 0 ]; then
  echo "Test Case 4 PASSED"
else
  echo "Test Case 4 FAILED"
  exit 1
fi

# Test Case 5: Fail on error is false, should not exit with non-zero status on error
echo "\n--- Test Case 5: Fail on error is false, should not exit with non-zero status on error ---"
(cd "$TEST_DIR" && docker run --rm -v "$(pwd)":/app -w /app polsala/ApocalypsAI/nightly-gh-action-lint-runner:latest --paths ".github/workflows/invalid_yaml.yml" --fail_on_error false)
if [ $? -eq 0 ]; then
  echo "Test Case 5 PASSED"
else
  echo "Test Case 5 FAILED"
  exit 1
fi

# Test Case 6: Linting only specific valid file
echo "\n--- Test Case 6: Linting only specific valid file ---"
(cd "$TEST_DIR" && docker run --rm -v "$(pwd)":/app -w /app polsala/ApocalypsAI/nightly-gh-action-lint-runner:latest --paths ".github/workflows/valid_workflow.yml" --fail_on_error true)
if [ $? -eq 0 ]; then
  echo "Test Case 6 PASSED"
else
  echo "Test Case 6 FAILED"
  exit 1
fi

# Test Case 7: No paths specified (should default to current dir)
echo "\n--- Test Case 7: No paths specified (should default to current dir) ---"
(cd "$TEST_DIR" && docker run --rm -v "$(pwd)":/app -w /app polsala/ApocalypsAI/nightly-gh-action-lint-runner:latest --fail_on_error true)
if [ $? -eq 0 ]; then
  echo "Test Case 7 PASSED"
else
  echo "Test Case 7 FAILED"
  exit 1
fi

# --- Cleanup ---
rm -rf "$TEST_DIR"

echo "All tests completed."
