#!/usr/bin/env bash
# nightly-mem-guardian
# Checks memory usage and prints a whimsical status.

set -euo pipefail

MEMINFO="${1:-/proc/meminfo}"

if [[ ! -f "$MEMINFO" ]]; then
  echo "Error: meminfo file '$MEMINFO' not found." >&2
  exit 1
fi

# Extract values in kB
mem_total_kb=$(grep -i '^MemTotal:' "$MEMINFO" | awk '{print $2}')
mem_available_kb=$(grep -i '^MemAvailable:' "$MEMINFO" | awk '{print $2}')

if [[ -z "$mem_available_kb" ]]; then
  # Fallback to MemFree if MemAvailable missing
  mem_available_kb=$(grep -i '^MemFree:' "$MEMINFO" | awk '{print $2}')
fi

# Guard against missing values
if [[ -z "$mem_total_kb" || -z "$mem_available_kb" ]]; then
  echo "Error: Unable to parse memory info." >&2
  exit 1
fi

# Calculate free percentage (rounded)
free_percent=$(( (mem_available_kb * 100) / mem_total_kb ))

# Human readable MB
mem_total_mb=$(( mem_total_kb / 1024 ))
mem_available_mb=$(( mem_available_kb / 1024 ))

echo "Memory Total: ${mem_total_mb} MB"
echo "Memory Free : ${mem_available_mb} MB (${free_percent}%)"

if (( free_percent >= 30 )); then
  echo "Your system is as fresh as a morning breeze! 🌬️"
else
  echo "Your memory is feeling cramped, consider closing some apps. 🐢"
fi
