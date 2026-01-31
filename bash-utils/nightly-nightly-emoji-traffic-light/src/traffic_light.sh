#!/usr/bin/env bash
# nightly-emoji-traffic-light
# Reads load average and prints traffic‑light emoji status.

# Allow overrides for testing
LOADAVG_FILE="${LOADAVG_FILE:-/proc/loadavg}"
CPU_COUNT="${CPU_COUNT:-$(nproc)}"

# Read first field (1‑minute load)
if ! read -r load _ < "$LOADAVG_FILE"; then
  echo "Error: cannot read $LOADAVG_FILE" >&2
  exit 1
fi

# Compute load per CPU (rounded to two decimals)
load_per_cpu=$(awk -v l="$load" -v c="$CPU_COUNT" 'BEGIN { printf "%.2f", l / c }')

# Determine status
if (( $(awk "BEGIN {print ($load_per_cpu < 0.5)}") )); then
  emoji="🟢"
  level="low"
elif (( $(awk "BEGIN {print ($load_per_cpu >= 0.5 && $load_per_cpu <= 1.0)}") )); then
  emoji="🟡"
  level="moderate"
else
  emoji="🔴"
  level="high"
fi

printf "Load: %s (per CPU: %s) - Status: %s (%s)\n" "$load" "$load_per_cpu" "$emoji" "$level"
