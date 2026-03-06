#!/usr/bin/env bash
set -euo pipefail

# Default threshold (percentage) if not supplied as first argument
THRESHOLD=${1:-80}

# Function to retrieve `df` output. Allows injection of mock data via env var for testing.
get_df_output() {
  if [[ -n "${DISK_ALERT_DF_MOCK-}" ]]; then
    # Mock rationale: use provided mock data instead of calling the real `df` command.
    printf "%s" "$DISK_ALERT_DF_MOCK"
    return
  fi
  df -hP
}

# Process each line of `df` output, skipping the header.
while IFS= read -r line; do
  if [[ "$line" == Filesystem* ]]; then
    continue
  fi
  # Extract the usage percentage and mount point.
  usage=$(awk '{print $5}' <<<"$line")
  mount=$(awk '{print $6}' <<<"$line")
  usage_num=${usage%\%}
  if (( usage_num > THRESHOLD )); then
    echo "ALERT: $mount at ${usage_num}% usage"
  fi
done < <(get_df_output)
