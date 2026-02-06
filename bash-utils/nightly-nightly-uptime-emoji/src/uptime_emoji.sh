#!/usr/bin/env bash
set -euo pipefail

# Parse an uptime string like "up 2 days, 3 hours, 15 minutes"
parse_uptime() {
  local up_str="$1"
  local days=0 hours=0 minutes=0
  if [[ "$up_str" =~ ([0-9]+)\ days? ]]; then
    days="${BASH_REMATCH[1]}"
  fi
  if [[ "$up_str" =~ ([0-9]+)\ hours? ]]; then
    hours="${BASH_REMATCH[1]}"
  fi
  if [[ "$up_str" =~ ([0-9]+)\ minutes? ]]; then
    minutes="${BASH_REMATCH[1]}"
  fi
  echo $((days*1440 + hours*60 + minutes))
}

# Obtain the uptime string – use argument if supplied (for testing)
if [[ $# -gt 0 ]]; then
  uptime_str="$1"
else
  # `uptime -p` returns something like "up 2 hours, 15 minutes"
  uptime_str=$(uptime -p)
fi

# Convert to total minutes
total_minutes=$(parse_uptime "$uptime_str")

# Choose an emoji based on total minutes
if (( total_minutes < 60 )); then
  emoji="🌱"
elif (( total_minutes < 360 )); then
  emoji="🌞"
elif (( total_minutes < 1440 )); then
  emoji="🌆"
else
  emoji="🌙"
fi

# Compute hours and minutes for display
display_hours=$(( total_minutes / 60 ))
display_minutes=$(( total_minutes % 60 ))

printf "Uptime: %dh %dm %s\n" "$display_hours" "$display_minutes" "$emoji"
