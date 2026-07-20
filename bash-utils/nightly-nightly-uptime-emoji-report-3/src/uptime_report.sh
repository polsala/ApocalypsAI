#!/usr/bin/env bash
# nightly-uptime-emoji-report
# Prints an emoji based on system uptime.

# If an argument is provided, use it as uptime seconds (for testing)
if [[ -n "$1" && "$1" =~ ^[0-9]+$ ]]; then
  uptime_seconds=$1
else
  # Read first field from /proc/uptime
  if [[ -r /proc/uptime ]]; then
    uptime_seconds=$(awk '{print int($1)}' /proc/uptime)
  else
    echo "Cannot read /proc/uptime"
    exit 1
  fi
fi

if (( uptime_seconds < 3600 )); then
  emoji="🚀"
  desc="just launched"
elif (( uptime_seconds < 86400 )); then
  emoji="🌞"
  desc="basking in the sun"
elif (( uptime_seconds < 604800 )); then
  emoji="🌤"
  desc="cloudy week"
else
  emoji="🐢"
  desc="steady as a turtle"
fi

echo "$emoji System uptime: $uptime_seconds seconds ($desc)"
