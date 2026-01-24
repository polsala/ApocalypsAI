#!/bin/bash

# Mock rationale: We override $RANDOM and environment variables to ensure deterministic behavior.

set -euo pipefail

SCRIPT="../src/chaos.sh"

# Test 1: No chaos when chance is 0
export CHAOS_CHANCE=0
output=$(env RANDOM=999 $SCRIPT 2>&1 || true)
if [[ -n "$output" ]]; then
  echo "FAIL: Expected no output when CHAOS_CHANCE=0"
  exit 1
else
  echo "PASS: No chaos when chance is 0"
fi

# Test 2: Typo mode
export CHAOS_MODE="typo"
output=$(env RANDOM=50 $SCRIPT 2>&1 || true)
if [[ "$output" != *"Oops! Did I type that right?"* ]]; then
  echo "FAIL: Typo mode failed"
  echo "Output: $output"
  exit 1
else
  echo "PASS: Typo mode works"
fi

# Test 3: Emoji mode
export CHAOS_MODE="emoji"
output=$(env RANDOM=100 $SCRIPT 2>&1 || true)
if [[ ! "$output" =~ (👾|🤪|👻|👽|🤖|⚡|💥) ]]; then
  echo "FAIL: Emoji mode failed"
  echo "Output: $output"
  exit 1
else
  echo "PASS: Emoji mode works"
fi

# Test 4: Delay mode
export CHAOS_MODE="delay"
start=$(date +%s)
env RANDOM=200 $SCRIPT > /dev/null 2>&1 || true
end=$(date +%s)
diff=$((end - start))
if (( diff < 1 || diff > 4 )); then
  echo "FAIL: Delay mode failed (took ${diff}s)"
  exit 1
else
  echo "PASS: Delay mode works"
fi

# Test 5: Random mode (mock to fixed outcome)
export CHAOS_MODE="random"
output=$(env RANDOM=1 $SCRIPT 2>&1 || true)
if [[ ! "$output" =~ (Oops|Chaos|🐌) ]]; then
  echo "FAIL: Random mode failed"
  echo "Output: $output"
  exit 1
else
  echo "PASS: Random mode works"
fi

echo "All tests passed! 🎉"
