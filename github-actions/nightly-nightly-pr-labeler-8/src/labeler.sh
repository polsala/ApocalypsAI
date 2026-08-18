#!/usr/bin/env bash
set -euo pipefail

# Input: multiline string of file paths as a single argument
IFS=$'\n' read -d '' -r -a files <<< "$1"

declare -A label_map=(
  ["documentation"]=0
  ["python"]=0
  ["markdown"]=0
  ["misc"]=0
)

for file in "${files[@]}"; do
  if [[ "$file" == docs/** ]]; then
    label_map["documentation"]=1
  elif [[ "$file" == src/**/*.py ]]; then
    label_map["python"]=1
  elif [[ "$file" == *.md ]]; then
    label_map["markdown"]=1
  else
    label_map["misc"]=1
  fi
done

labels=()
for label in "${!label_map[@]}"; do
  if [[ ${label_map[$label]} -eq 1 ]]; then
    labels+=("$label")
  fi
done

IFS=,
echo "Labels to add: ${labels[*]}"
