#!/usr/bin/env bash
set -euo pipefail

# Directory to analyze (default: current)
DIR="${1:-.}"

# Scale: 200 KB per 📦 emoji
SCALE=200

# If mock data is provided via DISK_USAGE_MOCK_DATA, use it; otherwise run du.
if [[ -n "${DISK_USAGE_MOCK_DATA:-}" ]]; then
  du_output="${DISK_USAGE_MOCK_DATA}"
else
  # Get size (KB) of each immediate subdirectory
  du_output=$(du -sk "${DIR}"/* 2>/dev/null | sort -nr)
fi

# Process each line: size<TAB>path
while IFS=$'\t' read -r size path; do
  # Calculate number of emojis
  count=$(( size / SCALE ))
  if (( count > 0 )); then
    emojis=$(printf '📦%.0s' $(seq 1 $count))
    echo "${path} ${emojis}"
  else
    echo "${path}"
  fi
done <<< "$du_output"
