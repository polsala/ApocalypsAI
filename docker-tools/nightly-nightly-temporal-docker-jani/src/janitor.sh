#!/bin/bash

echo "🌌 Initiating Temporal Void-Sweeping Protocol..."
echo "Scanning for temporal anomalies (stale Docker resources)..."

# Execute the Docker system prune command
# -a: Remove all unused images (not just dangling ones)
# -f: Do not prompt for confirmation
# --volumes: Prune volumes
# Mock rationale: In a real run, this interacts with the Docker daemon.
# For testing, the 'docker' command will be mocked to simulate its output
# without requiring a live daemon or actual resource deletion.
DOCKER_OUTPUT=$(docker system prune -a -f --volumes 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "🧹 Temporal void swept clean! All detected anomalies purged."
    echo "Report from the Chrono-Custodian:"
    echo "$DOCKER_OUTPUT"
    echo "✨ Your Docker environment is now pristine and ready for new temporal deployments."
else
    echo "🚨 Temporal distortion detected during void-sweeping!"
    echo "Chrono-Custodian encountered an issue:"
    echo "$DOCKER_OUTPUT"
    echo "Please investigate the temporal flux."
    exit $EXIT_CODE
fi
