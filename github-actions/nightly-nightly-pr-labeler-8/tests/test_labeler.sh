#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: The tests invoke the labeler script with fabricated environment variables
# and verify that the expected label string appears in the output.

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)
LABELER="$SCRIPT_DIR/labeler.sh"

run_test() {
  local title="$1"
  local expected_label="$2"
  export PR_NUMBER=123
  export REPO="owner/repo"
  export GITHUB_TOKEN="dummy"
  export PR_TITLE="$title"

  output=$(bash "$LABELER")
  if [[ "$output" == *"label '${expected_label}'"* ]]; then
    echo "PASS: '$title' => $expected_label"
  else
    echo "FAIL: '$title' expected $expected_label but got: $output"
    exit 1
  fi
}

# Test cases
run_test "Fix critical bug in parser" "bug"
run_test "Add new feature for user profiles" "enhancement"
run_test "Update docs for installation" "documentation"
run_test "Refactor codebase" "needs-triage"

echo "All tests passed."
