#!/bin/bash

# Setup: Create mock files and variables for testing
MOCK_PR_BODY_FILE_GOOD="tests/mock_pr_body_good.txt"
MOCK_PR_BODY_FILE_BAD="tests/mock_pr_body_bad.txt"
MOCK_PR_BODY_FILE_EMPTY="tests/mock_pr_body_empty.txt"
MOCK_PR_NUMBER="123"
MOCK_REPO_FULL_NAME="polsala/ApocalypsAI"
MOCK_GITHUB_TOKEN="ghp_mocktoken_for_testing"
MOCK_REQUIRED_PHRASE="Chronicle Entry:|Changelog:|Release Notes:"
MOCK_COMMENT_MESSAGE="Please add a chronicle entry."

mkdir -p tests

# Create mock PR body files
echo -e "This is a PR description.\n\n## Chronicle Entry\n- Added feature X." > "$MOCK_PR_BODY_FILE_GOOD"
echo -e "This is another PR description.\nIt has no special section." > "$MOCK_PR_BODY_FILE_BAD"
echo "" > "$MOCK_PR_BODY_FILE_EMPTY"

# Function to run a test case
run_test() {
  local test_name="$1"
  local pr_body_file="$2"
  local expected_exit_code="$3"
  local expected_output_contains="$4"
  local expected_gh_output_contains="$5"

  echo "--- Running Test: $test_name ---"
  
  # Clear previous GITHUB_OUTPUT file
  rm -f test_github_output.txt

  # Run the script with mock inputs, redirecting GITHUB_OUTPUT to a temporary file
  OUTPUT=$(GITHUB_OUTPUT="test_github_output.txt" bash src/check_chronicle_entry.sh \
    "$pr_body_file" \
    "$MOCK_PR_NUMBER" \
    "$MOCK_REPO_FULL_NAME" \
    "$MOCK_GITHUB_TOKEN" \
    "$MOCK_REQUIRED_PHRASE" \
    "$MOCK_COMMENT_MESSAGE")
  EXIT_CODE=$?

  local test_passed=true

  if [ "$EXIT_CODE" -ne "$expected_exit_code" ]; then
    echo "Test Failed: $test_name - Unexpected exit code. Expected $expected_exit_code, got $EXIT_CODE."
    test_passed=false
  fi

  if ! echo "$OUTPUT" | grep -qE "$expected_output_contains"; then
    echo "Test Failed: $test_name - Script output did not contain expected phrase: '$expected_output_contains'."
    echo "Actual output: $OUTPUT"
    test_passed=false
  fi

  if ! grep -qE "$expected_gh_output_contains" test_github_output.txt; then
    echo "Test Failed: $test_name - GITHUB_OUTPUT file did not contain expected phrase: '$expected_gh_output_contains'."
    echo "Actual GITHUB_OUTPUT: $(cat test_github_output.txt)"
    test_passed=false
  fi

  if $test_passed; then
    echo "Test Passed: $test_name."
  else
    echo "Test Failed: $test_name."
    rm -f test_github_output.txt
    exit 1
  fi
  rm -f test_github_output.txt
}

# Test 1: Chronicle Entry found
run_test \
  "Chronicle Entry found" \
  "$MOCK_PR_BODY_FILE_GOOD" \
  0 \
  "Chronicle Entry found. All clear!" \
  "chronicle_entry_found=true"

# Test 2: Chronicle Entry not found
run_test \
  "Chronicle Entry not found" \
  "$MOCK_PR_BODY_FILE_BAD" \
  1 \
  "Chronicle Entry not found. Reminding contributor..." \
  "chronicle_entry_found=false"

# Test 3: Empty PR body (should also not find entry)
run_test \
  "Empty PR body" \
  "$MOCK_PR_BODY_FILE_EMPTY" \
  1 \
  "Chronicle Entry not found. Reminding contributor..." \
  "chronicle_entry_found=false"

# Cleanup mock files
rm "$MOCK_PR_BODY_FILE_GOOD" "$MOCK_PR_BODY_FILE_BAD" "$MOCK_PR_BODY_FILE_EMPTY"
rmdir tests

echo "All tests passed for check_chronicle_entry.sh!"
exit 0
