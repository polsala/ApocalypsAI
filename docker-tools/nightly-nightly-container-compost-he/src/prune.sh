#!/bin/bash

# Nightly Container Compost Heap - Pruning Script

echo "🌿 Starting Nightly Container Compost Heap..."

# Default configuration
DEFAULT_PRUNE_INTERVAL="24h" # Default to daily
DEFAULT_PRUNE_OPTIONS="--volumes --all" # Prune all unused images, containers, networks, and volumes

PRUNE_INTERVAL="${DOCKER_PRUNE_INTERVAL:-$DEFAULT_PRUNE_INTERVAL}"
PRUNE_OPTIONS="${DOCKER_PRUNE_OPTIONS:-$DEFAULT_PRUNE_OPTIONS}"

# Convert human-readable interval to seconds for sleep
# This is a simplified conversion, for production, a more robust parser would be needed.
# For this utility, we'll support 'Xs', 'Xm', 'Xh', 'Xd'
convert_interval_to_seconds() {
    local interval_str="$1"
    local num="${interval_str//[^0-9]/}"
    local unit="${interval_str//[0-9]/}"
    local seconds=0

    case "$unit" in
        s|S|"") seconds="$num" ;;
        m|M) seconds=$((num * 60)) ;;
        h|H) seconds=$((num * 3600)) ;;
        d|D) seconds=$((num * 86400)) ;;
        *) echo "Warning: Unknown interval unit '$unit'. Defaulting to 24 hours." >&2; seconds=86400 ;;
    esac
    echo "$seconds"
}

SLEEP_SECONDS=$(convert_interval_to_seconds "$PRUNE_INTERVAL")

if [ -z "$SLEEP_SECONDS" ] || [ "$SLEEP_SECONDS" -le 0 ]; then
    echo "Error: Invalid or zero sleep interval calculated. Exiting."
    exit 1
fi

echo "Configured to prune every: $PRUNE_INTERVAL ($SLEEP_SECONDS seconds)"
echo "Prune options: docker system prune -f $PRUNE_OPTIONS"

while true; do
    echo "---"
    echo "🌱 Time to turn digital debris into compost! Running 'docker system prune -f $PRUNE_OPTIONS'..."
    
    # Execute the prune command
    # We need to ensure docker is available. In a Docker container, this usually means
    # mounting /var/run/docker.sock
    if command -v docker &> /dev/null; then
        docker system prune -f $PRUNE_OPTIONS
        if [ $? -eq 0 ]; then
            echo "✅ Compost heap tidied! Disk space reclaimed."
        else
            echo "❌ Failed to prune Docker system. Check Docker daemon connection or permissions."
        fi
    else
        echo "⚠️ Docker command not found. Is /var/run/docker.sock mounted correctly?"
    fi

    echo "😴 Resting for $PRUNE_INTERVAL before the next composting cycle..."
    sleep "$SLEEP_SECONDS"
done
