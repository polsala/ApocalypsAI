#!/usr/bin/env bash

# nightly-disk-guardian – watch root disk usage and emit apocalyptic warnings

# Default threshold (percentage) if not supplied
DEFAULT_THRESHOLD=80

# List of whimsical apocalypse‑themed warnings
QUOTES=(
  "The end is nigh! Beware the looming data deluge."
  "Your storage is swelling like a volcano – eruption imminent!"
  "Disk space apocalypse incoming – evacuate your files!"
  "The bytes are rising; the void watches."
  "Critical mass reached – the digital horizon darkens."
)

# Function to print usage information
usage() {
  echo "Usage: $0 [threshold]"
  echo "  threshold – optional integer 0‑100 (default $DEFAULT_THRESHOLD)"
  exit 1
}

# Parse optional argument
if [[ $# -gt 1 ]]; then
  usage
fi

THRESHOLD=${1:-$DEFAULT_THRESHOLD}

# Validate that THRESHOLD is an integer between 0 and 100
if ! [[ "$THRESHOLD" =~ ^[0-9]+$ ]] || (( THRESHOLD < 0 || THRESHOLD > 100 )); then
  echo "Error: threshold must be an integer between 0 and 100."
  usage
fi

# Retrieve the usage percentage for the root filesystem
# Expected format (example):
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sda1        50G   38G   10G  80% /
get_root_usage() {
  df -h / | awk 'NR==2 {print $5}' | tr -d '%'
}

USAGE=$(get_root_usage)

# Compare usage against threshold
if (( USAGE >= THRESHOLD )); then
  # Pick a random quote
  INDEX=$(( RANDOM % ${#QUOTES[@]} ))
  SELECTED="${QUOTES[$INDEX]}"
  echo -e "⚠️  Disk usage at ${USAGE}% – $SELECTED"
else
  echo "✅  Disk usage at ${USAGE}% – within safe limits."
fi
