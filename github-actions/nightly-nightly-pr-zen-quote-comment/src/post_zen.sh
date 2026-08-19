#!/usr/bin/env bash
set -euo pipefail

# Default API URL if not overridden
GITHUB_API_URL="${GITHUB_API_URL:-https://api.github.com}"

# Ensure required variables are present
if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "Error: GITHUB_TOKEN is not set" >&2
  exit 1
fi
if [[ -z "${PR_NUMBER:-}" ]]; then
  echo "Error: PR_NUMBER is not set" >&2
  exit 1
fi
if [[ -z "${GITHUB_REPOSITORY:-}" ]]; then
  echo "Error: GITHUB_REPOSITORY is not set" >&2
  exit 1
fi

# Static list of zen quotes
quotes=(
  "The journey of a thousand miles begins with one step."
  "Simplicity is the ultimate sophistication."
  "What you think, you become."
  "The only constant is change."
  "Be the change you wish to see in the world."
)

# Pick a quote (deterministic if RANDOM is seeded)
index=$(( RANDOM % ${#quotes[@]} ))
quote="${quotes[$index]}"

# Build JSON payload
payload=$(printf '{"body":"%s"}' "$quote")

# POST comment to the PR
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$GITHUB_API_URL/repos/$GITHUB_REPOSITORY/issues/$PR_NUMBER/comments" \
  -d "$payload"
