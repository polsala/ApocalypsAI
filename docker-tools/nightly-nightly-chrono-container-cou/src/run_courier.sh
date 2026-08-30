#!/bin/bash
set -euo pipefail

# Check if the Docker socket is accessible. This is crucial for the courier to function.
if [ ! -S "/var/run/docker.sock" ]; then
    echo "Error: Docker socket /var/run/docker.sock not found or not accessible."
    echo "Please ensure the courier container is run with: -v /var/run/docker.sock:/var/run/docker.sock"
    exit 1
fi

# The first argument is the target Docker image (e.g., python:3.9-slim)
TARGET_IMAGE="$1"
shift 1

# The remaining arguments are passed directly to the 'docker run' command for the target container.
# This allows users to specify commands, arguments, environment variables, etc.
TARGET_CONTAINER_ARGS=($@)

# Validate that a target image was provided.
if [ -z "$TARGET_IMAGE" ]; then
    echo "Usage: run_courier.sh <target_image> [docker_run_args_for_target_container...]"
    echo "Example: run_courier.sh python:3.9-slim python /app/my_script.py arg1"
    exit 1
fi

echo "--- Chrono-Container Courier Dispatch ---"
echo "Target Image: $TARGET_IMAGE"
echo "Target Container Args: ${TARGET_CONTAINER_ARGS[*]}"
echo "-----------------------------------------"

# Execute the command in the target container.
# We assume that the host's current working directory has been mounted into the courier container
# at /app_host_mount, and we pass this mount through to the target container as /app.
# This allows scripts and files from the host to be accessible within the target container.
# The '--rm' flag ensures the target container is removed after execution.

docker run --rm -v /app_host_mount:/app "$TARGET_IMAGE" "${TARGET_CONTAINER_ARGS[@]}"
