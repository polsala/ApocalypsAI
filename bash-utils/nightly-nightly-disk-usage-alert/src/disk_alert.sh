#!/usr/bin/env bash
set -euo pipefail

# Default threshold percentage
THRESHOLD="${THRESHOLD:-80}"

# Get df output: either from env var or real command
if [[ -n "${DISK_USAGE_OUTPUT:-}" ]]; then
  df_output="${DISK_USAGE_OUTPUT}"
else
  df_output="$(df -h / 2>/dev/null || true)"
fi

# Extract the usage percentage from the second line, 5th column
usage_line=$(echo "$df_output" | tail -n +2 | head -n 1)
if [[ -z "$usage_line" ]]; then
  echo "Error: unable to get disk usage information." >&2
  exit 2
fi

# Use awk to get the 5th field (e.g., 45%)
usage_percent=$(echo "$usage_line" | awk '{print $5}')
if [[ -z "$usage_percent" ]]; then
  echo "Error: unable to parse usage percentage." >&2
  exit 2
fi

# Strip trailing %
usage_number=${usage_percent%\%}

# Validate numeric
if ! [[ "$usage_number" =~ ^[0-9]+$ ]]; then
  echo "Error: non‑numeric usage value '$usage_percent'." >&2
  exit 2
fi

if (( usage_number >= THRESHOLD )); then
  echo "Warning: disk usage is ${usage_number}% (threshold ${THRESHOLD}%)."
  exit 1
else
  echo "OK: disk usage is ${usage_number}% (threshold ${THRESHOLD}%)."
  exit 0
fi
