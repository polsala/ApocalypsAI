#!/usr/bin/env bash
# uptime-emoji.sh – Print an emoji representing system uptime.
#
# Usage: uptime-emoji.sh [seconds]
#   If a numeric argument is supplied, it is used as the uptime in seconds.
#   Otherwise the script reads the real uptime from /proc/uptime.
#
# Emoji mapping:
#   <  1 hour   (3600s) -> 🌱
#   <  1 day    (86400s) -> 🌿
#   <  1 week   (604800s) -> 🌳
#   >= 1 week            -> 🌲

set -euo pipefail

# Function to obtain uptime seconds
get_uptime_seconds() {
  if [[ $# -eq 1 && $1 =~ ^[0-9]+$ ]]; then
    echo "$1"
    return
  fi
  # Read from /proc/uptime; the first field is total seconds (float)
  if [[ -r /proc/uptime ]]; then
    awk '{print int($1)}' /proc/uptime
    return
  fi
  # Fallback: use the `uptime` command and parse its output (unlikely needed)
  uptime -p | grep -oE '[0-9]+' | paste -sd+ - | bc
}

seconds=$(get_uptime_seconds "$@")

if (( seconds < 3600 )); then
  emoji="🌱"
elif (( seconds < 86400 )); then
  emoji="🌿"
elif (( seconds < 604800 )); then
  emoji="🌳"
else
  emoji="🌲"
fi

echo "$emoji"
