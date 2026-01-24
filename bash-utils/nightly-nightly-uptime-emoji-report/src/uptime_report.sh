#!/usr/bin/env bash

# nightly-uptime-emoji-report
# Reports system uptime with an emoji reflecting load average.

# Default file locations (can be overridden for testing)
UPTIME_FILE="/proc/uptime"
LOADAVG_FILE="/proc/loadavg"

# Parse command‑line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --uptime-file)
      UPTIME_FILE="$2"
      shift 2
      ;;
    --loadavg-file)
      LOADAVG_FILE="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

# Function to convert seconds to days, hours, minutes
seconds_to_dhms() {
  local total_seconds=$1
  local days=$(( total_seconds / 86400 ))
  local hours=$(( (total_seconds % 86400) / 3600 ))
  local minutes=$(( (total_seconds % 3600) / 60 ))
  echo "$days days, $hours hours, $minutes minutes"
}

# Read uptime (first field = seconds since boot)
if [[ ! -r "$UPTIME_FILE" ]]; then
  echo "Cannot read uptime file: $UPTIME_FILE" >&2
  exit 1
fi
UPTIME_SECONDS=$(awk '{print int($1)}' "$UPTIME_FILE")

# Read load average (first field = 1‑minute load)
if [[ ! -r "$LOADAVG_FILE" ]]; then
  echo "Cannot read loadavg file: $LOADAVG_FILE" >&2
  exit 1
fi
LOADAVG=$(awk '{print $1}' "$LOADAVG_FILE")

# Determine emoji based on load thresholds
if (( $(echo "$LOADAVG < 0.5" | bc -l) )); then
  EMOJI="😊"
elif (( $(echo "$LOADAVG < 1.5" | bc -l) )); then
  EMOJI="😐"
else
  EMOJI="😫"
fi

# Format uptime
UPTIME_STR=$(seconds_to_dhms "$UPTIME_SECONDS")

# Output result
printf "Uptime: %s – Load: %s %s\n" "$UPTIME_STR" "$LOADAVG" "$EMOJI"
