#!/usr/bin/env bash

# Disk Guardian: checks disk usage and prints whimsical warning if above threshold.
# Usage: disk_guardian.sh <path> [threshold]
#   <path>      – directory or mount point to inspect (default: /)
#   [threshold] – usage percent that triggers a warning (default: 80)

set -euo pipefail

# Default arguments
TARGET="${1:-/}"
THRESHOLD="${2:-80}"

# Allow overriding the df command for testing (e.g., mock function)
DF_CMD="${DF_CMD:-df}"

# Retrieve usage percent for the target mount point
# Using POSIX output (-P) and extracting the 5th column (e.g., "20%")
usage=$($DF_CMD -P "$TARGET" | awk 'NR==2 {print $5}' | tr -d '%')

if [[ -z "$usage" ]]; then
  echo "Error: Could not determine disk usage for $TARGET" >&2
  exit 1
fi

if (( usage < THRESHOLD )); then
  echo "✅ Disk usage at ${usage}% is below threshold (${THRESHOLD}%). All clear."
  exit 0
fi

# Whimsical warning messages
messages=(
  "⚠️ The disk is feeling a bit cramped, like a sardine in a tin!"
  "🚨 Space is scarce, the bytes are staging a protest!"
  "🛑 Warning: Your storage is on a diet, but it's starving!"
  "💥 Disk overload! The data elves are taking a coffee break."
  "🔔 Alert! The filesystem is shouting, 'I need more room!'"
)

# Pick a random message
RANDOM_INDEX=$(( RANDOM % ${#messages[@]} ))
echo "${messages[$RANDOM_INDEX]} (Usage: ${usage}%, Threshold: ${THRESHOLD}%)"

exit 0
