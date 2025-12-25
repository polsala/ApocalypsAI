#!/usr/bin/env bash
set -euo pipefail

# Function to get df output; can be overridden for testing
get_df_output() {
    df -P "$1"
}

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <config-file>"
    exit 1
fi

config_file="$1"

while IFS= read -r line || [[ -n "$line" ]]; do
    # Skip empty lines and comments
    [[ -z "$line" || "$line" =~ ^# ]] && continue
    dir=$(echo "$line" | awk '{print $1}')
    thresh=$(echo "$line" | awk '{print $2}')
    if [[ -z "$dir" || -z "$thresh" ]]; then
        echo "Invalid line in config: $line"
        continue
    fi
    # Get usage percent for the filesystem containing dir
    usage=$(get_df_output "$dir" | awk 'NR==2 {print $5}' | tr -d '%')
    if (( usage >= thresh )); then
        if (( usage >= 90 )); then
            echo "💀  $dir is at ${usage}% – the void beckons!"
        else
            echo "⚠️  $dir is at ${usage}% – beware the wasteland!"
        fi
    fi
done < "$config_file"
