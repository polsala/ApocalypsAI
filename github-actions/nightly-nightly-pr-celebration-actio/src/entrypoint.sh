#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: This script reads the GitHub event payload and posts a celebratory comment.

# Ensure required env vars
if [[ -z "${GITHUB_EVENT_PATH:-}" ]]; then
  echo "GITHUB_EVENT_PATH not set"
  exit 1
fi
if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "GITHUB_TOKEN not set"
  exit 1
fi

# Extract PR info
PR_NUMBER=$(jq -r .pull_request.number "$GITHUB_EVENT_PATH")
PR_TITLE=$(jq -r .pull_request.title "$GITHUB_EVENT_PATH")
REPO=$(jq -r .repository.full_name "$GITHUB_EVENT_PATH")

if [[ "$PR_NUMBER" == "null" || -z "$PR_NUMBER" ]]; then
  echo "No pull request data found"
  exit 0
fi

COMMENT="🎉 Congratulations on merging PR #${PR_NUMBER}: ${PR_TITLE}! Keep the apocalypse at bay!"

API_URL="https://api.github.com/repos/${REPO}/issues/${PR_NUMBER}/comments"

# Post comment
curl -s -X POST "$API_URL" \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  -d "$(printf '{\"body\":\"%s\"}' "$COMMENT")" > /dev/null

echo "Posted celebratory comment."
