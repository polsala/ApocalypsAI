#!/bin/bash

set -euo pipefail

# Mock rationale: We are testing the core logic of the report generation script
# by simulating different repository states (presence/absence of files/directories)
# in a temporary directory. This allows for deterministic and offline testing
# without needing a real GitHub repository or API calls.

TEST_DIR=$(mktemp -d -t readiness-report-XXXXXX)
SCRIPT_PATH="$(dirname "$0")"/../src/generate_report.sh

cleanup() {
  rm -rf "$TEST_DIR"
}
trap cleanup EXIT

run_test() {
  local test_name="$1"
  local report_level="$2"
  local expected_score_regex="$3"
  local expected_status_regex="$4"
  shift 4
  local files_to_create=("$@")

  echo "--- Running test: $test_name (Level: $report_level) ---"

  # Clean up previous test environment
  rm -rf "$TEST_DIR"/*
  mkdir -p "$TEST_DIR"
  cd "$TEST_DIR"

  # Create specified files/directories
  for item in "${files_to_create[@]}"; do
    if [[ "$item" == *'/' ]]; then # It's a directory
      mkdir -p "$item"
    else # It's a file
      touch "$item"
    fi
  done

  # Run the script with the specified report level
  REPORT_LEVEL="$report_level" REPORT_OUTPUT=$(bash "$SCRIPT_PATH")

  # Assertions
  if echo "$REPORT_OUTPUT" | grep -Eq "$expected_score_regex"; then
    echo "✅ Score regex '$expected_score_regex' found."
  else
    echo "❌ Score regex '$expected_score_regex' NOT found."
    echo "Actual output:\n$REPORT_OUTPUT"
    exit 1
  fi

  if echo "$REPORT_OUTPUT" | grep -Eq "$expected_status_regex"; then
    echo "✅ Status regex '$expected_status_regex' found."
  else
    echo "❌ Status regex '$expected_status_regex' NOT found."
    echo "Actual output:\n$REPORT_OUTPUT"
    exit 1
  fi

  echo "--- Test '$test_name' PASSED ---"
  echo ""
}

# Test Case 1: Basic level, all files present
run_test "Basic - All Present" "basic" "Overall Readiness Score: 2/2" "Fully Prepared" \
  "README.md" "LICENSE"

# Test Case 2: Basic level, missing README
run_test "Basic - Missing README" "basic" "Overall Readiness Score: 1/2" "Significant Gaps Detected" \
  "LICENSE"

# Test Case 3: Standard level, all files present
run_test "Standard - All Present" "standard" "Overall Readiness Score: 5/5" "Fully Prepared" \
  "README.md" "LICENSE" "CONTRIBUTING.md" "SECURITY.md" "CODE_OF_CONDUCT.md"

# Test Case 4: Standard level, some missing
run_test "Standard - Some Missing" "standard" "Overall Readiness Score: 3/5" "Some Preparations Made" \
  "README.md" "LICENSE" "CONTRIBUTING.md"

# Test Case 5: Full level, all files present
run_test "Full - All Present" "full" "Overall Readiness Score: 9/9" "Fully Prepared" \
  "README.md" "LICENSE" "CONTRIBUTING.md" "SECURITY.md" "CODE_OF_CONDUCT.md" \
  ".github/workflows/" ".github/ISSUE_TEMPLATE/" ".github/PULL_REQUEST_TEMPLATE/" "CHANGELOG.md"

# Test Case 6: Full level, many missing
run_test "Full - Many Missing" "full" "Overall Readiness Score: 2/9" "Significant Gaps Detected" \
  "README.md" "LICENSE"

# Test Case 7: Full level, mostly present
run_test "Full - Mostly Present" "full" "Overall Readiness Score: 7/9" "Mostly Ready" \
  "README.md" "LICENSE" "CONTRIBUTING.md" "SECURITY.md" "CODE_OF_CONDUCT.md" \
  ".github/workflows/" ".github/ISSUE_TEMPLATE/"

echo "All tests passed successfully!"
