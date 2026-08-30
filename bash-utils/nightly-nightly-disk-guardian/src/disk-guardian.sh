#!/usr/bin/env bash
set -euo pipefail

# Configurable threshold (percentage)
DISK_THRESHOLD="${DISK_THRESHOLD:-80}"

# Apocalyptic messages array
APOC_MESSAGES=(
    "⚠️ The sky darkens as your disk fills... %s%% used!"
    "🔥 Your storage is ablaze! %s%% occupied!"
    "☢️ Radiation levels rising: %s%% disk usage!"
    "🌋 Volcanic eruption imminent at %s%% capacity!"
    "🧟 Zombies are crowding your bytes: %s%% used!"
)

# Function to get df output (allows mocking)
get_df_output() {
    if [[ -n "${MOCK_DF:-}" ]]; then
        echo "$MOCK_DF"
    else
        df -h /
    fi
}

# Extract used percentage (e.g., 73%)
used_percent=$(get_df_output | awk 'NR==2 {print $5}' | tr -d '%')
if ! [[ "$used_percent" =~ ^[0-9]+$ ]]; then
    echo "Error: Unable to parse disk usage."
    exit 1
fi

if (( used_percent >= DISK_THRESHOLD )); then
    # Pick random message
    idx=$(( RANDOM % ${#APOC_MESSAGES[@]} ))
    msg=${APOC_MESSAGES[$idx]}
    printf "$msg\n" "$used_percent"
    exit 2
else
    echo "✅ Disk usage is safe: $used_percent% (threshold $DISK_THRESHOLD%)."
    exit 0
fi
