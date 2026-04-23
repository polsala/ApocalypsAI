#!/bin/bash

set -euo pipefail

# Default values
DOCKERFILE="Dockerfile"
COMMAND="bash"
CONTAINER_NAME=""

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    key="$1"
    case $key in
        --dockerfile)
        DOCKERFILE="$2"
        shift # past argument
        shift # past value
        ;;
        --command)
        COMMAND="$2"
        shift # past argument
        shift # past value
        ;;
        --name)
        CONTAINER_NAME="$2"
        shift # past argument
        shift # past value
        ;;
        -h|--help)
        echo "Usage: $0 [--dockerfile <path>] [--command <cmd>] [--name <container_name>]"
        exit 0
        ;;
        *)
        # If no container name is provided, use a default based on the Dockerfile name
        if [ -z "$CONTAINER_NAME" ]; then
            CONTAINER_NAME=$(basename "$DOCKERFILE" | sed 's/\.[^.]*$//')-env
        fi
        # Assume remaining arguments are for the command
        COMMAND="$@"
        break
        ;;
    esac
done

# If no container name was explicitly set and we are here, it means the command was the first argument
if [ -z "$CONTAINER_NAME" ]; then
    CONTAINER_NAME=$(basename "$DOCKERFILE" | sed 's/\.[^.]*$//')-env
fi

# Create a temporary Dockerfile if it's not the default one
TEMP_DOCKERFILE=""
if [ "$DOCKERFILE" != "Dockerfile" ]; then
    TEMP_DOCKERFILE=$(mktemp)
    echo "FROM alpine:latest" > "$TEMP_DOCKERFILE"
    echo "RUN apk add --no-cache docker docker-cli bash curl" >> "$TEMP_DOCKERFILE"
    cat "$DOCKERFILE" >> "$TEMP_DOCKERFILE"
    DOCKERFILE="$TEMP_DOCKERFILE"
fi

# Build a temporary image from the Dockerfile
IMAGE_TAG="apoc-temp-env-$(date +%s%N)"
docker build -t "$IMAGE_TAG" -f "$DOCKERFILE" .

# Run the container
# We use --privileged to allow docker commands inside the container if needed
# We also mount the docker socket to allow the container to control the host's docker daemon
# This is a powerful feature and should be used with caution.
# For simpler use cases, you might not need these flags.

# Check if docker socket exists before mounting
DOCKER_SOCKET="/var/run/docker.sock"
if [ -S "$DOCKER_SOCKET" ]; then
    docker run -d --name "$CONTAINER_NAME" -v "$DOCKER_SOCKET":"$DOCKER_SOCKET" --privileged "$IMAGE_TAG" "$COMMAND"
else
    echo "Warning: Docker socket not found at $DOCKER_SOCKET. Running without docker daemon access inside the container."
    docker run -d --name "$CONTAINER_NAME" "$IMAGE_TAG" "$COMMAND"
fi

# Clean up temporary Dockerfile if created
if [ -n "$TEMP_DOCKERFILE" ] && [ -f "$TEMP_DOCKERFILE" ]; then
    rm "$TEMP_DOCKERFILE"
fi

# Clean up the temporary image
docker rmi "$IMAGE_TAG" > /dev/null 2>&1 || true

echo "Environment '$CONTAINER_NAME' started with command: '$COMMAND'"
