#!/usr/bin/env bash

# nightly-disk-guardian – monitor root disk usage

# Default threshold (percentage)
THRESHOLD=${DISK_THRESHOLD:-80}

# Apocalyptic warnings
WARNINGS=(
    "⚠️ The end is near! Disk usage at %s%%."
    "🔥 Your storage is on fire! %s%% full."
    "💀 Doom approaches: %s%% of space consumed."
    "🌪️ A vortex of data swallows %s%% of your disk."
    "☢️ Radiation levels rising: %s%% used."
)

# Function to get usage percent
get_usage() {
    # Use df -h / and extract the Use% column, strip %
    df -h / | awk 'NR==2 {gsub("%","",$5); print $5}'
}

# Main logic
usage=$(get_usage)

if [[ -z "$usage" ]]; then
    echo "Error: Unable to determine disk usage."
    exit 2
fi

if (( usage > THRESHOLD )); then
    # Pick random warning
    idx=$(( RANDOM % ${#WARNINGS[@]} ))
    printf "${WARNINGS[$idx]}\n" "$usage"
    exit 1
else
    echo "Disk usage is $usage%, within safe limits."
    exit 0
fi
