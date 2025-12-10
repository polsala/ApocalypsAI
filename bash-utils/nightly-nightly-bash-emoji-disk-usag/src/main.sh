#!/usr/bin/env bash
set -euo pipefail

# Default target is root filesystem
TARGET="${1:-/}"

# Allow overriding the df command (useful for testing)
DF_CMD=${DF_CMD:-"df -h"}

# Capture df output, skip header line
output=$($DF_CMD "$TARGET" | tail -n +2)

while IFS= read -r line; do
  # Extract the Use% column (5th field) and strip the % sign
  usage=$(echo "$line" | awk '{print $5}' | tr -d '%')
  # Default emoji
  emoji="🟢"
  if (( usage > 80 )); then
    emoji="💀"
  elif (( usage > 60 )); then
    emoji="🔴"
  elif (( usage > 40 )); then
    emoji="🟠"
  elif (( usage > 20 )); then
    emoji="🟡"
  fi
  echo "$line $emoji"
done <<< "$output"
