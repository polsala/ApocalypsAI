#!/usr/bin/env bash
# uptime_emoji.sh - display uptime with an emoji
# If an argument is provided, it is treated as the uptime in seconds (for testing).

if [[ -n "$1" ]]; then
  uptime_seconds=$1
else
  # Read the first field from /proc/uptime and truncate to integer seconds
  uptime_seconds=$(awk '{print int($1)}' /proc/uptime)
fi

if (( uptime_seconds < 86400 )); then
  emoji="🌱"
elif (( uptime_seconds < 604800 )); then
  emoji="🌳"
else
  emoji="🏔️"
fi

printf "Uptime: %d seconds %s\n" "$uptime_seconds" "$emoji"
