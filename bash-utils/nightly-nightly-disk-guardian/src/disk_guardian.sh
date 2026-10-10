#!/usr/bin/env bash

set -euo pipefail

# Default threshold (percentage) if not supplied as first argument
THRESHOLD="${1:-80}"
# Optional path to a file containing df output (used for testing)
DF_FILE="${2:-}"

function get_df_output() {
  if [[ -n "$DF_FILE" ]]; then
    cat "$DF_FILE"
  else
    df -h
  fi
}

function check_usage() {
  local warn=0
  while IFS= read -r line; do
    # Skip header line
    if [[ "$line" == Filesystem* ]]; then
      continue
    fi
    # Extract usage percent (e.g., 85%) and mount point
    usage=$(echo "$line" | awk '{print $5}' | tr -d '%')
    mount=$(echo "$line" | awk '{print $6}')
    if (( usage > THRESHOLD )); then
      echo "⚠️  $mount is ${usage}% full – time to clean up!"
      warn=1
    fi
  done < <(get_df_output)
  return $warn
}

check_usage
