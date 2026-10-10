#!/usr/bin/env bash
# Tests for emoji_annotator.sh – ensure correct emoji selection.

set -e

SCRIPT="../src/emoji_annotator.sh"

run_test() {
  local input="$1"
  local expected="$2"
  local output
  output=$(echo "$input" | bash "$SCRIPT")
  if [[ "$output" != "$expected" ]]; then
    echo "FAIL: input='$input' expected='$expected' got='$output'"
    exit 1
  fi
}

# Test cases
run_test "Fix the login bug" "Fix the login bug 🛠️"
run_test "Add new feature for dashboard" "Add new feature for dashboard 🚀"
run_test "Just a random note" "Just a random note 🙂"

echo "All tests passed."
