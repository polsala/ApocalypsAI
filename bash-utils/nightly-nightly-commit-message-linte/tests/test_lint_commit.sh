#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
LINTER="$SCRIPT_DIR/lint_commit.sh"

run_test() {
  local name="$1"
  local input="$2"
  local expect_exit="$3"
  echo "Running $name..."
  tmp=$(mktemp)
  echo -e "$input" > "$tmp"
  if "$LINTER" "$tmp"; then
    exit_code=0
  else
    exit_code=$?
  fi
  rm -f "$tmp"
  if [[ $exit_code -eq $expect_exit ]]; then
    echo "PASS $name"
  else
    echo "FAIL $name: expected $expect_exit got $exit_code"
    exit 1
  fi
}

# Test 1: valid commit message
run_test "valid" "Add new feature\n\nImplemented the new feature as described." 0

# Test 2: subject too long
run_test "subject-too-long" "$(printf 'A%.0s' {1..51})\n\nBody line." 1

# Test 3: subject not capitalized
run_test "subject-not-capital" "add something\n\nBody." 1

# Test 4: subject ends with period
run_test "subject-period" "Fix bug.\n\nDetails." 1

# Test 5: body line too long
run_test "body-too-long" "Fix bug\n\n$(printf 'B%.0s' {1..73})" 1

# Test 6: trailing whitespace in body
run_test "trailing-ws" "Fix bug\n\nLine with space " 1

echo "All tests passed."
