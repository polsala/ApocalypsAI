#!/usr/bin/env bash
# nightly-cpu-hunger-alert

# Default threshold is 80% if not provided
THRESHOLD=${1:-80}
# Allow overriding the stat file for testing
PROC_STAT=${PROC_STAT:-/proc/stat}

# Read the first line of the stat file
read -r cpu_line < "$PROC_STAT"
# Split into fields
read -a fields <<< "$cpu_line"
# Extract CPU times
user=${fields[1]}
nice=${fields[2]}
system=${fields[3]}
idle=${fields[4]}
iowait=${fields[5]}
irq=${fields[6]}
softirq=${fields[7]}
steal=${fields[8]}
# Compute total and usage
TOTAL=$((user + nice + system + idle + iowait + irq + softirq + steal))
USAGE=$(( (TOTAL - idle) * 100 / TOTAL ))

if (( USAGE > THRESHOLD )); then
  echo "CPU is feeling hungry! Current usage: ${USAGE}% (threshold ${THRESHOLD}%)"
  exit 1
else
  echo "CPU is calm. Current usage: ${USAGE}% (threshold ${THRESHOLD}%)"
  exit 0
fi
