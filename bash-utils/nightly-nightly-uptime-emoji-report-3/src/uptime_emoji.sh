#!/usr/bin/env bash
# nightly-uptime-emoji-report

# Function to get uptime seconds; can be overridden for testing
get_uptime_seconds() {
  if [[ -n "$MOCK_UPTIME_SECONDS" ]]; then
    echo "$MOCK_UPTIME_SECONDS"
  else
    # /proc/uptime first field is seconds with fractions
    awk '{print int($1)}' /proc/uptime
  fi
}

seconds=$(get_uptime_seconds)

# Calculate days, hours, minutes
days=$((seconds / 86400))
hours=$(((seconds % 86400) / 3600))
minutes=$(((seconds % 3600) / 60))

# Choose emoji
if (( seconds < 86400 )); then
  emoji="🌱"
elif (( seconds < 604800 )); then
  emoji="🌿"
else
  emoji="🌳"
fi

printf "Uptime: %d days, %d hours, %d minutes %s\n" "$days" "$hours" "$minutes" "$emoji"
