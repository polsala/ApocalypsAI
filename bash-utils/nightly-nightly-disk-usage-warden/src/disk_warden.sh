#!/usr/bin/env bash
set -euo pipefail

# Optional argument: path to a file containing `df -h /` output.
# If omitted, the script runs `df -h /` on the live system.
DF_SOURCE="${1:-}"

if [[ -n "$DF_SOURCE" ]]; then
  DF_OUTPUT=$(cat "$DF_SOURCE")
else
  DF_OUTPUT=$(df -h /)
fi

# Extract the usage percentage from the second line.
usage=$(echo "$DF_OUTPUT" | awk 'NR==2 {print $5}' | tr -d '%')

if [[ -z "$usage" ]]; then
  echo "⚠️ Unable to determine disk usage."
  exit 1
fi

if (( usage >= 90 )); then
  echo "🚨 Critical: Disk usage at ${usage}%! Time to evacuate the data vault!"
elif (( usage >= 70 )); then
  echo "⚠️ Warning: Disk usage at ${usage}%. Consider cleaning up."
else
  echo "✅ All clear: Disk usage at ${usage}%."
fi
