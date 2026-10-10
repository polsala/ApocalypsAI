#!/usr/bin/env bash
# nightly-disk-guardian
# Checks disk usage and prints a whimsical warning if usage exceeds a threshold.

set -euo pipefail

# Default values
MOUNT_POINT="/"
THRESHOLD=80

# Parse arguments
if [[ $# -ge 1 ]]; then
  MOUNT_POINT="$1"
fi
if [[ $# -ge 2 ]]; then
  THRESHOLD="$2"
fi

# Function to get used percentage (without % sign)
get_usage() {
  if [[ -n "${DF_OUTPUT:-}" ]]; then
    # DF_OUTPUT should be like '45%'
    echo "${DF_OUTPUT}"
  else
    df -P "$MOUNT_POINT" | tail -1 | awk '{print $5}'
  fi
}

USAGE_STR=$(get_usage)
# Strip trailing %
USAGE=${USAGE_STR%\%}

if (( USAGE < THRESHOLD )); then
  exit 0
fi

# Array of apocalyptic warnings
WARNINGS=(
  "⚠️ The void is swallowing your disk! (${USAGE}% used)"
  "🔥 Your storage is on fire! (${USAGE}% used)"
  "☢️ Radiation levels rising in your filesystem (${USAGE}% used)"
  "🧟‍♂️ Zombies are crawling over your blocks (${USAGE}% used)"
  "🌪️ A data tornado approaches (${USAGE}% used)"
)

# Pick a random warning
RANDOM_INDEX=$(( RANDOM % ${#WARNINGS[@]} ))
echo "${WARNINGS[$RANDOM_INDEX]}" >&2
exit 1
