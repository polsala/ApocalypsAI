#!/usr/bin/env bash
# dusty_disk_watcher.sh - Warn about high disk usage with whimsical messages

# Default threshold percentage
THRESHOLD=${1:-80}

# Function to get df output; can be overridden via DF_OUTPUT env var for testing
get_df_output() {
    if [[ -n "$DF_OUTPUT" ]]; then
        echo "$DF_OUTPUT"
    else
        df -h /
    fi
}

# Extract usage percent (e.g., 85%)
USAGE=$(get_df_output | awk 'NR==2 {gsub("%","",$5); print $5}')

# Compare usage with threshold
if (( USAGE >= THRESHOLD )); then
    echo "⚠️  Warning! Disk usage at ${USAGE}% – The wasteland is swelling!"
else
    echo "✅  All clear. Disk usage at ${USAGE}% – The dunes are calm."
fi

exit 0
