#!/usr/bin/env bash
set -euo pipefail

# Determine number of commits to analyze (default 100)
NUM_COMMITS="${1:-100}"

# Retrieve commit messages from the current repository
messages=$(git log -n "$NUM_COMMITS" --pretty=%B)

# Simplified Unicode emoji regex covering common emoji blocks
emoji_regex='[\x{1F600}-\x{1F64F}]|[\x{1F300}-\x{1F5FF}]|[\x{1F680}-\x{1F6FF}]|[\x{2600}-\x{26FF}]|[\x{2700}-\x{27BF}]'

# Declare associative array for counting
declare -A counts

# Iterate over each line of commit messages
while IFS= read -r line; do
  while [[ $line =~ $emoji_regex ]]; do
    emoji="${BASH_REMATCH[0]}"
    ((counts["$emoji"]++))
    # Remove the first matched emoji to continue searching the line
    line="${line#*$emoji}"
  done
done <<< "$messages"

# Output sorted results with a bar chart made of '#'
for emoji in "${!counts[@]}"; do
  echo -e "${counts[$emoji]}\t$emoji"
done | sort -nr | while IFS=$'\t' read -r count emoji; do
  bar=$(printf '%*s' "$count" '' | tr ' ' '#')
  echo -e "$emoji $count $bar"
done
