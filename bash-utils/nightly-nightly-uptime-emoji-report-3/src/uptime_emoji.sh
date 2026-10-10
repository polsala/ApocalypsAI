#!/usr/bin/env bash
set -euo pipefail

# Optional overrides for testing
if [[ -n "${UPTIME_SECONDS:-}" ]]; then
  uptime_seconds=$UPTIME_SECONDS
else
  uptime_seconds=$(cut -d' ' -f1 /proc/uptime)
fi

# Strip fractional part
uptime_seconds=${uptime_seconds%.*}

# Convert seconds to days, hours, minutes
days=$(( uptime_seconds / 86400 ))
hours=$(( (uptime_seconds % 86400) / 3600 ))
minutes=$(( (uptime_seconds % 3600) / 60 ))

# Load average (1‑minute)
if [[ -n "${LOADAVG_1:-}" ]]; then
  load1=$LOADAVG_1
else
  load1=$(cut -d' ' -f1 /proc/loadavg)
fi

# Number of CPU cores (allow override for deterministic tests)
if [[ -n "${CORES_OVERRIDE:-}" ]]; then
  cores=$CORES_OVERRIDE
else
  cores=$(nproc)
fi

# Determine thresholds
threshold_low=$(awk "BEGIN {print $cores * 0.5}")
threshold_high=$cores

# Choose emoji based on load
if (( $(awk "BEGIN {print ($load1 < $threshold_low)}") )); then
  emoji="🌞"
elif (( $(awk "BEGIN {print ($load1 < $threshold_high)}") )); then
  emoji="🌤"
else
  emoji="🌩"
fi

printf "Uptime: %d days, %d hours, %d minutes. Load: %.2f %s\n" "$days" "$hours" "$minutes" "$load1" "$emoji"
