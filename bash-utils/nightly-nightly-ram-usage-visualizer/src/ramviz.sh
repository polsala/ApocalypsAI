#!/usr/bin/env bash
# nightly-ram-usage-visualizer
# Reads /proc/meminfo (or a provided file) and prints RAM usage as a bar graph.

MEMINFO="${1:-/proc/meminfo}"

if [[ ! -r "$MEMINFO" ]]; then
  echo "Cannot read $MEMINFO" >&2
  exit 1
fi

# Extract MemTotal and MemAvailable (kB)
TOTAL=$(grep -i '^MemTotal:' "$MEMINFO" | awk '{print $2}')
AVAILABLE=$(grep -i '^MemAvailable:' "$MEMINFO" | awk '{print $2}')

if [[ -z "$TOTAL" || -z "$AVAILABLE" ]]; then
  echo "Failed to parse meminfo" >&2
  exit 1
fi

USED=$((TOTAL - AVAILABLE))
PERCENT=$(( (USED * 100) / TOTAL ))

# Bar of length 20
BAR_LENGTH=20
FILLED=$(( (PERCENT * BAR_LENGTH) / 100 ))
EMPTY=$(( BAR_LENGTH - FILLED ))
FILLED_BAR=$(printf '█%.0s' $(seq 1 $FILLED))
EMPTY_BAR=$(printf '─%.0s' $(seq 1 $EMPTY))

echo "RAM Usage: $PERCENT% [$FILLED_BAR$EMPTY_BAR]"

if (( PERCENT > 80 )); then
  QUOTES=(
    "Stay cool, the memory will recover."
    "Time for a reboot? Maybe."
    "Your system is thirsty for RAM."
    "Consider closing some tabs."
  )
  INDEX=$(( RANDOM % ${#QUOTES[@]} ))
  echo "${QUOTES[$INDEX]}"
fi
