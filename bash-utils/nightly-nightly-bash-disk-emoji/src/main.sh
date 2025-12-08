#!/usr/bin/env bash
set -euo pipefail

# Get df output in POSIX format, skip header
df_output=$(df -P -h | tail -n +2)

while read -r line; do
  # Extract mount point (6th field) and usage percent (5th field)
  mount=$(echo "$line" | awk '{print $6}')
  usage=$(echo "$line" | awk '{print $5}')
  # Remove % sign
  percent=${usage%\%}
  # Calculate filled blocks (0-10)
  filled=$(( percent * 10 / 100 ))
  empty=$((10 - filled))
  # Build bar using emojis
  bar=$(printf '🟥%.0s' $(seq 1 $filled))
  bar+=$(printf '⬜%.0s' $(seq 1 $empty))
  echo "$mount $usage $bar"
done <<< "$df_output"
