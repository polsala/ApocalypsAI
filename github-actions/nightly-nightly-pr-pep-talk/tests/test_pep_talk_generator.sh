#!/bin/bash

# Mock rationale: We are testing the logic of the script itself,
# not its interaction with the GitHub API or the actual system date.
# By passing fixed dates, we ensure deterministic test results.

# Source the script to be tested
SCRIPT_TO_TEST="$(dirname "$0")"/../src/pep_talk_generator.sh

# Helper function to run the script and capture output
run_test() {
  local pr_updated_at=$1
  local inactivity_days=$2
  local comment_prefix=$3
  local current_date=$4
  bash "$SCRIPT_TO_TEST" "$pr_updated_at" "$inactivity_days" "$comment_prefix" "$current_date"
}

# Test Case 1: PR is active (updated recently)
echo "--- Test Case 1: PR is active ---"
OUTPUT=$(run_test "2023-10-26T10:00:00Z" "7" "Test Prefix:" "2023-10-27T10:00:00Z")
if echo "$OUTPUT" | grep -q "should_comment=false"; then
  echo "PASS: PR active, no comment."
else
  echo "FAIL: PR active, comment generated unexpectedly."
  echo "Output: $OUTPUT"
  exit 1
fi

# Test Case 2: PR is inactive (older than inactivity days)
echo "--- Test Case 2: PR is inactive ---"
OUTPUT=$(run_test "2023-10-19T10:00:00Z" "7" "Test Prefix:" "2023-10-27T10:00:00Z") # 8 days difference
if echo "$OUTPUT" | grep -q "should_comment=true" && echo "$OUTPUT" | grep -q "comment_body=Test Prefix:"; then
  echo "PASS: PR inactive, comment generated."
else
  echo "FAIL: PR inactive, no comment or incorrect prefix."
  echo "Output: $OUTPUT"
  exit 1
fi

# Test Case 3: PR is exactly on the inactivity threshold
echo "--- Test Case 3: PR is exactly on threshold ---"
OUTPUT=$(run_test "2023-10-20T10:00:00Z" "7" "Test Prefix:" "2023-10-27T10:00:00Z") # 7 days difference
if echo "$OUTPUT" | grep -q "should_comment=true" && echo "$OUTPUT" | grep -q "comment_body=Test Prefix:"; then
  echo "PASS: PR exactly on threshold, comment generated."
else
  echo "FAIL: PR exactly on threshold, no comment or incorrect prefix."
  echo "Output: $OUTPUT"
  exit 1
fi

# Test Case 4: Inactivity days set to 0 (always active unless updated in future)
echo "--- Test Case 4: Inactivity days 0 ---"
OUTPUT=$(run_test "2023-10-26T10:00:00Z" "0" "Test Prefix:" "2023-10-27T10:00:00Z") # 1 day diff >= 0 days
if echo "$OUTPUT" | grep -q "should_comment=true"; then
  echo "PASS: Inactivity 0, comment generated."
else
  echo "FAIL: Inactivity 0, no comment."
  echo "Output: $OUTPUT"
  exit 1
fi

# Test Case 5: Different prefix
echo "--- Test Case 5: Different prefix ---"
OUTPUT=$(run_test "2023-10-20T10:00:00Z" "7" "Another Prefix:" "2023-10-27T10:00:00Z")
if echo "$OUTPUT" | grep -q "should_comment=true" && echo "$OUTPUT" | grep -q "comment_body=Another Prefix:"; then
  echo "PASS: Different prefix, comment generated with correct prefix."
else
  echo "FAIL: Different prefix, no comment or incorrect prefix."
  echo "Output: $OUTPUT"
  exit 1
fi

echo "All tests completed successfully."
