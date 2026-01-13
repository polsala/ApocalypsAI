#!/usr/bin/env bash
set -euo pipefail

# Load payload path (GitHub provides this env var)
PAYLOAD="${EVENT_PAYLOAD:-}"
if [[ -z "$PAYLOAD" ]]; then
  echo "No EVENT_PAYLOAD provided, exiting without action."
  exit 0
fi

# Extract fields from payload (very simple JSON parsing, sufficient for test)
TITLE=$(grep -i '"title"' "$PAYLOAD" | head -1 | cut -d'"' -f4)
BODY=$(grep -i '"body"' "$PAYLOAD" | head -1 | cut -d'"' -f4)
NUMBER=$(grep -i '"number"' "$PAYLOAD" | head -1 | grep -o '[0-9]\+')

# Default keywordâtoâlabel map (can be overridden via LABEL_CONFIG)
declare -A MAP
MAP=(
  [radiation]=radiation
  [mutant]=mutant
  [survivor]=survivor
)

# If a custom JSON config is supplied, attempt a very naive parse (key:value pairs)
if [[ -n "${LABEL_CONFIG:-}" && "${LABEL_CONFIG}" != "" ]]; then
  # Remove surrounding braces and spaces
  CONFIG=$(echo "$LABEL_CONFIG" | tr -d '{} ' )
  IFS=',' read -ra PAIRS <<< "$CONFIG"
  for pair in "${PAIRS[@]}"; do
    IFS=':' read -r key val <<< "$pair"
    # Strip quotes if present
    key=$(echo "$key" | tr -d '"')
    val=$(echo "$val" | tr -d '"')
    MAP["$key"]="$val"
  done
fi

# Find matching labels
labels=()
for kw in "${!MAP[@]}"; do
  if [[ "$TITLE" =~ $kw ]] || [[ "$BODY" =~ $kw ]]; then
    labels+=("${MAP[$kw]}")
  fi
done

if [[ ${#labels[@]} -eq 0 ]]; then
  echo "No matching keywords found; no labels added."
  exit 0
fi

# Prepare JSON array for API call
json=$(printf '[%s]' "$(printf '"%s",' "${labels[@]}" | sed 's/,\$//')")

# Call GitHub API to add labels
API_URL="https://api.github.com/repos/${GITHUB_REPOSITORY}/issues/${NUMBER}/labels"
# Use curl; in tests curl is stubbed
response=$(curl -s -X POST -H "Authorization: token ${GITHUB_TOKEN}" -H "Accept: application/vnd.github+json" -d "$json" "$API_URL")

echo "Added labels: ${labels[*]}"
exit 0
