#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: In real usage this would call the GitHub API via gh CLI or REST.
# For offline testing we simply echo the labels that would be added.

title="${PR_TITLE:-}"
labels=()

if [[ "$title" =~ [Bb]ug ]]; then
  labels+=("bug")
fi
if [[ "$title" =~ [Ff]eature ]] || [[ "$title" =~ [Ff]eat ]]; then
  labels+=("enhancement")
fi
if [[ "$title" =~ [Dd]oc ]]; then
  labels+=("documentation")
fi

if [ ${#labels[@]} -eq 0 ]; then
  echo "No matching labels for title: $title"
else
  for lbl in "${labels[@]}"; do
    echo "Adding label: $lbl"
  done
fi
