#!/usr/bin/env bash
# uptime_emoji.sh - Convert system uptime to an emoji.
# If an argument is provided, it is interpreted as uptime in seconds (for testing).

set -euo pipefail

# Function to determine emoji based on seconds
get_emoji() {
  local secs=$1
  if (( secs < 3600 )); then
    echo "🚀"
  elif (( secs < 86400 )); then
    echo "🌞"
  elif (( secs < 604800 )); then
    echo "🌤"
  elif (( secs < 2592000 )); then
    echo "🌧"
  else
    echo "🐢"
  fi
}

if [[ $# -gt 0 ]]; then
  uptime_secs=$1
else
  # Read first field from /proc/uptime and truncate to integer seconds
  uptime_secs=$(awk '{print int($1)}' /proc/uptime)
fi

emoji=$(get_emoji "$uptime_secs")
echo "$emoji"
