#!/usr/bin/env bash

messages=(
  "Keep calm and hoard the canned beans."
  "When in doubt, build a bunker."
  "Radiation? Just a warm hug from the universe."
  "Remember: every night ends with sunrise, even in the wasteland."
  "Scavenge today, survive tomorrow."
)

# Pick a random message
msg="${messages[RANDOM % ${#messages[@]}]}"

# Export as action output (GitHub >= 2022)
# Mock rationale: using GITHUB_OUTPUT env var to communicate output
if [[ -z "$GITHUB_OUTPUT" ]]; then
  echo "::error::GITHUB_OUTPUT not set"
  exit 1
fi
echo "message=$msg" >> "$GITHUB_OUTPUT"
