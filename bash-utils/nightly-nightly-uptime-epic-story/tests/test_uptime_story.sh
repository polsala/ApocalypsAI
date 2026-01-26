#!/usr/bin/env bash
set -e

# Determine script location relative to this test file
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)
SCRIPT="$SCRIPT_DIR/uptime_story.sh"

# Helper to run the script with given env vars and capture output
run_script() {
  UPTIME_MOCK="$1" STORY_INDEX="$2" "$SCRIPT"
}

# Test case 1: 90061 seconds -> 1 day, 1 hour, 1 minute (plus 1 second, ignored)
output=$(run_script "90061.00 0" 0)
expected="1 days, 1 hours, 1 minutes"
if [[ "$output" != *"$expected"* ]]; then
  echo "Test 1 failed: expected '$expected' in output"
  echo "Got: $output"
  exit 1
fi

# Test case 2: same uptime, different template (index 2)
output=$(run_script "90061.00 0" 2)
if [[ "$output" != *"$expected"* ]]; then
  echo "Test 2 failed: expected '$expected' in output with template index 2"
  echo "Got: $output"
  exit 1
fi

# Test case 3: zero uptime
output=$(run_script "0.00 0" 1)
expected="0 days, 0 hours, 0 minutes"
if [[ "$output" != *"$expected"* ]]; then
  echo "Test 3 failed: expected '$expected' for zero uptime"
  echo "Got: $output"
  exit 1
fi

echo "All tests passed"
