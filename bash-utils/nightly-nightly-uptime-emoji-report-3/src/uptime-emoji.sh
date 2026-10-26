#!/usr/bin/env bash
# nightly-uptime-emoji-report
# Prints system uptime with an emoji reflecting duration.
# Usage: ./uptime-emoji.sh [seconds]
# If seconds argument is provided, it is used instead of reading /proc/uptime (useful for testing).

set -euo pipefail

# Function to convert seconds to human readable format
human_readable() {
    local total=$1
    local days=$((total/86400))
    local hours=$(( (total%86400)/3600 ))
    local minutes=$(( (total%3600)/60 ))
    local secs=$((total%60))
    local result=""
    if (( days > 0 )); then
        result+="${days}d "
    fi
    if (( hours > 0 || days > 0 )); then
        result+="${hours}h "
    fi
    if (( minutes > 0 || hours > 0 || days > 0 )); then
        result+="${minutes}m "
    fi
    result+="${secs}s"
    echo "$result"
}

# Determine uptime in seconds
if [[ $# -ge 1 ]]; then
    uptime_seconds=$1
else
    # Read from /proc/uptime, first field is seconds with fractions
    if [[ -f /proc/uptime ]]; then
        uptime_seconds=$(awk '{print int($1)}' /proc/uptime)
    else
        echo "Cannot determine uptime on this system." >&2
        exit 1
    fi
fi

# Select emoji based on uptime
if (( uptime_seconds < 3600 )); then
    emoji="🐣"
elif (( uptime_seconds < 21600 )); then
    emoji="🌞"
elif (( uptime_seconds < 86400 )); then
    emoji="🌤"
elif (( uptime_seconds < 259200 )); then
    emoji="🌥"
else
    emoji="🌙"
fi

human=$(human_readable "$uptime_seconds")
echo "Uptime: $human $emoji"
