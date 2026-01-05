#!/bin/sh
set -e

# Inputs
CHANGED_FILES="${INPUT_CHANGED_FILES}"
TOKEN="${GITHUB_TOKEN}"
REPO="${GITHUB_REPOSITORY}"
PR_NUMBER="${GITHUB_EVENT_PULL_REQUEST_NUMBER}"

# Fallback for testing if PR number is not set
if [ -z "$PR_NUMBER" ]; then
  PR_NUMBER="1"
fi

# Count files (comma‑separated list)
IFS=','
set -- $CHANGED_FILES
COUNT=$#

# Determine badge based on count
if [ "$COUNT" -le 5 ]; then
  BADGE="🛡️ Small"
elif [ "$COUNT" -le 20 ]; then
  BADGE="⚔️ Medium"
else
  BADGE="☢️ Massive"
fi

COMMENT="## 📜 Apocalypse Badge\n\nYour PR changes $COUNT file(s). Badge: $BADGE"

# If no token is provided (e.g., during tests), just output the comment
if [ -z "$TOKEN" ]; then
  echo "$COMMENT"
  exit 0
fi

# In a real run we would post the comment via the GitHub API.
# For brevity and offline safety we simply echo what would happen.
echo "Would post comment to $REPO PR #$PR_NUMBER"
