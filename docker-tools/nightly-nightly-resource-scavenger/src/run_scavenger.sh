#!/bin/bash
set -euo pipefail

# Helper script to build and run the Nightly Resource Scavenger Docker container.
# This script mounts the host's Docker socket into the container, allowing the
# scavenger to inspect other containers on the host.

IMAGE_NAME="apocalypsai/nightly-resource-scavenger"
CONTAINER_NAME="nightly-resource-scavenger-runner"

echo "--- Building Nightly Resource Scavenger Docker image ---"
# Build the Docker image from the current directory's Dockerfile
docker build -t "$IMAGE_NAME" .

echo "--- Running Nightly Resource Scavenger ---"
echo "  (Mounting /var/run/docker.sock to allow container to inspect host's Docker daemon)"
echo "  (Any arguments passed to this script will be forwarded to the scavenger script inside the container)"
echo ""

# Run the container, mounting the Docker socket.
# --rm ensures the container is removed after it exits, keeping the system clean.
# -v /var/run/docker.sock:/var/run/docker.sock provides the container access to the Docker daemon.
# --name gives a predictable name for the ephemeral runner instance.
# "$@" forwards all arguments passed to this host script directly to the ENTRYPOINT
# (which is src/scavenge.sh) of the Docker container.
docker run --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    --name "$CONTAINER_NAME" \
    "$IMAGE_NAME" "$@"

echo ""
echo "--- Nightly Resource Scavenger finished ---"
