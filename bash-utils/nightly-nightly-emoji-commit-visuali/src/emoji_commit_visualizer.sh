#!/usr/bin/env bash
# emoji_commit_visualizer.sh
# Prefixes git commit messages with emojis based on keywords.

set -euo pipefail

# Default range is HEAD
range="${1:-HEAD}"

# Mapping of keywords to emojis
declare -A emoji_map=(
  ["fix"]="🛠️"
  ["add"]="✨"
  ["remove"]="❌"
  ["refactor"]="♻️"
  ["docs"]="📚"
  ["test"]="✅"
)

# Function to select emoji for a line
select_emoji() {
  local line_lower
  line_lower=$(echo "$1" | tr '[:upper:]' '[:lower:]')
  for key in "${!emoji_map[@]}"; do
    if [[ "$line_lower" == *"$key"* ]]; then
      echo "${emoji_map[$key]}"
      return
    fi
  done
  echo "🔎"
}

# Read commit messages and output with emojis
while IFS= read -r msg; do
  emoji=$(select_emoji "$msg")
  printf "%s %s\n" "$emoji" "$msg"
 done < <(git log --pretty=%s "$range")
