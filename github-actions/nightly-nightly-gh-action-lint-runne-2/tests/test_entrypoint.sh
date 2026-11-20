#!/bin/sh

# Mocking the GitHub Actions environment variables
export INPUT_WORKFLOWS_PATH="test_workflows"
export INPUT_FAIL_ON_WARNINGS="false"

# Mocking the actionlint command to simulate success and failure scenarios
# We'll create dummy files and directories for the test.

# Create a dummy workflows directory and a valid workflow file
mkdir -p test_workflows
cat <<EOF > test_workflows/valid_workflow.yml
name: Test Workflow

on: push

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
EOF

# Create a dummy invalid workflow file
cat <<EOF > test_workflows/invalid_workflow.yml
name: Invalid Workflow

on: push

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          invalid-param: 'some-value'
EOF

# Mock the actionlint executable to control its behavior
# This mock will simulate a successful run for valid files and a failure for invalid ones.
cat <<EOF > /usr/local/bin/actionlint
#!/bin/sh

# Simulate actionlint behavior based on arguments
if echo "$@" | grep -q "--fail-on-warnings"; then
  if echo "$@" | grep -q "invalid_workflow.yml"; then
    echo "Simulating failure with warnings enabled."
    exit 1 # Simulate failure
  else
    echo "Simulating success with warnings enabled."
    exit 0 # Simulate success
  fi
else
  if echo "$@" | grep -q "invalid_workflow.yml"; then
    echo "Simulating failure without warnings enabled."
    exit 1 # Simulate failure
  else
    echo "Simulating success without warnings enabled."
    exit 0 # Simulate success
  fi
fi
EOF
chmod +x /usr/local/bin/actionlint

# --- Test Case 1: Successful linting with default settings ---
echo "--- Running Test Case 1: Successful linting (default settings) ---"
if sh src/entrypoint.sh; then
  echo "Test Case 1 PASSED: Linting succeeded as expected."
else
  echo "Test Case 1 FAILED: Linting failed unexpectedly."
  exit 1
fi

# --- Test Case 2: Failing linting with fail_on_warnings enabled ---
export INPUT_FAIL_ON_WARNINGS="true"
echo "\n--- Running Test Case 2: Failing linting (fail_on_warnings enabled) ---"
if sh src/entrypoint.sh; then
  echo "Test Case 2 FAILED: Linting should have failed."
  exit 1
else
  echo "Test Case 2 PASSED: Linting failed as expected."
fi

# --- Test Case 3: Linting with a custom path ---
export INPUT_WORKFLOWS_PATH="custom_workflows"
export INPUT_FAIL_ON_WARNINGS="false"

# Create a custom workflows directory and a valid workflow file
mkdir -p custom_workflows
cat <<EOF > custom_workflows/another_valid_workflow.yml
name: Another Workflow

on: pull_request

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
EOF

# Mock actionlint to only succeed for the custom path
cat <<EOF > /usr/local/bin/actionlint
#!/bin/sh

if echo "$@" | grep -q "custom_workflows"; then
  echo "Simulating success for custom path."
  exit 0
else
  echo "Simulating failure for other paths."
  exit 1
fi
EOF
chmod +x /usr/local/bin/actionlint

echo "\n--- Running Test Case 3: Linting with custom path ---"
if sh src/entrypoint.sh; then
  echo "Test Case 3 PASSED: Linting with custom path succeeded as expected."
else
  echo "Test Case 3 FAILED: Linting with custom path failed unexpectedly."
  exit 1
fi

# Clean up mocks and dummy files
rm -rf test_workflows custom_workflows /usr/local/bin/actionlint

echo "\nAll tests completed."
exit 0
