#!/usr/bin/env bash
set -euo pipefail

MIN_LENGTH="${1}"
EVENT_PATH="${GITHUB_EVENT_PATH:-}"

if [[ -z "${EVENT_PATH}" ]]; then
  echo "::error::GITHUB_EVENT_PATH is not set."
  exit 1
fi

# Extract title using jq (assume jq is available)
if ! command -v jq >/dev/null 2>&1; then
  echo "::error::jq is required but not installed."
  exit 1
fi

TITLE=$(jq -r .pull_request.title "${EVENT_PATH}")

if [[ -z "${TITLE}" ]]; then
  echo "::error::Could not find pull request title in event payload."
  exit 1
fi

TITLE_LENGTH=${#TITLE}

if (( TITLE_LENGTH < MIN_LENGTH )); then
  echo "::error::PR title is too short (${TITLE_LENGTH} < ${MIN_LENGTH})."
  exit 1
else
  echo "PR title length (${TITLE_LENGTH}) meets minimum (${MIN_LENGTH})."
fi
