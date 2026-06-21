#!/usr/bin/env bash
# nightly-uptime-emoji-report
# Reads system uptime and prints an emoji with a friendly message.

# If an argument is supplied, treat it as uptime in seconds (for testing).
if [[ $# -gt 0 ]]; then
  uptime_seconds=$1
else
  if [[ -f /proc/uptime ]]; then
    # Extract the first field (seconds) and truncate to integer.
    uptime_seconds=$(awk '{print int($1)}' /proc/uptime)
  else
    echo "Cannot determine uptime: /proc/uptime not found" >&2
    exit 1
  fi
fi

# Determine emoji and message based on uptime.
if (( uptime_seconds < 3600 )); then
  emoji="☕️"
  msg="System just woke up! Time for coffee."
elif (( uptime_seconds < 86400 )); then
  emoji="🚀"
  msg="System is cruising."
else
  emoji="🛌"
  msg="System has been up a long time, maybe a nap?"
fi

# Output the result.
echo "$emoji $msg"
