#!/usr/bin/env bash
# nightly-disk-usage-watcher
# Scans disk usage and warns if usage exceeds THRESHOLD (default 80)

set -euo pipefail

# Default threshold
THRESHOLD="${THRESHOLD:-80}"

# Get df output, either from DF_MOCK (for tests) or real command
if [[ -n "${DF_MOCK:-}" ]]; then
  df_output="${DF_MOCK}"
else
  df_output="$(df -P)"
fi

# Initialize flag
exceeded=0

# Process each line except header
while IFS= read -r line; do
  # Skip header
  if [[ "$line" == Filesystem* ]]; then
    continue
  fi
  # Fields: Filesystem Size Used Avail Use% Mounted_on
  usage_percent=$(echo "$line" | awk '{print $5}' | tr -d '%')
  mount_point=$(echo "$line" | awk '{print $6}')
  if (( usage_percent > THRESHOLD )); then
    echo "Warning: ${mount_point} is at ${usage_percent}% usage (threshold ${THRESHOLD}%)"
    exceeded=1
  fi
done <<< "$df_output"

exit $exceeded
