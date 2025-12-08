#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: This script reads the GitHub event payload, extracts PR title,
# determines an emoji label, and adds it via GitHub API.

EVENT_PATH="${GITHUB_EVENT_PATH:-}"
REPO="${GITHUB_REPOSITORY:-}"
TOKEN="${GITHUB_TOKEN:-}"

if [[ -z "$EVENT_PATH" || -z "$REPO" || -z "$TOKEN" ]]; then
  echo "Missing required environment variables."
  exit 1
fi

# Extract PR number and title
PR_NUMBER=$(jq -r .pull_request.number "$EVENT_PATH")
PR_TITLE=$(jq -r .pull_request.title "$EVENT_PATH")

# Determine emoji based on first word (lowercased)
FIRST_WORD=$(echo "$PR_TITLE" | awk '{print tolower($1)}')
case "$FIRST_WORD" in
  fix|bug) EMOJI="🐛" ;;
  feat|feature) EMOJI="✨" ;;
  docs) EMOJI="📚" ;;
  refactor) EMOJI="🔧" ;;
  test|tests) EMOJI="✅" ;;
  chore) EMOJI="🧹" ;;
  *) EMOJI="❓" ;;
esac

LABEL_NAME="${EMOJI} PR"

# Add label via GitHub API
API_URL="https://api.github.com/repos/${REPO}/issues/${PR_NUMBER}/labels"
curl -s -X POST -H "Authorization: token ${TOKEN}" -H "Accept: application/vnd.github+json" \
  -d "$(jq -n --arg name \"$LABEL_NAME\" '{labels: [$name]}')" "$API_URL"

exit 0
