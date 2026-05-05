#!/bin/bash
set -euo pipefail

TARGET_IMAGE="$1"
DURATION_SECONDS="$2"
shift 2
COMMAND="$@"

if [ -z "$TARGET_IMAGE" ] || [ -z "$DURATION_SECONDS" ] || [ -z "$COMMAND" ]; then
    echo "Usage: $0 <target_image> <duration_seconds> <command...>"
    exit 1
fi

CONTAINER_NAME="ephemeral-env-$(date +%s%N)-$$" # Add PID for more uniqueness

echo "Launching ephemeral environment '$CONTAINER_NAME' from image '$TARGET_IMAGE' for $DURATION_SECONDS seconds..."
echo "Command: $COMMAND"

# Run the target container in detached mode
docker run -d --name "$CONTAINER_NAME" "$TARGET_IMAGE" $COMMAND > /dev/null

if [ $? -ne 0 ]; then
    echo "Failed to launch target container."
    exit 1
fi

echo "Container '$CONTAINER_NAME' started. Waiting for $DURATION_SECONDS seconds..."

# Wait for the specified duration
sleep "$DURATION_SECONDS"

echo "Duration expired. Checking container '$CONTAINER_NAME' status..."

# Check if the container is still running
if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
    echo "Container '$CONTAINER_NAME' is still running. Stopping and removing..."
    docker stop "$CONTAINER_NAME" > /dev/null
    docker rm "$CONTAINER_NAME" > /dev/null
    if [ $? -ne 0 ]; then
        echo "Failed to stop/remove container '$CONTAINER_NAME'."
    else
        echo "Container '$CONTAINER_NAME' stopped and removed."
    fi
else
    echo "Container '$CONTAINER_NAME' already exited. Removing any lingering resources..."
    # Even if it exited, ensure it's removed in case it's just stopped
    docker rm "$CONTAINER_NAME" > /dev/null 2>&1 || true # `|| true` to prevent script from exiting if rm fails (e.g., already removed)
    echo "Container '$CONTAINER_NAME' was already stopped/removed."
fi

echo "Ephemeral environment enforcement complete."
