#!/usr/bin/env bash

# nightly-uptime-chronicle
# Turns system uptime into a whimsical story.
# If a numeric argument is supplied, it is interpreted as the uptime in seconds (for testing).

set -euo pipefail

# Function to compute days, hours, minutes from seconds
human_readable_uptime() {
  local total_seconds=$1
  local days=$(( total_seconds / 86400 ))
  local hours=$(( (total_seconds % 86400) / 3600 ))
  local minutes=$(( (total_seconds % 3600) / 60 ))
  echo "${days} day$( [ $days -ne 1 ] && echo s ), ${hours} hour$( [ $hours -ne 1 ] && echo s ), and ${minutes} minute$( [ $minutes -ne 1 ] && echo s )"
}

# Determine uptime in seconds
if [[ $# -ge 1 && $1 =~ ^[0-9]+$ ]]; then
  uptime_seconds=$1
else
  # Read the first field from /proc/uptime (seconds with fractions), truncate to integer
  uptime_seconds=$(awk '{print int($1)}' /proc/uptime)
fi

# Build the story
uptime_phrase=$(human_readable_uptime "$uptime_seconds")

# Choose a random whimsical suffix from a small list (deterministic for testing when SEED is set)
suffixes=(
  "bravely weathering countless coffee spills."
  "defying the odds of nightly reboots."
  "standing tall amidst endless log churn."
  "surviving the relentless ping of monitoring tools."
  "outlasting the last forgotten cron job."
)

# Allow deterministic selection via optional environment variable UPTIME_CHRONICLE_SEED
if [[ -n "${UPTIME_CHRONICLE_SEED:-}" ]]; then
  seed=$UPTIME_CHRONICLE_SEED
else
  # Use current nanoseconds as seed
  seed=$(date +%s%N)
fi
index=$(( seed % ${#suffixes[@]} ))
selected_suffix=${suffixes[$index]}

# Output the story
printf "Your server has survived %s, %s\n" "$uptime_phrase" "$selected_suffix"
