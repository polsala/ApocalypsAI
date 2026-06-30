#!/bin/bash
set -euo pipefail

IMAGE_NAME="foraging-pod-image"
# Use a timestamp for a unique container name to avoid conflicts
CONTAINER_NAME="foraging-pod-container-$(date +%s)"
COMMAND_TO_RUN="$@"

# Check if a command was provided
if [ -z "$COMMAND_TO_RUN" ]; then
    echo "Usage: $0 <command_to_run_in_container>"
    echo "Example: $0 \"ls -la /\""
    exit 1
fi

echo "Building Foraging Pod image..."
# Build the Docker image silently, redirecting output to /dev/null
docker build -t "$IMAGE_NAME" . > /dev/null

echo "Launching Foraging Pod container '$CONTAINER_NAME' and running command: '$COMMAND_TO_RUN'"
# Run the container, execute the command, and automatically remove it afterwards (--rm)
# We use 'bash -c' to ensure the command is executed within a shell inside the container
docker run --rm --name "$CONTAINER_NAME" "$IMAGE_NAME" bash -c "$COMMAND_TO_RUN"

echo "Foraging Pod mission complete. Cleaning up..."
# Remove the Docker image silently
docker rmi "$IMAGE_NAME" > /dev/null

echo "Foraging Pod is gone. Stay safe out there!"
