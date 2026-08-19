#!/usr/bin/env bash

# nightly-disk-usage-alert
# Monitors disk usage and warns if any mount point exceeds a given threshold.
# Usage: ./disk-usage-alert.sh [threshold]
#   threshold – integer percent (default 80)

THRESHOLD=${1:-80}
EXIT_CODE=0

# Use df -hP for a predictable, parsable format (POSIX compliant)
while IFS= read -r line; do
  # Skip header line
  if [[ $line == Filesystem* ]]; then
    continue
  fi
  # Extract usage percent and mount point
  usage=$(echo "$line" | awk '{print $5}' | tr -d '%')
  mount=$(echo "$line" | awk '{print $6}')
  if (( usage > THRESHOLD )); then
    echo "Warning: $mount is ${usage}% full (threshold ${THRESHOLD}%)"
    EXIT_CODE=1
  fi
done < <(df -hP)

exit $EXIT_CODE
