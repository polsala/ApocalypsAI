#!/usr/bin/env bash

# nightly-uptime-emoji-report
# Reads system uptime and prints an emoji based on duration.

# Function to convert seconds to human‑readable format
format_uptime() {
  local total_seconds=$1
  local days=$(( total_seconds / 86400 ))
  local hours=$(( (total_seconds % 86400) / 3600 ))
  local minutes=$(( (total_seconds % 3600) / 60 ))
  echo "${days} days ${hours} hours ${minutes} minutes"
}

# Function to select emoji based on days
select_emoji() {
  local days=$1
  if (( days < 1 )); then
    echo "🌱"
  elif (( days < 3 )); then
    echo "🌿"
  elif (( days < 7 )); then
    echo "🌳"
  else
    echo "🌲"
  fi
}

# Main execution
main() {
  if [[ ! -r /proc/uptime ]]; then
    echo "Cannot read /proc/uptime"
    exit 1
  fi
  # First field is total seconds
  local uptime_seconds=$(awk '{print int($1)}' /proc/uptime)
  local human=$(format_uptime "$uptime_seconds")
  local days=$(( uptime_seconds / 86400 ))
  local emoji=$(select_emoji "$days")
  echo "System uptime: $human $emoji"
}

# If script is executed (not sourced), run main
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
