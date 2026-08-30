#!/bin/bash

set -euo pipefail

IMAGE="$1"
shift
COMMAND="$@"

if [ -z "$IMAGE" ]; then
    echo "Error: No Docker image specified."
    echo "Usage: nightly-version-vault <docker_image> <command...>"
    exit 1
fi

if [ -z "$COMMAND" ]; then
    echo "Error: No command to run specified."
    echo "Usage: nightly-version-vault <docker_image> <command...>"
    exit 1
fi

echo "Entering the Version Vault for image: $IMAGE"
echo "Executing command: $COMMAND"

# Run the command in a temporary Docker container
# --rm: Automatically remove the container when it exits
# -v "$(pwd):/app": Mount the current directory into /app inside the container
# -w /app: Set the working directory inside the container to /app
docker run --rm -v "$(pwd):/app" -w /app "$IMAGE" bash -c "$COMMAND"
