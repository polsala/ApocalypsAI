#!/bin/bash

# This script builds and runs the Nightly Chrono-Container.
# Usage: ./run-chrono-container.sh "your_command_here" ["YYYY-MM-DD HH:MM:SS"]

set -euo pipefail

UTIL_DIR="$(dirname "$0")"/..
DOCKERFILE_PATH="$UTIL_DIR/Dockerfile"
IMAGE_NAME="apocalypsai/nightly-chrono-container"

COMMAND="$1"
TEMPORAL_ANCHOR="$2"

if [ -z "$COMMAND" ]; then
    echo "Usage: $0 \"your_command_here\" [\"YYYY-MM-DD HH:MM:SS\"]"
    echo "Example: $0 \"date -u +%Y-%m-%d %H:%M:%S\" \"2077-10-23 13:37:00\""
    exit 1
fi

echo "Building Docker image: $IMAGE_NAME"
docker build -t "$IMAGE_NAME" -f "$DOCKERFILE_PATH" "$UTIL_DIR" || { echo "Docker build failed!"; exit 1; }

echo "Running command in Chrono-Container..."
# Pass the command and temporal anchor as arguments to the container's entrypoint
docker run --rm "$IMAGE_NAME" "$COMMAND" "$TEMPORAL_ANCHOR"
