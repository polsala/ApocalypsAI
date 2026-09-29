#!/usr/bin/env bash
set -euo pipefail

title="${INPUT_TITLE:-}"
declare -A map=(
  ["bug"]="bug"
  ["fix"]="bug"
  ["feature"]="enhancement"
  ["add"]="enhancement"
  ["docs"]="documentation"
  ["doc"]="documentation"
  ["test"]="tests"
)

labels=()
lower_title=$(echo "$title" | tr '[:upper:]' '[:lower:]')
for keyword in "${!map[@]}"; do
  if [[ "$lower_title" == *"$keyword"* ]]; then
    labels+=("${map[$keyword]}")
  fi
done

# Remove duplicates
unique_labels=($(printf "%s\n" "${labels[@]}" | sort -u))

if [ ${#unique_labels[@]} -eq 0 ]; then
  echo "No matching labels found."
  echo "::set-output name=labels::"
else
  joined=$(IFS=,; echo "${unique_labels[*]}")
  echo "Suggested labels: $joined"
  echo "::set-output name=labels::$joined"
fi
