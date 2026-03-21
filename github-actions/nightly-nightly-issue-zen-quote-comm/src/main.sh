#!/usr/bin/env bash
set -euo pipefail

# Load event payload
EVENT_PATH="${GITHUB_EVENT_PATH:-}"
if [[ -z "$EVENT_PATH" ]]; then
  echo "GITHUB_EVENT_PATH not set"
  exit 1
fi

# Extract issue number and repository information
ISSUE_NUMBER=$(jq -r .issue.number "$EVENT_PATH")
REPO="${GITHUB_REPOSITORY}"
TOKEN="${GITHUB_TOKEN}"

if [[ -z "$ISSUE_NUMBER" || "$ISSUE_NUMBER" == "null" ]]; then
  echo "No issue number found in event – nothing to do"
  exit 0
fi

# Array of zen quotes
QUOTES=(
  "The journey of a thousand miles begins with one step."
  "Simplicity is the ultimate sophistication."
  "When the mind is still, the universe surrenders."
  "Let go or be dragged."
  "The obstacle is the path."
)

# Pick a random quote (deterministic when RANDOM is preset)
RANDOM_INDEX=$((RANDOM % ${#QUOTES[@]}))
SELECTED="${QUOTES[$RANDOM_INDEX]}"

# Prepare API request
API_URL="https://api.github.com/repos/$REPO/issues/$ISSUE_NUMBER/comments"
PAYLOAD=$(jq -n --arg body "$SELECTED" '{body: $body}')

# Post comment via curl
curl -s -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d "$PAYLOAD" \
  "$API_URL"

exit 0
