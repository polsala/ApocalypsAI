#!/bin/bash

set -euo pipefail

# Mocking yq command
# Mock rationale: The 'yq' command is an external dependency that is not easily available in all test environments. 
# We mock it here to simulate its behavior for syntax checking.
yq() {
  local cmd="$1"
  local file="$2"

  if [[ "$cmd" == "eval" && "$file" == "invalid.yml" ]]; then
    return 1 # Simulate syntax error
  elif [[ "$cmd" == "eval" && "$file" == "valid.yml" ]]; then
    return 0 # Simulate valid syntax
  elif [[ "$cmd" == "eval" && "$file" == "valid_no_on.yml" ]]; then
    return 0 # Simulate valid syntax but missing 'on:'
  elif [[ "$cmd" == "eval" && "$file" == "valid_no_version.yml" ]]; then
    return 0 # Simulate valid syntax with potential missing version
  elif [[ "$cmd" == "eval" && "$file" == "valid_with_secrets.yml" ]]; then
    return 0 # Simulate valid syntax with secrets usage
  fi
  echo "Mocked yq: $cmd $file" # Fallback for unexpected calls
  return 0
}

# Source the script to be tested
source src/main.sh

# --- Test Cases ---

# Test 1: Valid workflow file
log_info "Running Test 1: Valid workflow file"
mkdir -p .github/workflows
echo "name: My Test Workflow\non: push\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - name: Checkout\n        uses: actions/checkout@v3"
  > .github/workflows/valid.yml

if ./src/main.sh; then
  log_info "Test 1 Passed: Valid workflow linted successfully."
else
  log_error "Test 1 Failed: Valid workflow caused an error."
  exit 1
fi
rm -rf .github

# Test 2: Invalid YAML syntax
log_info "Running Test 2: Invalid YAML syntax"
mkdir -p .github/workflows
echo "name: Invalid Workflow\n  invalid indentation: true"
  > .github/workflows/invalid.yml

if ./src/main.sh 2>&1 | grep -q "Invalid YAML syntax"; then
  log_info "Test 2 Passed: Invalid YAML detected."
else
  log_error "Test 2 Failed: Invalid YAML not detected."
  exit 1
fi
rm -rf .github

# Test 3: Missing 'name:' at top level
log_info "Running Test 3: Missing 'name:'"
mkdir -p .github/workflows
echo "on: push\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - name: Checkout\n        uses: actions/checkout@v3"
  > .github/workflows/missing_name.yml

if ./src/main.sh 2>&1 | grep -q "Missing 'name:' at the top level"; then
  log_info "Test 3 Passed: Missing 'name:' detected."
else
  log_error "Test 3 Failed: Missing 'name:' not detected."
  exit 1
fi
rm -rf .github

# Test 4: Missing 'on:' trigger
log_info "Running Test 4: Missing 'on:'"
mkdir -p .github/workflows
echo "name: Workflow without trigger\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - name: Checkout\n        uses: actions/checkout@v3"
  > .github/workflows/valid_no_on.yml

if ./src/main.sh 2>&1 | grep -q "Missing 'on:' trigger"; then
  log_info "Test 4 Passed: Missing 'on:' detected."
else
  log_error "Test 4 Failed: Missing 'on:' not detected."
  exit 1
fi
rm -rf .github

# Test 5: Potential missing version tag (heuristic)
log_info "Running Test 5: Potential missing version tag"
mkdir -p .github/workflows
echo "name: Workflow with potential missing version\non: push\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - name: Checkout\n        uses: actions/checkout"
  > .github/workflows/valid_no_version.yml

if ./src/main.sh 2>&1 | grep -q "Potential missing version tag"; then
  log_info "Test 5 Passed: Potential missing version tag detected."
else
  log_error "Test 5 Failed: Potential missing version tag not detected."
  exit 1
fi
rm -rf .github

# Test 6: Usage of 'secrets.' (warning)
log_info "Running Test 6: Usage of 'secrets.'"
mkdir -p .github/workflows
echo "name: Workflow with secrets\non: push\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - name: Use secret\n        run: echo ${{ secrets.MY_SECRET }}"
  > .github/workflows/valid_with_secrets.yml

if ./src/main.sh 2>&1 | grep -q "Found 'secrets.' usage"; then
  log_info "Test 6 Passed: 'secrets.' usage detected."
else
  log_error "Test 6 Failed: 'secrets.' usage not detected."
  exit 1
fi
rm -rf .github

# Test 7: Empty workflows directory
log_info "Running Test 7: Empty workflows directory"
rm -rf .github # Ensure it's empty

if ./src/main.sh 2>&1 | grep -q "No workflows directory found"; then
  log_info "Test 7 Passed: Empty workflows directory handled."
else
  log_error "Test 7 Failed: Empty workflows directory not handled."
  exit 1
fi

log_info "All tests completed."
exit 0
