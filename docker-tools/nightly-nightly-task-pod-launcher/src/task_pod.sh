#!/bin/bash

# Nightly Task Pod Launcher
# Launches a temporary Docker container to execute a single command and then self-destructs.

set -euo pipefail

IMAGE="$1"
COMMAND="$2"
CONTAINER_NAME="nightly-task-pod-$(date +%s%N)" # Unique name

echo "Launching task pod '$CONTAINER_NAME' with image '$IMAGE' to execute: $COMMAND"

# Run the command in a temporary container.
# --rm: Automatically remove the container when it exits.
# -v "$(pwd):/workspace": Mount the current directory into /workspace in the container.
# -w /workspace: Set the working directory inside the container.
# Using /bin/sh -c for command execution to ensure it runs within a shell context
# This allows for complex commands with pipes, redirects, etc.
docker run --rm \
           -v "$(pwd):/workspace" \
           -w /workspace \
           --name "$CONTAINER_NAME" \
           "$IMAGE" \
           /bin/sh -c "$COMMAND"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "Task pod '$CONTAINER_NAME' completed successfully."
else
    echo "Task pod '$CONTAINER_NAME' failed with exit code $EXIT_CODE."
fi

exit $EXIT_CODE
