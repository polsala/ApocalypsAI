#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: read issue title from event JSON
EVENT_PATH="${GITHUB_EVENT_PATH:-}"
if [[ -z "$EVENT_PATH" ]]; then
  echo "::error::GITHUB_EVENT_PATH not set"
  exit 1
fi

TITLE=$(jq -r .issue.title "$EVENT_PATH")
ISSUE_NUMBER=$(jq -r .issue.number "$EVENT_PATH")
REPO=$(jq -r .repository.full_name "$EVENT_PATH")

# Simple keyword detection
KEYWORD=""
if [[ "$TITLE" =~ [Bb]ug ]]; then
  KEYWORD="bug"
elif [[ "$TITLE" =~ [Ff]eature ]]; then
  KEYWORD="feature"
fi

FORTUNES=(
  "The stars align for your $KEYWORD. Great things await!"
  "Beware the $KEYWORD, but also embrace its potential."
  "A surprise $KEYWORD will change your path."
  "Your $KEYWORD journey is just beginning."
  "Fortune favors the bold $KEYWORD."
)

# Choose random
RANDOM_INDEX=$((RANDOM % ${#FORTUNES[@]}))
MESSAGE="${FORTUNES[$RANDOM_INDEX]}"

# Post comment via GitHub API
API_URL="https://api.github.com/repos/$REPO/issues/$ISSUE_NUMBER/comments"
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github.v3+json" \
  -d "$(printf '{\"body\": \"%s\"}' \"$MESSAGE\")" "$API_URL" > /dev/null

echo "Posted fortune comment."
