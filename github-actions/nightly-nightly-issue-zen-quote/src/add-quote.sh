#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: This script selects a random Zen quote and posts it as a comment on the issue that triggered the workflow.

# Load event payload
EVENT_PATH="${GITHUB_EVENT_PATH:-}"
if [[ -z "$EVENT_PATH" || ! -f "$EVENT_PATH" ]]; then
  echo "Error: GITHUB_EVENT_PATH not set or file does not exist"
  exit 1
fi

# Extract repository and issue number using jq (fallback to pure bash if jq missing)
if command -v jq >/dev/null 2>&1; then
  REPO="$(jq -r .repository.full_name "$EVENT_PATH")"
  ISSUE_NUMBER="$(jq -r .issue.number "$EVENT_PATH")"
else
  # Simple parsing assuming known format
  REPO="$(grep -oP '(?<=\"full_name\": \\")[^\"]+' "$EVENT_PATH")"
  ISSUE_NUMBER="$(grep -oP '(?<=\"number\": )[0-9]+' "$EVENT_PATH")"
fi

if [[ -z "$REPO" || -z "$ISSUE_NUMBER" ]]; then
  echo "Error: Could not determine repository or issue number"
  exit 1
fi

# List of Zen quotes
QUOTES=(
  "The journey of a thousand miles begins with one step."
  "When the mind is still, the universe surrenders."
  "Simplicity is the ultimate sophistication."
  "Let go or be dragged."
  "The obstacle is the path."
)

# Pick a random quote
RANDOM_INDEX=$((RANDOM % ${#QUOTES[@]}))
SELECTED_QUOTE="${QUOTES[$RANDOM_INDEX]}"

# Prepare payload
PAYLOAD=$(printf '{"body":"%s"}' "$SELECTED_QUOTE")

# Determine curl command (allow override for testing)
CURL_CMD="${CURL_CMD:-curl}"

# Post comment
"$CURL_CMD" -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d "$PAYLOAD" \
  "https://api.github.com/repos/$REPO/issues/$ISSUE_NUMBER/comments"
