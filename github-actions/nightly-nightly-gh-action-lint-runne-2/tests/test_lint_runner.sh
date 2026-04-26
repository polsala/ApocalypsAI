#!/bin/bash
set -euo pipefail

# Mock rationale: This script uses docker-compose to spin up a test environment.
# It creates dummy workflow files, some valid and some invalid, and then runs the
# lint-runner container against them. The exit codes and output are checked to
# verify the action's behavior.

# Ensure docker-compose is available
if ! command -v docker-compose &> /dev/null
then
    echo "docker-compose could not be found. Please install it." >&2
    exit 1
fi

# Create a directory for test workflows
mkdir -p test_workflows

# --- Test Case 1: Valid workflow ---
cat <<EOF > test_workflows/valid_workflow.yml
name: Valid Workflow

on: push

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run a one-line script
        run: echo Hello, world!
EOF

# --- Test Case 2: Invalid workflow (missing job name) ---
cat <<EOF > test_workflows/invalid_workflow_missing_job.yml
name: Invalid Workflow (Missing Job)

on: push

jobs:
  # Missing job name here
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
EOF

# --- Test Case 3: Invalid workflow (incorrect syntax) ---
cat <<EOF > test_workflows/invalid_workflow_syntax.yml
name: Invalid Workflow (Syntax Error)

on: push

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        invalid_key: some_value # Syntax error
EOF

echo "Running tests..."

# Test 1: Valid workflow should pass
echo "Testing with a valid workflow..."
if docker-compose run --rm lint-runner '**/.github/workflows/valid_workflow.yml'; then
  echo "Test 1 Passed: Valid workflow linted successfully."
else
  echo "Test 1 Failed: Valid workflow should not have failed."
  exit 1
fi

# Test 2: Invalid workflow (missing job name) should fail
echo "Testing with an invalid workflow (missing job name)..."
if ! docker-compose run --rm lint-runner '**/.github/workflows/invalid_workflow_missing_job.yml'; then
  echo "Test 2 Passed: Invalid workflow (missing job name) failed as expected."
else
  echo "Test 2 Failed: Invalid workflow (missing job name) should have failed."
  exit 1
fi

# Test 3: Invalid workflow (syntax error) should fail
echo "Testing with an invalid workflow (syntax error)..."
if ! docker-compose run --rm lint-runner '**/.github/workflows/invalid_workflow_syntax.yml'; then
  echo "Test 3 Passed: Invalid workflow (syntax error) failed as expected."
else
  echo "Test 3 Failed: Invalid workflow (syntax error) should have failed."
  exit 1
fi

# Test 4: Non-existent path should pass (no files to lint)
echo "Testing with a non-existent path..."
if docker-compose run --rm lint-runner 'non-existent-path/*.yml'; then
  echo "Test 4 Passed: Non-existent path handled gracefully."
else
  echo "Test 4 Failed: Non-existent path should not have failed."
  exit 1
fi

echo "All tests completed successfully!"

# Clean up test workflows
rm -rf test_workflows
