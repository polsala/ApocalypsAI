#!/usr/bin/env bash

# nightly-uptime-epic-story
# Transforms system uptime into a whimsical epic narrative.
#
# Environment variables for customization (useful for testing):
#   UPTIME_MOCK  – If set, its value is used instead of reading /proc/uptime.
#   STORY_INDEX  – Zero‑based index to select a specific story template.

# Retrieve uptime information
if [[ -n "$UPTIME_MOCK" ]]; then
  uptime_output="$UPTIME_MOCK"
else
  # Prefer /proc/uptime; fallback to `uptime -p` (which has a different format)
  if [[ -r /proc/uptime ]]; then
    uptime_output=$(cat /proc/uptime)
  else
    # `uptime -p` returns a human‑readable string like "up 1 day, 2 hours"
    # Convert it to seconds approximation (not needed for our simple demo)
    echo "Unable to read /proc/uptime and no mock provided" >&2
    exit 1
  fi
fi

# Extract the first number (seconds) and truncate to integer
seconds=$(awk '{print int($1)}' <<<"$uptime_output")

# Compute days, hours, minutes
days=$((seconds / 86400))
hours=$(((seconds % 86400) / 3600))
minutes=$(((seconds % 3600) / 60))

# Story templates (feel free to add more)
templates=(
  "In the wastelands of silicon, this server has endured for %d days, %d hours, and %d minutes, defying the digital decay."
  "The ancient hum of circuits whispers: %d days, %d hours, %d minutes have passed since its birth."
  "Behold! %d days, %d hours, and %d minutes of relentless uptime, a beacon in the void."
)

# Choose template index
if [[ -n "$STORY_INDEX" ]]; then
  idx=$((STORY_INDEX % ${#templates[@]}))
else
  idx=0
fi

# Output the story
printf "${templates[$idx]}\n" "$days" "$hours" "$minutes"
