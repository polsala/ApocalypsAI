#!/usr/bin/env bash
set -euo pipefail

# Create a temporary file to mock GITHUB_OUTPUT
OUTPUT_FILE=$(mktemp)
export GITHUB_OUTPUT="$OUTPUT_FILE"

run_test() {
  local title="$1"
  local expected="$2"
  PR_TITLE="$title" ./src/labeler.sh
  result=$(grep '^labels=' "$OUTPUT_FILE" | cut -d'=' -f2)
  if [[ "$result" == "$expected" ]]; then
    echo "PASS: '$title' -> '$expected'"
  else
    echo "FAIL: '$title' expected '$expected' got '$result'"
    exit 1
  fi
  # Reset mock output file for next case
  > "$OUTPUT_FILE"
}

run_test "[bug] Fix crash" "bug"
run_test "[feature] Add new API" "enhancement"
run_test "Refactor code" ""
run_test "[bug][feature] Mixed" "bug,enhancement"

echo "All tests passed."
