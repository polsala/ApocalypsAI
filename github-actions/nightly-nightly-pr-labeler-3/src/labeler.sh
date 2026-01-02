#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: In tests we replace gh with a mock script.

# Determine PR number from event payload
EVENT_PATH="${GITHUB_EVENT_PATH:-}"
if [[ -z "$EVENT_PATH" ]]; then
  echo "Error: GITHUB_EVENT_PATH not set"
  exit 1
fi

PR_NUMBER=$(jq -r .number "$EVENT_PATH")
if [[ "$PR_NUMBER" == "null" || -z "$PR_NUMBER" ]]; then
  echo "Error: Could not extract PR number"
  exit 1
fi

# Get list of changed files
CHANGED_FILES=$(gh pr view "$PR_NUMBER" --json files -q '.files[].path' 2>/dev/null || true)

# Determine labels
declare -A LABELS
while IFS= read -r file; do
  case "$file" in
    docs/*|*.md) LABELS[docs]=1 ;;
    src/*|*.py|*.js|*.ts|*.rs|*.go) LABELS[code]=1 ;;
    tests/*) LABELS[tests]=1 ;;
    .github/*) LABELS[ci]=1 ;;
  esac
done <<< "$CHANGED_FILES"

# Apply labels
for label in "${!LABELS[@]}"; do
  gh pr edit "$PR_NUMBER" --add-label "$label"
 done
