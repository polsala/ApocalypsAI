#!/bin/bash

# Mock rationale: GitHub Actions environment variables are mocked by setting them directly
# before executing the script. This allows for deterministic, offline testing.
# The '::set-output' and '::error' commands are GitHub Actions specific syntax.
# For offline testing, we verify that the script *would* output these strings to stdout/stderr,
# rather than actually setting an output or failing a real GitHub Action run.

SCRIPT_PATH="$(dirname "$0")"/../src/check_affirmation.sh

# Function to run the script with mocked environment and capture output/exit code
run_test() {
  local pr_desc="$1"
  local req_phrases="$2"
  local expected_exit_code="$3"
  local expected_output_contains="$4"
  local test_name="$5"

  echo "--- $test_name ---"
  
  # Clear previous output files
  rm -f test_output.txt test_error.txt

  # Run the script with mocked environment variables, capturing stdout and stderr
  PR_DESCRIPTION="$pr_desc" REQUIRED_PHRASES="$req_phrases" bash "$SCRIPT_PATH" > test_output.txt 2> test_error.txt
  local actual_exit_code=$?

  local output_content=$(cat test_output.txt)
  local error_content=$(cat test_error.txt)

  local pass=true

  # Check exit code
  if [ "$actual_exit_code" -ne "$expected_exit_code" ]; then
    echo "FAIL: Unexpected exit code. Expected $expected_exit_code, got $actual_exit_code."
    pass=false
  fi

  # Check if stdout contains the expected output string (e.g., ::set-output)
  if ! echo "$output_content" | grep -q "$expected_output_contains"; then
    echo "FAIL: Stdout did not contain expected string: '$expected_output_contains'."
    echo "Actual stdout:"
    echo "$output_content"
    pass=false
  fi

  # If expecting a failure (non-zero exit code), check for ::error in stderr
  if [ "$expected_exit_code" -ne 0 ] && ! echo "$error_content" | grep -q "::error"; then
    echo "FAIL: Expected '::error' message not found in stderr."
    echo "Actual stderr:"
    echo "$error_content"
    pass=false
  fi

  if $pass; then
    echo "PASS"
  else
    echo "FAIL"
    exit 1 # Exit on first failure to prevent cascading errors
  fi
}

# Test Case 1: Description contains a default required phrase (should pass)
run_test \
  "This is a PR. Whimsical Affirmation: You are resilient!" \
  "Whimsical Affirmation:,Survival Tip:" \
  0 \
  "::set-output name=affirmation-found::true" \
  "Test Case 1: Description contains 'Whimsical Affirmation:'"

# Test Case 2: Description contains another default required phrase (should pass)
run_test \
  "Fixing a bug. Survival Tip: Always carry a towel." \
  "Whimsical Affirmation:,Survival Tip:" \
  0 \
  "::set-output name=affirmation-found::true" \
  "Test Case 2: Description contains 'Survival Tip:'"

# Test Case 3: Description does NOT contain any default required phrase (should fail)
run_test \
  "Just a regular PR." \
  "Whimsical Affirmation:,Survival Tip:" \
  1 \
  "::set-output name=affirmation-found::false" \
  "Test Case 3: Description without required phrase"

# Test Case 4: Custom required phrases, one found (should pass)
run_test \
  "Adding new feature. Apocalyptic Insight: The squirrels are watching." \
  "Apocalyptic Insight:,Zen Moment:" \
  0 \
  "::set-output name=affirmation-found::true" \
  "Test Case 4: Custom phrases, one found"

# Test Case 5: Custom required phrases, none found (should fail)
run_test \
  "Another feature." \
  "Apocalyptic Insight:,Zen Moment:" \
  1 \
  "::set-output name=affirmation-found::false" \
  "Test Case 5: Custom phrases, none found"

echo "All tests completed successfully."
