#!/bin/bash

# Nightly Quantum Quibble Quencher
# A containerized sandbox for safely executing small, potentially conflicting scripts or commands.

set -euo pipefail

IMAGE_NAME="quibble-quencher-runtime"
CONTAINER_NAME_PREFIX="quibble-quench-session-"

# Function to build the Docker image if it doesn't exist
build_image() {
    if ! docker image inspect "$IMAGE_NAME" &>/dev/null; then
        echo "Building Docker image '$IMAGE_NAME' from $(dirname "$0")/Dockerfile..."
        # Build context is the directory containing the Dockerfile
        docker build -t "$IMAGE_NAME" -f "$(dirname "$0")/Dockerfile" "$(dirname "$0")"
        echo "Image '$IMAGE_NAME' built successfully."
    fi
}

# Function to clean up on exit
cleanup() {
    # The --rm flag on docker run handles most container removal.
    # This trap is primarily for printing the final message.
    echo "Quibble Quencher session complete. Purging temporal residue..."
}
trap cleanup EXIT

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <command_to_execute> [arg1] [arg2]..."
    echo "Example: $0 echo 'Hello from the void!'"
    echo "Example: $0 sh -c 'echo \"Error!\" >&2; exit 1'"
    exit 1
fi

# Build image if not present
build_image

echo "Initiating Quibble Quencher protocol for: $*"
echo "------------------------------------------------"

# Generate a unique container name for this run
CURRENT_CONTAINER_NAME="${CONTAINER_NAME_PREFIX}$(date +%s%N)"

# Execute the command in a new ephemeral container
# --rm: Automatically remove the container when it exits
# -i: Keep STDIN open even if not attached (useful for some commands)
# -a stdout -a stderr: Attach to stdout and stderr (ensures all output is captured)
# --name: Assign a specific name to the container for potential debugging/tracking
# $IMAGE_NAME: The image to use
# "$@": Pass all arguments as the command to execute inside the container
docker run --rm -i -a stdout -a stderr --name "$CURRENT_CONTAINER_NAME" "$IMAGE_NAME" "$@"

EXIT_CODE=$?

echo "------------------------------------------------"
echo "Quibble Quencher Report:"
echo "Command: $*"
echo "Exit Code: $EXIT_CODE"

if [ "$EXIT_CODE" -eq 0 ]; then
    echo "Status: Quibble successfully quenched. Reality remains stable."
else
    echo "Status: Quibble detected! Temporal ripples observed. Exit code indicates anomaly."
fi

exit "$EXIT_CODE"
