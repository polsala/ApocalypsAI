#!/usr/bin/env bash
# emoji-annotate.sh – prepend an emoji to each commit message read from stdin
# Supported conventional‑commit types are mapped to emojis; unknown types get a light‑bulb.

declare -A map=(
  ["fix"]="🔧"
  ["feat"]="✨"
  ["docs"]="📚"
  ["refactor"]="♻️"
  ["test"]="✅"
  ["chore"]="🧹"
)

while IFS= read -r line; do
  # Extract the type token before a colon or opening parenthesis, strip spaces
  type=$(echo "$line" | awk -F'[:(]' '{print $1}' | tr -d ' ')
  emoji=${map[$type]}
  if [[ -z $emoji ]]; then
    emoji="💡"
  fi
  echo "$emoji $line"
done
