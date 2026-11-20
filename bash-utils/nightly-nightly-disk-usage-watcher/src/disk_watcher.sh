#!/usr/bin/env bash
set -euo pipefail

# Default threshold percentage
THRESHOLD="${THRESHOLD:-80}"

# Function to get df output (real or mock)
get_df_output() {
  if [[ -n "${DF_MOCK_FILE:-}" && -f "$DF_MOCK_FILE" ]]; then
    cat "$DF_MOCK_FILE"
  else
    df -h /
  fi
}

# Extract usage percent (e.g., "85%")
usage=$(get_df_output | awk 'NR==2 {print $5}' | tr -d '%')

# Compare usage with threshold
if (( usage > THRESHOLD )); then
  cat <<EOF
   _____  _                     _ 
  / ____|| |                   | |
 | (___  | |__    ___  _ __ ___| |
  \___ \ | '_ \  / _ \| '__/ _ \ |
  ____) || | | ||  __/| | |  __/ |
 |_____/ |_| |_| \___||_|  \___|_|
                                 
WARNING: Disk usage is ${usage}% (threshold ${THRESHOLD}%)
EOF
  exit 1
else
  echo "✅ Disk usage is ${usage}% – all clear!"
  exit 0
fi
