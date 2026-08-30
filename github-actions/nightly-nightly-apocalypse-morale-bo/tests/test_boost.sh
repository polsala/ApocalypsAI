#!/usr/bin/env bash
set -e

# Mock GITHUB_OUTPUT to capture the output of the action script
TMP_OUTPUT=$(mktemp)
export GITHUB_OUTPUT="$TMP_OUTPUT"

# Run the boost script
bash "$(dirname "$0")/../src/boost.sh"

# Source the captured output to load the 'message' variable
source "$TMP_OUTPUT"

if [[ -z "$message" ]]; then
  echo "FAIL: No message output"
  exit 1
fi

# Expected messages list (must match the list in boost.sh)
expected=(
  "Keep calm and hoard the canned beans."
  "When in doubt, build a bunker."
  "Radiation? Just a warm hug from the universe."
  "Remember: every night ends with sunrise, even in the wasteland."
  "Scavenge today, survive tomorrow."
)

found=0
for e in "${expected[@]}"; do
  if [[ "$message" == "$e" ]]; then
    found=1
    break
  fi
done

if [[ $found -eq 1 ]]; then
  echo "PASS"
else
  echo "FAIL: Unexpected message: $message"
  exit 1
fi
