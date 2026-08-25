#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: In tests we replace curl with a function that records calls.

# Load event payload
EVENT_PATH="${GITHUB_EVENT_PATH:-}"
if [[ -z "$EVENT_PATH" || ! -f "$EVENT_PATH" ]]; then
  echo "::error ::GITHUB_EVENT_PATH not set or file missing"
  exit 1
fi

# Extract PR title using jq (assume jq is available)
if ! command -v jq >/dev/null 2>&1; then
  echo "::error ::jq is required"
  exit 1
fi

TITLE=$(jq -r .pull_request.title "$EVENT_PATH")
NUMBER=$(jq -r .pull_request.number "$EVENT_PATH")
REPO=$(jq -r .repository.full_name "$EVENT_PATH")

# Determine labels
labels=()

lower_title=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]')

if [[ "$lower_title" == *bug* ]]; then
  labels+=("bug")
fi
if [[ "$lower_title" == *add* ]] || [[ "$lower_title" == *implement* ]] || [[ "$lower_title" == *feature* ]]; then
  labels+=("feature")
fi
if [[ "$lower_title" == *doc* ]] || [[ "$lower_title" == *readme* ]] || [[ "$lower_title" == *documentation* ]]; then
  labels+=("docs")
fi

# Add a whimsical emoji label
EMOJIS=("🚀" "🧟" "🦄" "🌵" "🤖")
# Mock rationale: Use deterministic selection for tests by using first emoji.
selected_emoji="${EMOJIS[0]}"
labels+=("emoji-${selected_emoji}")

# Join labels for debugging output
label_str=$(IFS=,; echo "${labels[*]}")

# Call GitHub API to add labels
API_URL="https://api.github.com/repos/${REPO}/issues/${NUMBER}/labels"
payload=$(printf '[%s]' "$(printf '\"%s\",' "${labels[@]}" | sed 's/,\$//')")

# Mock rationale: In real run we use curl, but in tests curl is overridden.
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github+json" \
  -d "$payload" "$API_URL" >/dev/null

# Output for debugging
echo "Added labels: $label_str"
