#!/usr/bin/env bash
set -euo pipefail

# Get df output, either real or mocked
if [[ -n "${MOCK_DF:-}" ]]; then
  df_output="${MOCK_DF}"
else
  df_output="$(df -h /)"
fi

# Extract the Use% column for the root mount point
# Assume the line containing '/' as mount point
use_percent=$(echo "$df_output" | awk 'NR>1 && $NF=="/" {print $5}' | tr -d '%')

# Default to 0 if parsing fails
if [[ -z "$use_percent" ]]; then
  use_percent=0
fi

if (( use_percent < 80 )); then
  echo "🌞 All good! Disk usage is ${use_percent}% ."
else
  cat <<EOF
   .----.
  /      \
 |  .--.  |
 | ( () ) |
  \ '--' /
   '----'
⚠️  Warning: Disk usage is ${use_percent}%! Consider cleaning up.
EOF
fi
