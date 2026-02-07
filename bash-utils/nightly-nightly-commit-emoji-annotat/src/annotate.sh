#!/usr/bin/env bash
# annotate.sh – Prefix commit messages with emojis based on conventional commit types

# Declare associative array mapping commit types to emojis
declare -A map=(
  ["feat"]="✨"
  ["fix"]="🛠️"
  ["docs"]="📚"
  ["test"]="✅"
  ["chore"]="🧹"
  ["refactor"]="♻️"
  ["perf"]="🚀"
  ["style"]="🎨"
  ["build"]="🏗️"
  ["ci"]="🤖"
  ["revert"]="⏪"
)

while IFS= read -r line; do
  # Extract the type token (text before first ':' or space)
  type=$(echo "$line" | awk -F'[: ]' '{print $1}')
  emoji=${map[$type]:-"🔹"}
  echo "$emoji $line"
done
