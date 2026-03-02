#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
# Helper: log with a prefix
# ---------------------------------------------------------------------------
log() {
  echo "[nightly-commit-emoji-annotator] $*"
}

# ---------------------------------------------------------------------------
# Input handling
# ---------------------------------------------------------------------------
GITHUB_TOKEN="${INPUT_GITHUB_TOKEN:-}"
COMMIT_SHA="${INPUT_COMMIT_SHA:-}"
MESSAGE="${INPUT_MESSAGE:-}"
REPO="${GITHUB_REPOSITORY:-}"

if [[ -z "$GITHUB_TOKEN" || -z "$COMMIT_SHA" || -z "$REPO" ]]; then
  log "Error: github_token, commit_sha, and repository context are required."
  exit 1
fi

# If MESSAGE not supplied, fetch it via the API (offline tests will mock curl)
if [[ -z "$MESSAGE" ]]; then
  log "Fetching commit message for $COMMIT_SHA..."
  RESPONSE=$(curl -sSL -H "Authorization: token $GITHUB_TOKEN" \
    "https://api.github.com/repos/$REPO/commits/$COMMIT_SHA")
  MESSAGE=$(echo "$RESPONSE" | grep -Po '"message":\s*"\K[^"]+')
fi

# ---------------------------------------------------------------------------
# Emoji selection heuristics
# ---------------------------------------------------------------------------
select_emoji() {
  local msg="$1"
  shopt -s nocasematch
  if [[ $msg =~ fix|bug|patch ]]; then
    echo "🛠️"
  elif [[ $msg =~ feat|feature|add|implement ]]; then
    echo "✨"
  elif [[ $msg =~ docs|doc|readme|documentation ]]; then
    echo "📚"
  elif [[ $msg =~ test|spec|coverage ]]; then
    echo "✅"
  else
    echo "🤔"
  fi
  shopt -u nocasematch
}

EMOJI=$(select_emoji "$MESSAGE")
log "Selected emoji: $EMOJI for message: \"$MESSAGE\""

# ---------------------------------------------------------------------------
# Post reaction via GitHub Reactions API
# ---------------------------------------------------------------------------
API_URL="https://api.github.com/repos/$REPO/commits/$COMMIT_SHA/reactions"
log "Posting reaction to $API_URL"

RESPONSE=$(curl -sSL -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.squirrel-girl-preview+json" \
  -d "{\"content\": \"$EMOJI\"}" \
  "$API_URL")

if echo "$RESPONSE" | grep -q "created"; then
  log "Successfully added reaction $EMOJI to commit $COMMIT_SHA"
else
  log "Failed to add reaction. Response: $RESPONSE"
  exit 1
fi
