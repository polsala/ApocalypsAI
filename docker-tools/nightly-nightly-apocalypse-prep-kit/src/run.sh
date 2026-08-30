#!/bin/bash

# Define image name
IMAGE_NAME="apocalypsai-prep-kit"
CONTAINER_NAME="apocalypsai-prep-kit-instance"

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

echo "Building Docker image: $IMAGE_NAME from $SCRIPT_DIR..."
docker build -t "$IMAGE_NAME" "$SCRIPT_DIR"

if [ $? -ne 0 ]; then
    echo "Docker image build failed."
    exit 1
fi

echo "Running container $CONTAINER_NAME with current working directory mounted to /workspace..."
echo "To exit, type 'exit' inside the container."

# Remove any existing container with the same name
docker rm -f "$CONTAINER_NAME" &> /dev/null

# Run the container, mounting the current working directory of the user
# This allows users to work on files within their current context.
docker run -it --rm \
    --name "$CONTAINER_NAME" \
    -v "$(pwd)":/workspace \
    "$IMAGE_NAME"
