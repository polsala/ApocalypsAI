#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Read inputs from environment variables
GITHUB_TOKEN="$GITHUB_TOKEN"
PROVERBS_FILE="$PROVERBS_FILE"

if [ -z "$GITHUB_TOKEN" ]; then
  echo "Error: GITHUB_TOKEN is not set. Please provide it as an input."
  exit 1
fi

if [ ! -f "$PROVERBS_FILE" ]; then
  echo "Error: Proverbs file not found at $PROVERBS_FILE"
  exit 1
fi

# Get PR number from GITHUB_EVENT_PATH
# Mock rationale: In a real GitHub Action, GITHUB_EVENT_PATH points to a JSON file
# containing the webhook payload. We need to parse it to get the PR number.
# For testing, we'll create a dummy JSON file.
if [ -z "$GITHUB_EVENT_PATH" ]; then
  echo "Error: GITHUB_EVENT_PATH is not set. This action must run on a pull_request event."
  exit 1
fi

PR_NUMBER=$(jq -r '.pull_request.number' "$GITHUB_EVENT_PATH")

if [ -z "$PR_NUMBER" ] || [ "$PR_NUMBER" == "null" ]; then
  echo "Could not determine PR number from GITHUB_EVENT_PATH. Skipping comment."
  exit 0 # Not an error if not a PR, just skip.
fi

# Read all proverbs into an array
mapfile -t PROVERBS < "$PROVERBS_FILE"

# Pick a random proverb
# Mock rationale: RANDOM is shell built-in, but for deterministic tests, we control the input proverbs.
# With only one proverb in the mock file, it will always pick that one.
RANDOM_INDEX=$(( RANDOM % ${#PROVERBS[@]} ))
PROVERB="${PROVERBS[$RANDOM_INDEX]}"

echo "Adding proverb to PR #$PR_NUMBER: \"$PROVERB\""

# Use gh CLI to comment on the PR
# Mock rationale: In tests, 'gh' will be a mock executable.
# In a real action, it's the GitHub CLI.
echo "$PROVERB" | gh pr comment "$PR_NUMBER" --body-file - --repo "$GITHUB_REPOSITORY"
