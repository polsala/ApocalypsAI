#!/usr/bin/env bash
# nightly-uptime-emoji-reporter
# Reports system uptime with a whimsical emoji.

set -euo pipefail

# Function to get uptime string (seconds idle)
get_uptime() {
  if [[ $# -eq 1 ]]; then
    echo "$1"
  else
    cat /proc/uptime
  fi
}

# Main logic
main() {
  local uptime_str
  uptime_str=$(get_uptime "$@")
  # uptime_str format: "<total_seconds> <idle_seconds>"
  local total_seconds
  total_seconds=$(awk '{print $1}' <<<"$uptime_str")
  # Convert to hours
  local total_hours
  total_hours=$(awk "BEGIN {printf \"%.2f\", $total_seconds/3600}")

  local emoji
  if (( $(awk "BEGIN {print ($total_seconds < 3600)}") )); then
    emoji="🚀"
  elif (( $(awk "BEGIN {print ($total_seconds < 6*3600)}") )); then
    emoji="🌱"
  elif (( $(awk "BEGIN {print ($total_seconds < 24*3600)}") )); then
    emoji="🐢"
  elif (( $(awk "BEGIN {print ($total_seconds < 7*24*3600)}") )); then
    emoji="🌞"
  else
    emoji="🌙"
  fi

  printf "Uptime: %.2f hours %s\n" "$total_hours" "$emoji"
}

main "$@"
