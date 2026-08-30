#!/usr/bin/env bash
# nightly‑disk‑usage‑emoji‑report
# Prints `df -h` with an emoji indicating free‑space health.

set -euo pipefail

# Determine target mount point (default: /)
TARGET="${1:-/}"

# If DF_MOCK is set, use it instead of calling df – this makes testing deterministic.
if [[ -n "${DF_MOCK:-}" ]]; then
  DF_OUTPUT="$DF_MOCK"
else
  DF_OUTPUT=$(df -h "$TARGET")
fi

# Function to map free‑space percentage to an emoji
map_emoji() {
  local used_percent=$1   # e.g., "23%"
  # Strip the trailing % and convert to integer
  local used=${used_percent%%%}
  local free=$((100 - used))
  if (( free >= 80 )); then
    echo "🟢"
  elif (( free >= 50 )); then
    echo "🟡"
  else
    echo "🔴"
  fi
}

# Print header line unchanged
header=$(echo "$DF_OUTPUT" | head -n1)
printf "%s  EMOJI\n" "$header"

# Process each subsequent line
echo "$DF_OUTPUT" | tail -n +2 | while read -r line; do
  # Collapse multiple spaces to a single space for easier splitting
  line=$(echo "$line" | tr -s ' ')
  # Split into fields: Filesystem Size Used Avail Use% Mounted_on
  # Using awk to extract the Use% column (5th) and the whole line
  use_percent=$(echo "$line" | awk '{print $5}')
  emoji=$(map_emoji "$use_percent")
  printf "%s  %s\n" "$line" "$emoji"
done
