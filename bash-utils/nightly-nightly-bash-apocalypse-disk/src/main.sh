#!/usr/bin/env bash
set -euo pipefail

# -------------------------------------------------------------------
# nightly-bash-apocalypse-disk-alert
# -------------------------------------------------------------------
# Checks disk usage and prints an apocalypse‑themed warning if any
# partition exceeds the defined THRESHOLD (default 80%).
# -------------------------------------------------------------------

# Configurable usage threshold (percentage)
THRESHOLD=80

# Array of dramatic apocalypse phrases (zero‑based indexing)
APOC_PHRASES=(
  "The heavens crack!"
  "Rocks tumble!"
  "The seas rise!"
  "Fire engulfs the lands!"
  "Shadows lengthen!"
  "The winds howl!"
  "Stars fall!"
  "The ground shakes!"
  "Silence before the storm!"
  "Doom approaches!"
)

# Gather df output (only the target and usage columns). The '--output'
# flag ensures a stable column order across platforms.
# 'tail -n +2' skips the header line.
df_output=$(df -h --output=target,pcent | tail -n +2)

alert=false
while read -r target pcent; do
  # Strip the trailing '%' from the usage column
  usage=${pcent%\%}
  if [[ $usage -ge $THRESHOLD ]]; then
    alert=true
    break
  fi
done <<< "$df_output"

if $alert; then
  # Deterministic selection when RANDOM is preset (useful for tests)
  idx=$((RANDOM % ${#APOC_PHRASES[@]}))
  echo "${APOC_PHRASES[$idx]}"
else
  echo "All clear. No apocalypse imminent."
fi
