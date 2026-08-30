#!/usr/bin/env bash
set -euo pipefail

# Load inputs
TOKEN="${GITHUB_TOKEN}"
MAP_JSON="${KEYWORD_EMOJI_MAP}"
EVENT_PATH="${GITHUB_EVENT_PATH}"

# Extract PR title using jq (jq is available in the default GitHub runner)
PR_TITLE=$(jq -r .pull_request.title "$EVENT_PATH")
# Default emoji if no match
EMOJI="❓"

# Convert JSON map to Bash associative array
declare -A map
while IFS="=" read -r key value; do
  map["$key"]="$value"
# The jq command outputs lines like "key=value"
done < <(echo "$MAP_JSON" | jq -r "to_entries|map(\"\(.key)=\(.value)\")|.[]")

# Find first matching keyword (regex match)
for kw in "${!map[@]}"; do
  if [[ "$PR_TITLE" =~ $kw ]]; then
    EMOJI="${map[$kw]}"
    break
  fi
done

# Export as GitHub Action output
# GITHUB_OUTPUT is set by the runner; we append the key/value pair
if [[ -z "${GITHUB_OUTPUT:-}" ]]; then
  echo "::set-output name=emoji::$EMOJI"
else
  echo "emoji=$EMOJI" >> "$GITHUB_OUTPUT"
fi
