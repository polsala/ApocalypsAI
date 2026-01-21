#!/usr/bin/env bash
set -euo pipefail

# Arguments: mapping string
MAPPING="${1}"

# Ensure GITHUB_EVENT_PATH exists
if [[ ! -f "${GITHUB_EVENT_PATH:-}" ]]; then
  echo "GITHUB_EVENT_PATH not set or file missing" >&2
  exit 1
fi

# Extract PR title
TITLE=$(jq -r .pull_request.title "${GITHUB_EVENT_PATH}")

# Iterate over mapping lines
while IFS= read -r line; do
  # Skip empty lines
  [[ -z "$line" ]] && continue
  KEYWORD="${line%%:*}"
  LABEL="${line##*:}"
  if [[ -z "$KEYWORD" || -z "$LABEL" ]]; then
    continue
  fi
  shopt -s nocasematch
  if [[ "$TITLE" == *"$KEYWORD"* ]]; then
    echo "::add-label::${LABEL}"
    exit 0
  fi
  shopt -u nocasematch
done <<< "$MAPPING"

# No label matched
exit 0
