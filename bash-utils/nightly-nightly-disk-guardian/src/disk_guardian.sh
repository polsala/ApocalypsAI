#!/usr/bin/env bash
set -euo pipefail

# Default threshold (percentage) if not supplied as argument
THRESHOLD=${1:-80}

# Allow injection of a mock df output for testing via DISK_DF_FILE
if [[ -n "${DISK_DF_FILE:-}" ]]; then
  DF_DATA=$(cat "$DISK_DF_FILE")
else
  DF_DATA=$(df -h /)
fi

# Extract the usage percent from the second line, fifth column (e.g., "75%")
USAGE=$(echo "$DF_DATA" | awk 'NR==2 {gsub("%","",$5); print $5}')

# Compare usage against threshold
if (( USAGE < THRESHOLD )); then
  echo "✅ Disk usage is $USAGE%, below threshold $THRESHOLD%."
  exit 0
fi

# Apocalyptic phrases pool
PHRASES=(
  "The heavens crack as your storage fills!"
  "Apocalypse imminent: disk full!"
  "Your data hoard summons the void!"
  "Beware! The bytes overflow!"
  "The server screams under the weight!"
)

RANDOM_INDEX=$(( RANDOM % ${#PHRASES[@]} ))
echo "⚠️ ${PHRASES[$RANDOM_INDEX]} (Usage: $USAGE% ≥ $THRESHOLD%)"
exit 1
