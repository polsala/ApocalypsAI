#!/usr/bin/env bash

# disk_guardian.sh - monitor root disk usage and emit whimsical warnings

# Default threshold (percentage) can be overridden via first positional argument
THRESHOLD=${1:-80}

# Get usage percent of the root filesystem using POSIX‑compatible output
USAGE=$(df -P / | awk 'NR==2 {print $5}' | tr -d '%')

# Array of apocalyptic messages
MESSAGES=(
    "The sky darkens as the bytes overflow."
    "Rocks tumble, but your files remain."
    "The servers scream, yet you stand firm."
    "A meteor of data approaches!"
    "Your disk is a ticking time bomb."
)

if [[ "$USAGE" -ge "$THRESHOLD" ]]; then
    # Pick a random message
    IDX=$((RANDOM % ${#MESSAGES[@]}))
    echo "[WARN] Disk usage at ${USAGE}% – ${MESSAGES[$IDX]}"
    exit 1
else
    echo "[OK] Disk usage at ${USAGE}% – the world is still safe."
    exit 0
fi
