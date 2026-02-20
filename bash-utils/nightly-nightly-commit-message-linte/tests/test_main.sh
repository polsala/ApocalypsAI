#!/usr/bin/env bash
set -euo pipefail
SCRIPT="../src/main.sh"

run_test() {
  local name="$1"
  local input="$2"
  local expect_exit="$3"
  echo "$input" > /tmp/commit_msg.txt
  if "$SCRIPT" /tmp/commit_msg.txt; then
    status=0
  else
    status=$?
  fi
  if [[ "$status" -eq "$expect_exit" ]]; then
    echo "PASS: $name"
  else
    echo "FAIL: $name (expected $expect_exit, got $status)"
    exit 1
  fi
}

# Valid commit (should pass)
run_test "valid commit" "Add new feature X\n\nImplemented the new feature.\nFixes #123" 0

# Subject too long (should fail)
run_test "subject too long" "This subject line is definitely way longer than fifty characters allowed\n\nFixes #124" 1

# Subject not capitalized (should fail)
run_test "subject not capitalized" "add new feature Y\n\nFixes #125" 1

# Body line too long (should fail)
run_test "body line too long" "Add feature Z\n\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\nFixes #126" 1

# Missing issue reference (should fail)
run_test "missing issue reference" "Add feature W\n\nImplemented correctly." 1

echo "All tests passed"
