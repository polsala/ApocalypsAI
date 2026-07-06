#!/bin/bash
set -euo pipefail

# This script builds and runs the Temporal Container Tidy utility.
# It mounts the Docker socket to allow the utility to interact with the host's Docker daemon.

IMAGE_NAME="temporal-container-tidy"

echo "Building Docker image: $IMAGE_NAME..."
docker build -t "$IMAGE_NAME" .

echo "Running Temporal Container Tidy..."
echo "Note: This utility requires access to the Docker daemon via /var/run/docker.sock."
echo "      Use --dry-run to preview changes before --force-clean."

# Pass all arguments from this script to the Python script inside the container
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock "$IMAGE_NAME" "$@"
