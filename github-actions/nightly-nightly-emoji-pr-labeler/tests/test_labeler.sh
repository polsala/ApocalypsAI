#!/usr/bin/env bash
set -e

# Helper to run a single test case
run_test() {
  local title="$1"
  local expected="$2"
  # Capture the script output
  output=$(bash src/labeler.sh "$title")
  # Extract the value after the ::set-output marker
  actual=$(echo "$output" | sed -n 's/.*::set-output name=labels:://p')
  if [[ "$actual" == "$expected" ]]; then
    echo "PASS: \"$title\" => $actual"
  else
    echo "FAIL: \"$title\" => $actual (expected $expected)"
    exit 1
  fi
}

# Test cases
run_test "Fix bug 🐛" "bug"
run_test "Add shiny feature ✨ 🚀" "enhancement,feature"
run_test "Update docs 📚" "documentation"
run_test "Refactor code" ""

echo "All tests passed."
