#!/usr/bin/env bash
set -euo pipefail

# Ensure required environment variables are present
if [[ -z "${GITHUB_EVENT_PATH:-}" ]]; then
  echo "GITHUB_EVENT_PATH not set"
  exit 1
fi
if [[ -z "${GITHUB_REPOSITORY:-}" ]]; then
  echo "GITHUB_REPOSITORY not set"
  exit 1
fi

# Extract PR number and title from the event payload
PR_NUMBER=$(jq -r .pull_request.number "$GITHUB_EVENT_PATH")
TITLE=$(jq -r .pull_request.title "$GITHUB_EVENT_PATH")

# Determine appropriate label based on title keywords
if [[ "$TITLE" =~ [Ff]eat ]]; then
  LABEL="feature"
elif [[ "$TITLE" =~ [Ff]ix ]]; then
  LABEL="bug"
elif [[ "$TITLE" =~ [Dd]ocs ]]; then
  LABEL="documentation"
else
  LABEL="misc"
fi

# Apply the label using the GitHub CLI
gh pr edit "$PR_NUMBER" --add-label "$LABEL"
