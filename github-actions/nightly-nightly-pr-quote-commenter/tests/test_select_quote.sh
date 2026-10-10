#!/usr/bin/env bash
# Test that the select‑quote step outputs a line starting with "quote="
set -euo pipefail

# Use a known seed so the random choice is deterministic
RANDOM=42

# Capture the output of the step script
output=$(bash -c "
  mapfile -t quotes < \"$(pwd)/src/quotes.txt\"
  count=${#quotes[@]}
  idx=$((RANDOM % count))
  chosen=\"${quotes[$idx]}\"
  escaped=$(printf '%s' \"$chosen\" | sed 's/\"/\\\\\"/g')
  echo \"quote=$escaped\"")

# Verify the format
if [[ $output =~ ^quote=.+$ ]]; then
  echo "PASS: output format correct -> $output"
  exit 0
else
  echo "FAIL: unexpected output -> $output"
  exit 1
fi
