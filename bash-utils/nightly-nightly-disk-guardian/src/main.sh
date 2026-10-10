#!/usr/bin/env bash

# nightly-disk-guardian
# Monitors root disk usage and warns with apocalyptic messages.

set -euo pipefail

# List of whimsical messages (usage will be interpolated at runtime)
MESSAGES=(
    "⚠️ The end is near! Disk space dwindles to ${usage}% ."
    "💀 Your storage is dying... ${usage}% used."
    "🔥 Apocalypse incoming! Only ${usage}% occupied."
    "🪦 Graveyard of files approaching: ${usage}% ."
    "🌪️ Storm of data engulfs you at ${usage}% usage."
)

# Function to obtain df output; can be overridden for testing via MOCK_DF
get_df_output() {
    if [[ -n "${MOCK_DF:-}" ]]; then
        echo "$MOCK_DF"
    else
        df -h /
    fi
}

# Parse the usage percent from df output
parse_usage() {
    local df_output
    df_output=$(get_df_output)
    # Expected format: Filesystem Size Used Avail Use% Mounted on
    # Grab the Use% column for the second line (the root filesystem)
    usage=$(echo "$df_output" | awk 'NR==2 {print $5}' | tr -d '%')
    echo "$usage"
}

main() {
    local threshold=${1:-80}
    usage=$(parse_usage)
    if (( usage > threshold )); then
        # Choose a random message index
        local idx=$((RANDOM % ${#MESSAGES[@]}))
        echo "${MESSAGES[$idx]}"
    else
        echo "✅ All is calm. Disk usage at ${usage}% ."
    fi
}

main "$@"
