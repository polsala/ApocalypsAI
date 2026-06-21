#!/usr/bin/env bash
set -euo pipefail

# Determine the source of uptime information. By default this is /proc/uptime,
# but it can be overridden with the UPTIME_FILE environment variable (useful for testing).
UPTIME_FILE="${UPTIME_FILE:-/proc/uptime}"

if [[ ! -r "$UPTIME_FILE" ]]; then
  echo "Cannot read uptime file: $UPTIME_FILE" >&2
  exit 1
fi

# Extract the first field (seconds) and truncate to an integer.
uptime_seconds=$(awk '{print int($1)}' "$UPTIME_FILE")
# Convert seconds to whole days.
uptime_days=$(( uptime_seconds / 86400 ))

# Choose an emoji based on the number of days.
if (( uptime_days < 1 )); then
  emoji="🌱"
elif (( uptime_days < 7 )); then
  emoji="🌿"
else
  emoji="🌳"
fi

# Print a friendly message.
printf "Uptime: %d days %s\n" "$uptime_days" "$emoji"
