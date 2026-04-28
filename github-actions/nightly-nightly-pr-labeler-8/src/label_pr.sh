#!/usr/bin/env bash
set -euo pipefail

# Required environment variables provided by GitHub Actions
EVENT_PATH="${GITHUB_EVENT_PATH:-}"
REPO="${GITHUB_REPOSITORY:-}"
TOKEN="${GITHUB_TOKEN:-}"
LABEL="${LABEL:-}"

if [[ -z "$EVENT_PATH" || -z "$REPO" || -z "$TOKEN" || -z "$LABEL" ]]; then
  echo "Missing required environment variables."
  exit 1
fi

# Extract PR number from the event JSON (supports pull_request events)
PR_NUMBER=$(jq -r .pull_request.number "$EVENT_PATH")
if [[ "$PR_NUMBER" == "null" || -z "$PR_NUMBER" ]]; then
  echo "No pull_request number found in event."
  exit 1
fi

API_URL="https://api.github.com/repos/$REPO/issues/$PR_NUMBER/labels"

# Prepare JSON payload
PAYLOAD=$(jq -nc --arg label "$LABEL" '{labels: [$label]}')

# Add label via POST request
curl -s -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "$API_URL" \
  -d "$PAYLOAD"

echo "Label '$LABEL' added to PR #$PR_NUMBER."
