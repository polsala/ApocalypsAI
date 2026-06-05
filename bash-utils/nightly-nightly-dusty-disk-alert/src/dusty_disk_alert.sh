#!/usr/bin/env bash
set -euo pipefail

# nightly‑dusty‑disk‑alert
# Checks root filesystem usage and emits a whimsical warning if usage exceeds a threshold.
# Usage: ./dusty_disk_alert.sh [threshold_percent] [--mock]
#   threshold_percent: integer (default 80)
#   --mock: read df output from stdin instead of calling df (useful for testing)

# Default threshold
DEFAULT_THRESHOLD=80

# Parse arguments
THRESHOLD=${1:-$DEFAULT_THRESHOLD}
MOCK_FLAG=${2:-}

# Validate threshold is a number
if ! [[ "$THRESHOLD" =~ ^[0-9]+$ ]]; then
  echo "Error: Threshold must be an integer percentage." >&2
  exit 1
fi

# Obtain df output
if [[ "$MOCK_FLAG" == "--mock" ]]; then
  # Read from stdin (test mode)
  DF_OUTPUT=$(cat)
else
  DF_OUTPUT=$(df -h /)
fi

# Extract the used percentage (second line, 5th column)
USAGE=$(echo "$DF_OUTPUT" | awk 'NR==2 {print $5}' | tr -d '%')

# Ensure we got a numeric value
if ! [[ "$USAGE" =~ ^[0-9]+$ ]]; then
  echo "Error: Unable to parse disk usage." >&2
  exit 1
fi

# Compare usage against threshold
if (( USAGE >= THRESHOLD )); then
  PHRASES=(
    "The sky cracks as disks fill"
    "Apocalypse imminent: storage overflow"
    "Your server groans under the weight of data"
    "The void whispers: no more space"
    "Entropy rises as bytes pile up"
  )
  # Pick a random phrase
  IDX=$(( RANDOM % ${#PHRASES[@]} ))
  echo "⚠️ ${PHRASES[$IDX]} (${USAGE}% used)"
else
  echo "✅ All clear: ${USAGE}% used"
fi
