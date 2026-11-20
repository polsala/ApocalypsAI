#!/usr/bin/env bash
set -euo pipefail

# Ensure we have the event payload path
EVENT_PATH="${GITHUB_EVENT_PATH:-}"
if [[ -z "$EVENT_PATH" ]]; then
  echo "GITHUB_EVENT_PATH not set"
  exit 1
fi

# Extract the PR number using jq (available in the GitHub Actions runtime)
PR_NUMBER=$(jq -r .pull_request.number "$EVENT_PATH")
if [[ "$PR_NUMBER" == "null" || -z "$PR_NUMBER" ]]; then
  echo "Not a pull request event – nothing to do."
  exit 0
fi

# Hard‑coded list of whimsical quotes
QUOTES=(
  "The only limit to our realization of tomorrow is our doubts of today."
  "Adventure is out there!"
  "Keep calm and code on."
  "May the force be with you."
  "In the middle of difficulty lies opportunity."
)

# Deterministic selection based on PR number
INDEX=$(( PR_NUMBER % ${#QUOTES[@]} ))
SELECTED="${QUOTES[$INDEX]}"

# Build the API request
API_URL="https://api.github.com/repos/${GITHUB_REPOSITORY}/issues/${PR_NUMBER}/comments"
PAYLOAD=$(printf '{"body":"%s"}' "$SELECTED")

# Allow the curl command to be overridden for testing via CURL_CMD env var
CURL_CMD="${CURL_CMD:-curl}"
$CURL_CMD -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d "$PAYLOAD" \
  "$API_URL"

exit 0
