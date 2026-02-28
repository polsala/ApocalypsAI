#!/usr/bin/env bash
set -euo pipefail

# Function to get uptime seconds
get_uptime_seconds() {
  if [[ -n "${UPTIME_MOCK:-}" ]]; then
    echo "$UPTIME_MOCK"
  else
    # /proc/uptime first field is seconds (float). Convert to integer.
    awk '{print int($1)}' /proc/uptime
  fi
}

# Convert total seconds to a human‑readable string
format_uptime() {
  local total_seconds=$1
  local days=$(( total_seconds / 86400 ))
  local hours=$(( (total_seconds % 86400) / 3600 ))
  local minutes=$(( (total_seconds % 3600) / 60 ))
  local result=""
  if (( days > 0 )); then
    result+="${days}d "
  fi
  if (( hours > 0 )); then
    result+="${hours}h "
  fi
  result+="${minutes}m"
  echo "$result"
}

# Choose an emoji based on the number of days
choose_emoji() {
  local days=$1
  if (( days < 1 )); then
    echo "🌱"
  elif (( days <= 7 )); then
    echo "🌿"
  elif (( days <= 30 )); then
    echo "🌳"
  else
    echo "🌲"
  fi
}

main() {
  local seconds
  seconds=$(get_uptime_seconds)
  local days=$(( seconds / 86400 ))
  local formatted
  formatted=$(format_uptime "$seconds")
  local emoji
  emoji=$(choose_emoji "$days")
  echo "Uptime: $formatted $emoji"
}

main "$@"
