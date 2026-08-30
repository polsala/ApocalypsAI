#!/usr/bin/env bash

# nightly-uptime-emoji-reporter
# Reports system uptime with an emoji mood based on load average.

# Functions to retrieve uptime and load average.
# They first check for environment variables (used by tests) and fall back to reading /proc files.

get_uptime() {
  if [[ -n "$MOCK_UPTIME" ]]; then
    echo "$MOCK_UPTIME"
  else
    cat /proc/uptime
  fi
}

get_loadavg() {
  if [[ -n "$MOCK_LOADAVG" ]]; then
    echo "$MOCK_LOADAVG"
  else
    cat /proc/loadavg
  fi
}

# Convert uptime seconds to days, hours, minutes.
format_uptime() {
  local total_seconds=$1
  local days=$(( total_seconds / 86400 ))
  local hours=$(( (total_seconds % 86400) / 3600 ))
  local minutes=$(( (total_seconds % 3600) / 60 ))
  echo "${days} days, ${hours} hours, ${minutes} minutes"
}

# Determine emoji based on load per CPU (assumes 1 CPU for simplicity).
select_emoji() {
  local load=$1
  if (( $(awk "BEGIN {print ($load < 0.5)}") )); then
    echo "😊"
  elif (( $(awk "BEGIN {print ($load < 1.5)}") )); then
    echo "😐"
  else
    echo "😫"
  fi
}

main() {
  # Retrieve raw data.
  local uptime_raw=$(get_uptime)
  local loadavg_raw=$(get_loadavg)

  # Extract values.
  local uptime_seconds=$(awk '{print $1}' <<< "$uptime_raw")
  local load_one=$(awk '{print $1}' <<< "$loadavg_raw")

  # Format uptime.
  local formatted_uptime=$(format_uptime "${uptime_seconds%.*}")

  # Choose emoji.
  local mood=$(select_emoji "$load_one")

  echo "Uptime: $formatted_uptime - Mood: $mood"
}

# Execute when run directly.
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
