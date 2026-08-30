#!/bin/bash
set -euo pipefail # Exit on error, unset variables, and pipeline failures

echo "🌱 Welcome to the Chrono-Gardener! Time to tend to your digital garden. 🌿"

DRY_RUN=${DRY_RUN:-"false"}
PRUNE_VOLUMES=${PRUNE_VOLUMES:-"false"} # Set to "true" to prune volumes too

PRUNE_CMD="docker system prune -f"

if [ "$PRUNE_VOLUMES" = "true" ]; then
    PRUNE_CMD="$PRUNE_CMD --volumes"
    echo "Including unused volumes in the pruning process. 🌱"
else
    echo "Unused volumes will be preserved. Set PRUNE_VOLUMES=true to include them. 💧"
fi

if [ "$DRY_RUN" = "true" ]; then
    echo "🔍 Performing a dry run. No actual pruning will occur, just a peek at the weeds!"
    echo "Would execute: $PRUNE_CMD"
else
    echo "🧹 Sweeping away digital debris..."
    # Execute the command, capturing its output
    if ! $PRUNE_CMD; then
        echo "❌ Chrono-Gardener encountered an issue during pruning. Check Docker daemon status and permissions." >&2
        exit 1
    fi
fi

echo "✨ Your digital garden is now refreshed and tidy! Happy containerizing! ✨"
