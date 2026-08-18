#!/usr/bin/env bash
set -euo pipefail

# Expect PR_TITLE env var
title="${PR_TITLE:-}"
labels=()

if [[ "$title" == *"[bug]"* ]]; then
  labels+=("bug")
fi
if [[ "$title" == *"[feature]"* ]]; then
  labels+=("enhancement")
fi

# Join labels with commas
joined=$(IFS=,; echo "${labels[*]}")

# Output for GitHub Actions
echo "labels=$joined" >> "$GITHUB_OUTPUT"

echo "Added labels: $joined"
