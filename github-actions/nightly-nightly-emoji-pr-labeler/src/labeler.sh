#!/usr/bin/env bash
set -e

# Accept the PR title as the first argument
title="$1"

# Emoji‑to‑label map
declare -A emoji_map=(
  ["🐛"]="bug"
  ["✨"]="enhancement"
  ["📚"]="documentation"
  ["🚀"]="feature"
)

labels=()

# Iterate over known emojis and collect matching labels
for emoji in "${!emoji_map[@]}"; do
  if [[ "$title" == *"$emoji"* ]]; then
    labels+=("${emoji_map[$emoji]}")
  fi
done

# Remove duplicate labels while preserving order
if [ ${#labels[@]} -gt 0 ]; then
  uniq_labels=$(printf "%s\n" "${labels[@]}" | awk '!seen[$0]++' | paste -sd "," -)
else
  uniq_labels=""
fi

# Emit the GitHub Actions output
echo "::set-output name=labels::$uniq_labels"
