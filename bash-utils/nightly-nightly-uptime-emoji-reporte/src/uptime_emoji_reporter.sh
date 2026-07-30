#!/usr/bin/env bash
# nightly-uptime-emoji-reporter
# Usage: ./uptime_emoji_reporter.sh [seconds]
# If a seconds argument is provided, it is used instead of reading /proc/uptime (useful for testing).

if [[ $# -gt 0 ]]; then
  uptime_seconds=$1
else
  if [[ -r /proc/uptime ]]; then
    uptime_seconds=$(awk '{print int($1)}' /proc/uptime)
  else
    echo "Cannot read /proc/uptime"
    exit 1
  fi
fi

# Determine emoji based on uptime
if (( uptime_seconds < 3600 )); then
  emoji="🚀"
elif (( uptime_seconds < 21600 )); then
  emoji="🌞"
elif (( uptime_seconds < 43200 )); then
  emoji="🌤"
elif (( uptime_seconds < 86400 )); then
  emoji="🌙"
else
  emoji="💤"
fi

# Convert seconds to a human‑readable format
days=$(( uptime_seconds / 86400 ))
hours=$(( (uptime_seconds % 86400) / 3600 ))
minutes=$(( (uptime_seconds % 3600) / 60 ))

if (( days > 0 )); then
  human="${days}d ${hours}h ${minutes}m"
elif (( hours > 0 )); then
  human="${hours}h ${minutes}m"
else
  human="${minutes}m"
fi

echo "Uptime: ${human} ${emoji}"
