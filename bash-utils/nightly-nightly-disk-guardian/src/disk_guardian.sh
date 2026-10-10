#!/usr/bin/env bash

# Disk Guardian – warns when disk usage exceeds a threshold.
# Usage: disk_guardian.sh [threshold]
# If the environment variable DF_OUTPUT is set, its value is used as mock df output for testing.

set -euo pipefail

THRESHOLD="${1:-80}"

# Obtain df line for the root filesystem
if [[ -n "${DF_OUTPUT:-}" ]]; then
  DF_LINE="${DF_OUTPUT}"
else
  DF_LINE=$(df -h / | awk 'NR==2')
fi

# Extract the usage percent (e.g., 78%)
USAGE=$(echo "$DF_LINE" | awk '{print $5}' | tr -d '%')

if [[ -z "$USAGE" ]]; then
  echo "Failed to parse disk usage."
  exit 2
fi

if (( USAGE >= THRESHOLD )); then
  echo "⚠️  Disk usage is at ${USAGE}% – time to clean up!"
  cat <<'ART'
   ____
  / ___)   ___  _   _ _ __ ___   ___
 | |      / _ \| | | | '_ ` _ \ / _ \
 | |___  | (_) | |_| | | | | | |  __/
  \____)  \___/ \__,_|_| |_| |_|\___|
ART
  exit 1
else
  echo "Disk usage is at ${USAGE}% – all clear."
  exit 0
fi
