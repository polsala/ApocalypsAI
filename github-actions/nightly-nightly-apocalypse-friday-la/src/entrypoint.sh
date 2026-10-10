#!/usr/bin/env sh
set -e

# Ensure required env vars are present
if [ -z "$GITHUB_TOKEN" ]; then
  echo "::error::GITHUB_TOKEN is not set"
  exit 1
fi
if [ -z "$GITHUB_EVENT_PATH" ]; then
  echo "::error::GITHUB_EVENT_PATH is not set"
  exit 1
fi

# Read event payload
EVENT_JSON=$(cat "$GITHUB_EVENT_PATH")
ISSUE_NUMBER=$(echo "$EVENT_JSON" | grep -o '"number": *[0-9]*' | head -n1 | grep -o '[0-9]*')
REPO_FULL=$(echo "$EVENT_JSON" | grep -o '"full_name": *"[^"]*"' | head -n1 | cut -d'"' -f4)
CREATED_AT=$(echo "$EVENT_JSON" | grep -o '"created_at": *"[^"]*"' | head -n1 | cut -d'"' -f4)

if [ -z "$ISSUE_NUMBER" ] || [ -z "$REPO_FULL" ] || [ -z "$CREATED_AT" ]; then
  echo "::error::Failed to parse event payload"
  exit 1
fi

# Determine day of week (0=Sunday, 5=Friday)
DAY_OF_WEEK=$(date -u -d "$CREATED_AT" +%w)
if [ "$DAY_OF_WEEK" != "5" ]; then
  echo "Issue #$ISSUE_NUMBER was not opened on Friday (day $DAY_OF_WEEK). No label applied."
  exit 0
fi

# Apply label via GitHub API
API_URL="https://api.github.com/repos/$REPO_FULL/issues/$ISSUE_NUMBER/labels"
PAYLOAD="[\"${LABEL_NAME}\"]"

response=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d "$PAYLOAD" \
  "$API_URL")

if [ "$response" -ge 200 ] && [ "$response" -lt 300 ]; then
  echo "Successfully added label '$LABEL_NAME' to issue #$ISSUE_NUMBER."
else
  echo "::error::Failed to add label (HTTP $response)"
  exit 1
fi
