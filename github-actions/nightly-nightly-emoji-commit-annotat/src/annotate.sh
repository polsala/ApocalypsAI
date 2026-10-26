#!/usr/bin/env bash
set -e

# Retrieve the commit message passed as the first argument
message="$1"

# Define a static list of emojis
emojis=("🚀" "✨" "🔥" "💡" "🎉")

# Determine which emoji to use
if [[ -n "$SEED" ]]; then
  idx=$(( SEED % ${#emojis[@]} ))
else
  idx=$(( $(date +%s) % ${#emojis[@]} ))
fi
emoji="${emojis[$idx]}"

# Emit the output in the format expected by GitHub Actions composite actions
# GITHUB_OUTPUT is automatically provided by the runner
if [[ -z "$GITHUB_OUTPUT" ]]; then
  echo "::error::GITHUB_OUTPUT not set."
  exit 1
fi

echo "annotated_message=${emoji} ${message}" >> "$GITHUB_OUTPUT"
