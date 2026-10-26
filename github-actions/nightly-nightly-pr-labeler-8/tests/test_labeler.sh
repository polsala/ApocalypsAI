#!/usr/bin/env bash
set -euo pipefail

# Helper to run labeler and capture output
run_labeler() {
  local title="$1"
  INPUT_TITLE="$title" ./src/labeler.sh >output.txt 2>&1
  cat output.txt
}

# Test cases: title => expected label (empty string means no label)
declare -A cases=(
  ["Fix crash on startup"]="bug"
  ["Add new authentication feature"]="enhancement"
  ["Update docs for API"]="documentation"
  ["Refactor test suite"]="tests"
  ["Minor typo"]=""
)

passed=0
failed=0

for title in "${!cases[@]}"; do
  expected="${cases[$title]}"
  result=$(run_labeler "$title")
  if [[ -z "$expected" ]]; then
    if [[ "$result" == *"No matching labels found"* ]]; then
      ((passed++))
    else
      echo "FAIL: '$title' expected no labels, got '$result'"
      ((failed++))
    fi
  else
    if [[ "$result" == *"$expected"* ]]; then
      ((passed++))
    else
      echo "FAIL: '$title' expected '$expected', got '$result'"
      ((failed++))
    fi
  fi
done

echo "Tests passed: $passed"
echo "Tests failed: $failed"
exit $failed
