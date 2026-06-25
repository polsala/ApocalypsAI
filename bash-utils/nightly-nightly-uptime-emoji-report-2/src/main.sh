#!/usr/bin/env bash
# nightly-uptime-emoji-report
# Shows uptime with an emoji.

# Get uptime in seconds
if [[ -n "$MOCK_UPTIME" ]]; then
  uptime_seconds=$MOCK_UPTIME
else
  # /proc/uptime first field is seconds with decimals
  if [[ -r /proc/uptime ]]; then
    uptime_seconds=$(awk '{print int($1)}' /proc/uptime)
  else
    echo "Cannot read /proc/uptime" >&2
    exit 1
  fi
fi

# Compute days, hours, minutes
days=$(( uptime_seconds / 86400 ))
hours=$(( (uptime_seconds % 86400) / 3600 ))
minutes=$(( (uptime_seconds % 3600) / 60 ))

# Determine emoji
if (( uptime_seconds < 86400 )); then
  emoji="🌱"
elif (( uptime_seconds < 604800 )); then
  emoji="🌿"
elif (( uptime_seconds < 2592000 )); then
  emoji="🌳"
else
  emoji="🏜️"
fi

printf "Uptime: %d days, %d hours, %d minutes %s\n" "$days" "$hours" "$minutes" "$emoji"
