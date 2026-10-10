#!/usr/bin/env bash
# nightly-disk-guardian – monitor root filesystem usage and warn with ASCII art
#
# Usage: nightly-disk-guardian [THRESHOLD]
#        nightly-disk-guardian --mock-output "<df output>"
#
# THRESHOLD – integer percent (default 80)
# --mock-output – for testing; supplies df output via argument instead of calling df

set -euo pipefail

# Default threshold
THRESHOLD=80
MOCK_OUTPUT=""

# Parse arguments
while (( "$#" )); do
  case "$1" in
    --mock-output)
      MOCK_OUTPUT="$2"
      shift 2
      ;;
    *)
      if [[ "$1" =~ ^[0-9]+$ ]]; then
        THRESHOLD="$1"
        shift
      else
        echo "Invalid argument: $1" >&2
        exit 2
      fi
      ;;
  esac
done

# Function to obtain df output (real or mocked)
get_df_output() {
  if [[ -n "$MOCK_OUTPUT" ]]; then
    echo -e "$MOCK_OUTPUT"
  else
    df -h / || { echo "Failed to run df" >&2; exit 2; }
  fi
}

# Extract the usage percentage for the root mount point
USAGE=$(get_df_output | awk 'NR==2 {print $5}' | tr -d '%')

# Compare against threshold
if (( USAGE >= THRESHOLD )); then
  cat <<'EOF'
   _____  _               _   _                 _ 
  |  __ \| |             | | (_)               | |
  | |  | | |__   ___  ___| |_ _  ___  _ __  ___| |
  | |  | | '_ \ / _ \/ __| __| |/ _ \| '_ \/ __| |
  | |__| | | | |  __/ (__| |_| | (_) | | | \__ \_|
  |_____/|_| |_|\___|\___|\__|_|\___/|_| |_|___(_)

  WARNING: Disk usage is at ${USAGE}% (threshold: ${THRESHOLD}%).
  Consider cleaning up files or expanding storage.
EOF
  exit 1
else
  cat <<'EOF'
   _____                 _   _                 
  / ____|               | | (_)                
 | (___   ___  _ __ ___ | |_ _  ___  _ __  ___ 
  \___ \ / _ \| '_ ` _ \| __| |/ _ \| '_ \/ __|
  ____) | (_) | | | | | | |_| | (_) | | | \__ \
 |_____/ \___/|_| |_| |_|\__|_|\___/|_| |_|___/

  All clear! Disk usage is at ${USAGE}% (below ${THRESHOLD}%).
EOF
  exit 0
fi
