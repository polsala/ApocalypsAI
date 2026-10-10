#!/usr/bin/env bash
# nightly-disk-guardian
# Checks root filesystem usage and prints whimsical messages.

# Configurable threshold (percentage)
THRESHOLD=${THRESHOLD:-80}

# Function to get usage percent
get_usage() {
  if [[ -n "$MOCK_DF_OUTPUT" ]]; then
    echo "$MOCK_DF_OUTPUT" | awk 'NR==2 {gsub("%","",$5); print $5}'
  else
    df -h / | awk 'NR==2 {gsub("%","",$5); print $5}'
  fi
}

usage=$(get_usage)

if [[ -z "$usage" ]]; then
  echo "Unable to determine disk usage."
  exit 2
fi

if (( usage >= THRESHOLD )); then
  cat <<EOF
   _____  _               _   _                 
  |  __ \| |             | | (_)                
  | |  | | |__   ___  ___| |_ _  ___  _ __  ___ 
  | |  | | '_ \ / _ \/ __| __| |/ _ \| '_ \/ __|
  | |__| | | | |  __/ (__| |_| | (_) | | | \__ \
  |_____/|_| |_|\___|\___|\__|_|\___/|_| |_|___/
                                                 
  WARNING: Disk usage is ${usage}% (threshold ${THRESHOLD}%)
EOF
  exit 1
else
  cat <<EOF
   _____                 _ 
  / ____|               | |
 | (___   ___  _ __ ___ | |
  \___ \ / _ \| '_ ` _ \| |
  ____) | (_) | | | | | | |
 |_____/ \___/|_| |_| |_|_|
                           
  All clear! Disk usage is ${usage}% (threshold ${THRESHOLD}%)
EOF
  exit 0
fi
