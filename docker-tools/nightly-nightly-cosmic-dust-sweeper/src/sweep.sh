#!/bin/bash

set -euo pipefail

echo "🌌 Initiating Cosmic Dust Sweep..."

# Configuration variables
# Set to "true" or "false" via environment variables
DRY_RUN=${DRY_RUN:-"false"}
INCLUDE_VOLUMES=${INCLUDE_VOLUMES:-"true"} # Set to "false" to skip volume pruning

PRUNE_COMMAND="docker system prune --all --force"

if [ "$INCLUDE_VOLUMES" = "true" ]; then
    PRUNE_COMMAND="$PRUNE_COMMAND --volumes"
    echo "🧹 Including unused volumes in the sweep."
else
    echo "🚫 Skipping unused volume pruning."
fi

if [ "$DRY_RUN" = "true" ]; then
    echo "🔭 Performing a dry run. No actual dust will be removed."
    echo "MOCK: This would execute '$PRUNE_COMMAND' if DRY_RUN was false."
    echo "MOCK: No changes made during dry run."
    exit 0 # Exit successfully for dry run
else
    echo "Executing: $PRUNE_COMMAND"
    # Execute the actual docker prune command
    $PRUNE_COMMAND
    if [ $? -eq 0 ]; then
        echo "✨ Cosmic Dust Sweep complete! Your Docker realm is sparkling clean."
    else
        echo "⚠️ Cosmic Dust Sweep encountered anomalies. Check the logs for details."
        exit 1
    fi
fi
