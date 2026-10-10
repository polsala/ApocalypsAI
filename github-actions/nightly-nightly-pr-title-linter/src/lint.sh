#!/usr/bin/env bash
set -euo pipefail

# Ensure the GitHub event payload is available
if [[ -z "${GITHUB_EVENT_PATH:-}" ]]; then
  echo "::error::GITHUB_EVENT_PATH is not set. This action must run in a GitHub Actions environment."
  exit 1
fi

# Extract the PR title using jq (available in the default GitHub Actions runner)
if ! command -v jq >/dev/null 2>&1; then
  echo "::error::jq is required but not installed."
  exit 1
fi

title=$(jq -r .pull_request.title "$GITHUB_EVENT_PATH")
if [[ -z "$title" || "$title" == "null" ]]; then
  echo "::error::Could not extract pull request title from event payload."
  exit 1
fi

# Use the provided pattern (default is '.*')
pattern="${INPUT_PATTERN:-.*}"

# Perform the regex match (Bash uses extended regex with =~)
if [[ "$title" =~ $pattern ]]; then
  echo "✅ PR title matches pattern: $pattern"
else
  echo "::error::PR title does not match pattern: $pattern"
  echo "   Title: $title"
  exit 1
fi
