#!/usr/bin/env bash
set -euo pipefail

# Default threshold (percentage)
THRESHOLD=${1:-80}

# Get usage percent of the root filesystem
USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')

# Function to pick a random apocalypse‑themed warning
random_warning() {
    warnings=(
        "The sky darkens as your storage swells!"
        "Ravens gather over the overflowing bytes."
        "The digital tide rises, beware the flood."
        "Your disks whisper of impending doom."
        "Apocalypse imminent: space runs out!"
    )
    echo "${warnings[$RANDOM % ${#warnings[@]}]}"
}

if (( USAGE > THRESHOLD )); then
    echo "⚠️  Disk usage at ${USAGE}% – $(random_warning)"
else
    echo "✅  Disk usage at ${USAGE}% – All is calm."
fi
