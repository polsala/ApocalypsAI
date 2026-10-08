#!/bin/bash

# Mock rationale: This script directly tests the 'emojify.sh' logic
# by invoking it with various inputs and comparing its standard output.
# No external services or complex environment variables are involved,
# making direct execution a deterministic and offline test method.

SCRIPT_PATH="$(dirname "$0")"/../src/emojify.sh

# Function to run a test
run_test() {
  local status="$1"
  local expected_emojis="$2"
  local actual_emojis=$(bash "$SCRIPT_PATH" "$status")

  if [[ "$actual_emojis" == "$expected_emojis" ]]; then
    echo "✅ Test passed for status '$status'. Output: '$actual_emojis'"
  else
    echo "❌ Test failed for status '$status'."
    echo "   Expected: '$expected_emojis'"
    echo "   Actual:   '$actual_emojis'"
    exit 1
  fi
}

echo "Running tests for emojify.sh..."

run_test "success" "✨🚀🎉"
run_test "failure" "💥😭🔥"
run_test "cancelled" "💨👻🛑"
run_test "neutral" "☁️🤔⏳"
run_test "skipped" "⏭️😴💤"
run_test "timed_out" "⏳💀⏰"
run_test "action_required" "🚨👀❓"
run_test "unknown_status" "❓🌀🤷"
run_test "another_random_status" "❓🌀🤷"

echo "All tests completed."
