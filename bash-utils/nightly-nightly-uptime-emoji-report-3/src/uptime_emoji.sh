#!/usr/bin/env bash
# uptime_emoji.sh - report uptime with emoji

# Function to format seconds into days, hours, minutes
format_uptime() {
  local total_seconds=$1
  local days=$(( total_seconds / 86400 ))
  local hours=$(( (total_seconds % 86400) / 3600 ))
  local minutes=$(( (total_seconds % 3600) / 60 ))
  echo "${days}d ${hours}h ${minutes}m"
}

# Determine uptime seconds
if [[ -n $1 ]]; then
  uptime_seconds=$1
else
  # Read from /proc/uptime, first field is seconds with fractions
  if [[ -r /proc/uptime ]]; then
    uptime_seconds=$(awk '{print int($1)}' /proc/uptime)
  else
    echo "Cannot read /proc/uptime" >&2
    exit 1
  fi
fi

# Choose emoji based on duration
if (( uptime_seconds < 3600 )); then
  emoji="🐣"
elif (( uptime_seconds < 86400 )); then
  emoji="🐔"
elif (( uptime_seconds < 604800 )); then
  emoji="🐓"
else
  emoji="🦅"
fi

human=$(format_uptime "$uptime_seconds")
echo "Uptime: $human $emoji"
