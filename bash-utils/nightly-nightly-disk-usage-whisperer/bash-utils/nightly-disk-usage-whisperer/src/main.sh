#!/usr/bin/env bash
# nightly-disk-usage-whisperer
# Scans disk usage and warns if usage exceeds a threshold.

set -euo pipefail

# Default threshold (percentage)
THRESHOLD=80
INPUT_FILE=""

# Parse arguments
if [[ $# -ge 1 ]]; then
    THRESHOLD=$1
fi
if [[ $# -ge 2 ]]; then
    INPUT_FILE=$2
fi

# Function to get df output
get_df_output() {
    if [[ -n "$INPUT_FILE" ]]; then
        cat "$INPUT_FILE"
    else
        df -h
    fi
}

# Process each line
while IFS= read -r line; do
    # Skip header
    if [[ "$line" =~ ^Filesystem ]]; then
        echo "$line"
        continue
    fi
    # Extract usage percent (e.g., 45%)
    usage=$(echo "$line" | awk '{print $5}')
    # Remove trailing %
    usage_num=${usage%\%}
    # If usage is not a number, skip
    if ! [[ "$usage_num" =~ ^[0-9]+$ ]]; then
        echo "$line"
        continue
    fi
    if (( usage_num >= THRESHOLD )); then
        echo "$line ⚠️ High usage!"
    else
        echo "$line"
    fi
done < <(get_df_output)
