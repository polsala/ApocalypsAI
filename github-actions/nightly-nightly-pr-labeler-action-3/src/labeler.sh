#!/usr/bin/env bash
set -euo pipefail

# Default mapping if the user does not provide one
default_mapping='{"bug":"bug","feature":"enhancement","docs":"documentation"}'

# Use the input mapping or fall back to the default
mapping="${INPUT_LABEL_MAPPING:-$default_mapping}"

# Path to the GitHub event payload (provided by the runner)
event_path="${GITHUB_EVENT_PATH:-}"
if [[ -z "$event_path" || ! -f "$event_path" ]]; then
  echo "::error::GITHUB_EVENT_PATH not set or file missing"
  exit 1
fi

# Extract needed fields using jq (jq is pre‑installed on GitHub runners)
title=$(jq -r .pull_request.title "$event_path")
pr_number=$(jq -r .pull_request.number "$event_path")
repo=$(jq -r .repository.full_name "$event_path")

# Determine which labels apply
labels=()
while IFS=":" read -r keyword label; do
  if [[ "$title" =~ $keyword ]]; then
    labels+=("$label")
  fi
done < <(echo "$mapping" | jq -r 'to_entries|map("\(.key):\(.value)")|.[]')

if [[ ${#labels[@]} -eq 0 ]]; then
  echo "No matching labels for title: $title"
  exit 0
fi

# Add labels – if gh is available we call the real API, otherwise we mock it
if command -v gh >/dev/null 2>&1; then
  for lbl in "${labels[@]}"; do
    gh api -X POST "/repos/$repo/issues/$pr_number/labels" -f labels="[\"$lbl\"]" >/dev/null 2>&1 || echo "Failed to add label $lbl"
  done
else
  for lbl in "${labels[@]}"; do
    echo "Mock add label '$lbl' to PR #$pr_number in $repo"
  done
fi

exit 0
