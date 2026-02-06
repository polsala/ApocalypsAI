#!/usr/bin/env bash

set -euo pipefail

# Default arguments
DIR="${1:-.}"
COUNT="${2:-10}"

if [[ ! -d "$DIR" ]]; then
  echo "Error: $DIR is not a directory" >&2
  exit 1
fi

# Map size (bytes) to an emoji
map_emoji() {
  local size=$1
  if (( size < 1024*1024 )); then
    echo "🧚"
  elif (( size < 10*1024*1024 )); then
    echo "🐉"
  elif (( size < 100*1024*1024 )); then
    echo "🦖"
  else
    echo "🐢"
  fi
}

# Find files, get sizes in bytes, sort, and limit to COUNT
while IFS= read -r line; do
  size=$(awk '{print $1}' <<<"$line")
  path=$(awk '{print $2}' <<<"$line")
  emoji=$(map_emoji "$size")
  # Human‑readable size (e.g., 12K, 3.4M)
  hr=$(numfmt --to=iec-i --suffix=B "$size")
  printf "%s  %s  %s\n" "$emoji" "$hr" "$path"
# Use process substitution to feed the sorted list
# find prints: <size> <path>
# -printf "%s %p\n" prints size in bytes and full path
# sort -nr sorts numerically descending
# head limits the output
# Errors from find (e.g., permission denied) are silenced
#
# The loop reads from the subshell output
#
# Note: The while loop runs in the current shell, preserving variable values.
#
# End of loop

done < <(
  find "$DIR" -type f -printf "%s %p\n" 2>/dev/null |
  sort -nr |
  head -n "$COUNT"
)
