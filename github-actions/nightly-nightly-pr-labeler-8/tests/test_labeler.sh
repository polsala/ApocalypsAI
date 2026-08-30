#!/usr/bin/env bash
set -euo pipefail

run_test() {
  local title="$1"
  local expected="$2"
  output=$(PR_TITLE="$title" bash src/labeler.sh)
  if [[ "$output" == "$expected" ]]; then
    echo "PASS: $title"
  else
    echo "FAIL: $title"
    echo "Expected: $expected"
    echo "Got: $output"
    exit 1
  fi
}

# Test cases
run_test "Fix bug in parser" "Adding label: bug"
run_test "Add new feature for API" "Adding label: enhancement"
run_test "Update docs for endpoint" "Adding label: documentation"
run_test "Refactor code" "No matching labels for title: Refactor code"

echo "All tests passed."
