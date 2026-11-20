#!/usr/bin/env bash
# nightly-disk-usage-emoji-alert
# Scans `df -h` output and prints emoji‑enhanced usage warnings.

set -euo pipefail

# Default threshold (percentage) for red warning
DEFAULT_THRESHOLD=80

# Function to print usage information
usage() {
  echo "Usage: $(basename "$0") [threshold]"
  echo "  threshold   Optional integer (1-100) for usage percent that triggers a red warning. Default is ${DEFAULT_THRESHOLD}."
  exit 1
}

# Validate optional argument
if [[ "${1-}" == "-h" || "${1-}" == "--help" ]]; then
  usage
fi

THRESHOLD=${1:-$DEFAULT_THRESHOLD}
if ! [[ "$THRESHOLD" =~ ^[0-9]+$ ]] || (( THRESHOLD < 1 || THRESHOLD > 100 )); then
  echo "Error: threshold must be an integer between 1 and 100." >&2
  usage
fi

# Read df output: if stdin is not a terminal, use it; otherwise call df -h
if [ -t 0 ]; then
  DF_OUTPUT=$(df -hP)
else
  DF_OUTPUT=$(cat)
fi

# Process each line after the header
echo "$DF_OUTPUT" | tail -n +2 | while read -r line; do
  # df -hP guarantees space‑separated columns, even for mounted on spaces (escaped with \040)
  # Columns: Filesystem Size Used Avail Use% Mounted_on
  filesystem=$(echo "$line" | awk '{print $1}')
  size=$(echo "$line" | awk '{print $2}')
  used=$(echo "$line" | awk '{print $3}')
  avail=$(echo "$line" | awk '{print $4}')
  usepct=$(echo "$line" | awk '{print $5}' | tr -d '%')
  mount=$(echo "$line" | awk '{print $6}')

  if (( usepct >= THRESHOLD )); then
    emoji="🔴"
  else
    emoji="🟢"
  fi

  printf "%s %s %s %s %s%% %s\n" "$emoji" "$filesystem" "$size" "$used" "$usepct" "$mount"
done
