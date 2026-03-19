#!/usr/bin/env bash
set -euo pipefail

# Function to get uptime seconds
get_uptime_seconds() {
  if [[ -n "${UPTIME_MOCK:-}" ]]; then
    echo "$UPTIME_MOCK"
    return
  fi
  if [[ -r /proc/uptime ]]; then
    awk '{print $1}' /proc/uptime
    return
  fi
  echo "Error: Cannot read /proc/uptime and no UPTIME_MOCK provided." >&2
  exit 1
}

seconds=$(get_uptime_seconds)
# Convert to integer seconds (strip decimal)
seconds=${seconds%.*}
hours=$(( seconds / 3600 ))

if (( hours < 24 )); then
  echo "🌱 System uptime: ${hours}h – Fresh and ready!"
elif (( hours < 72 )); then
  echo "🌤 System uptime: ${hours}h – Running smoothly."
else
  echo "🔥 System uptime: ${hours}h – Time to consider a reboot."
fi
