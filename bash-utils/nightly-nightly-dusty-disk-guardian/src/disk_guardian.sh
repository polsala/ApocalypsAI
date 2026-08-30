#!/usr/bin/env bash
set -euo pipefail

# Default threshold (percentage)
THRESHOLD=${1:-80}

# Get usage percent of root filesystem
# Expected df output format (second line):
# /dev/root 100G 85G 15G 85% /
USAGE_LINE=$(df -h / | awk 'NR==2')
USAGE_PCT=$(echo "$USAGE_LINE" | awk '{print $5}' | tr -d '%')

# Array of apocalyptic warning messages (will embed the actual usage percentage)
MESSAGES=(
"⚠️  The sky darkens as your disk reaches ${USAGE_PCT}% full!"
"🔥  Flames lick the edges of your storage at ${USAGE_PCT}% usage!"
"☢️  Radiation levels spike: ${USAGE_PCT}% occupied!"
"🌪️  A vortex swirls, devouring ${USAGE_PCT}% of space!"
"🧟  Zombies crawl out of the ${USAGE_PCT}% filled sectors!"
)

if (( USAGE_PCT >= THRESHOLD )); then
    # Pick a random warning message
    idx=$(( RANDOM % ${#MESSAGES[@]} ))
    echo "${MESSAGES[$idx]}"
    exit 1
else
    echo "✅ All clear: disk usage is ${USAGE_PCT}%"
    exit 0
fi
