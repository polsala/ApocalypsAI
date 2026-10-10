#!/usr/bin/env bash

set -euo pipefail

# Default threshold is 80% if not provided
THRESHOLD="${1:-80}"

# Obtain df output either from the DF_OUTPUT env var (used for testing) or from the real system
if [[ -n "${DF_OUTPUT:-}" ]]; then
  DF_DATA="${DF_OUTPUT}"
else
  DF_DATA=$(df -h /)
fi

# Extract the usage percentage from the second line, fifth column (e.g., "50%")
USAGE=$(echo "$DF_DATA" | awk 'NR==2 {print $5}' | tr -d '%')

if [[ -z "$USAGE" ]]; then
  echo "ERROR: Unable to parse disk usage."
  exit 2
fi

if (( USAGE >= THRESHOLD )); then
  echo "ALERT: usage ${USAGE}% exceeds threshold ${THRESHOLD}%"
  exit 1
else
  echo "OK: usage ${USAGE}%"
  exit 0
fi
