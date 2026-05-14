#!/usr/bin/env bash

# nightly-uptime-emoji-report
# Reads system uptime and prints an emoji status.
# Optional environment variable UPTIME_FILE can point to a file containing the same format as /proc/uptime for testing.

# Default to /proc/uptime if no override is provided
UPTIME_SOURCE="${UPTIME_FILE:-/proc/uptime}"

# Ensure the source exists and is readable
if [[ ! -r "$UPTIME_SOURCE" ]]; then
  echo "Error: Cannot read uptime source '$UPTIME_SOURCE'" >&2
  exit 1
fi

# Extract the first field (seconds) from the uptime file
# The file format is: "<seconds> <idle_seconds>"
UPTIME_SECONDS=$(awk '{print $1}' "$UPTIME_SOURCE")

# Guard against non‑numeric values
if ! [[ "$UPTIME_SECONDS" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
  echo "Error: Invalid uptime format in '$UPTIME_SOURCE'" >&2
  exit 1
fi

# Convert to integer seconds for comparison
UPTIME_SECONDS_INT=${UPTIME_SECONDS%.*}

# Determine the appropriate emoji and human‑readable time
if (( UPTIME_SECONDS_INT >= 86400 )); then
  # 1 day or more
  DAYS=$(( UPTIME_SECONDS_INT / 86400 ))
  echo "🟢 System uptime: $DAYS day(s)"
elif (( UPTIME_SECONDS_INT >= 21600 )); then
  # 6 hours to less than 1 day
  HOURS=$(( UPTIME_SECONDS_INT / 3600 ))
  echo "🟡 System uptime: $HOURS hour(s)"
else
  # Less than 6 hours
  MINUTES=$(( UPTIME_SECONDS_INT / 60 ))
  echo "🔴 System uptime: $MINUTES minute(s)"
fi
