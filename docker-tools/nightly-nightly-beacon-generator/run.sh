#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

IMAGE_NAME="nightly-beacon-generator"
CONTAINER_NAME="beacon-service"
HOST_PORT="8080"
CONTAINER_PORT="5000"

echo "--- Building Docker image: $IMAGE_NAME ---"
docker build -t "$IMAGE_NAME" .

echo "--- Stopping and removing any existing container: $CONTAINER_NAME ---"
docker stop "$CONTAINER_NAME" > /dev/null 2>&1 || true
docker rm "$CONTAINER_NAME" > /dev/null 2>&1 || true

echo "--- Running Docker container: $CONTAINER_NAME on port $HOST_PORT ---"
docker run -d -p "$HOST_PORT":"$CONTAINER_PORT" --name "$CONTAINER_NAME" "$IMAGE_NAME"

echo "Service is running. Access it at http://localhost:$HOST_PORT/generate_beacon"
echo "To stop: docker stop $CONTAINER_NAME"
echo "To remove: docker rm $CONTAINER_NAME"
echo "To remove image: docker rmi $IMAGE_NAME"
