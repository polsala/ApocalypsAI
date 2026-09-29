#!/usr/bin/env bash

# nightly-emoji-disk-report
# Displays disk usage with emojis.

# Function to get df output; can be overridden in tests.
get_df_output() {
    df -h --output=source,size,used,avail,pcent,target -x tmpfs -x devtmpfs
}

# Function to map usage percent to emoji.
usage_to_emoji() {
    local usage=$1
    if (( usage < 50 )); then
        echo "🌱"
    elif (( usage < 80 )); then
        echo "🌿"
    elif (( usage < 95 )); then
        echo "🌳"
    else
        echo "🔥"
    fi
}

main() {
    local df_output
    df_output=$(get_df_output)

    # Skip header line
    while IFS= read -r line; do
        # Header line contains "Filesystem"
        if [[ "$line" == *"Filesystem"* ]]; then
            continue
        fi
        # Parse fields: source size used avail pcent target
        local source size used avail pcent target
        read -r source size used avail pcent target <<<"$line"
        # Remove % from pcent
        local usage=${pcent%\%}
        local emoji
        emoji=$(usage_to_emoji "$usage")
        printf "%s %s %s %s %s %s %s\n" "$emoji" "$source" "$size" "$used" "$avail" "$pcent" "$target"
    done <<<"$df_output"
}

# If script is executed, run main
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
