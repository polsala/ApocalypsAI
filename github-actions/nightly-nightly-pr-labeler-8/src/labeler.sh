#!/usr/bin/env bash
set -euo pipefail

# Determine PR number
if [[ -n "${GITHUB_REF-}" ]]; then
  PR_NUMBER="${GITHUB_REF##*/}"
else
  PR_NUMBER=$(jq -r .pull_request.number "$GITHUB_EVENT_PATH")
fi

# Default mapping if none provided
DEFAULT_MAPPING='{"docs/**":"documentation","tests/**":"tests","src/**":"code"}'
MAPPING="${LABEL_MAPPING:-$DEFAULT_MAPPING}"

# Fetch changed files via GitHub CLI (gh)
CHANGED_FILES=$(gh api "repos/${GITHUB_REPOSITORY}/pulls/${PR_NUMBER}/files" --paginate -q '.[].filename')

declare -A LABELS_TO_ADD

while IFS= read -r file; do
  echo "$MAPPING" | jq -r 'to_entries[] | "\(.key) \(.value)"' | while read -r pattern label; do
    # Use Bash's extended globbing for pattern matching
    shopt -s extglob
    if [[ "$file" == $pattern ]]; then
      LABELS_TO_ADD["$label"]=1
    fi
    shopt -u extglob
  done
done <<< "$CHANGED_FILES"

if [[ ${#LABELS_TO_ADD[@]} -gt 0 ]]; then
  # Build JSON array of labels
  LABELS_JSON=$(printf '%s\n' "${!LABELS_TO_ADD[@]}" | jq -R . | jq -s .)
  gh api -X POST "repos/${GITHUB_REPOSITORY}/issues/${PR_NUMBER}/labels" -f labels="$LABELS_JSON"
  echo "Added labels: ${!LABELS_TO_ADD[@]}"
else
  echo "No matching labels found."
fi
