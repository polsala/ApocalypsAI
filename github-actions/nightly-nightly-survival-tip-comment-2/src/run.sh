#!/usr/bin/env bash
set -e

# Array of whimsical survival tips
tips=(
  "Always keep a spare bottle of water."
  "Never trust a silent night."
  "Carry a flashlight, even in daylight."
  "Know your escape routes."
  "Mark your supplies with chalk."
)

# Determine index based on the workflow run number (default 0)
run_number=${GITHUB_RUN_NUMBER:-0}
count=${#tips[@]}
index=$(( run_number % count ))
selected="${tips[$index]}"

# Export the selected tip as an output for the composite action
# GitHub expects outputs to be written to the file path in $GITHUB_OUTPUT
if [[ -n "$GITHUB_OUTPUT" ]]; then
  echo "tip=$selected" >> "$GITHUB_OUTPUT"
else
  # Fallback for local testing
  echo "tip=$selected"
fi

# If a token is provided, post the tip as a comment on the PR
if [[ -n "$INPUT_TOKEN" ]]; then
  repo="$GITHUB_REPOSITORY"
  pr_number="$GITHUB_EVENT_PULL_REQUEST_NUMBER"
  if [[ -n "$repo" && -n "$pr_number" ]]; then
    comment_body="💡 Survival Tip: $selected"
    curl -s -X POST -H "Authorization: token $INPUT_TOKEN" \
      -H "Accept: application/vnd.github.v3+json" \
      "https://api.github.com/repos/$repo/issues/$pr_number/comments" \
      -d "{\"body\":\"$comment_body\"}"
  fi
fi
