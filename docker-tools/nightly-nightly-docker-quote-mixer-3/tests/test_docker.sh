#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Use Docker CLI to build and run the image locally; this is deterministic because we only verify the presence of a \"quote\" field in the JSON response.

IMAGE_NAME="quote-mixer-test"
CONTAINER_NAME="quote-mixer-test-container"

# Build the Docker image (quiet output)
docker build -t "$IMAGE_NAME" . > /dev/null

# Run the container in the background, mapping host port 18080 to container port 8080
docker run -d --rm -p 18080:8080 --name "$CONTAINER_NAME" "$IMAGE_NAME"

# Give the server a moment to start
sleep 2

# Retrieve the quote via curl
RESPONSE=$(curl -s http://localhost:18080/quote)

# Simple validation: response must contain a "quote" field
if echo "$RESPONSE" | grep -q '"quote"'; then
    echo "PASS: Received quote"
else
    echo "FAIL: Unexpected response"
    exit 1
fi

# Clean up the container
docker stop "$CONTAINER_NAME" > /dev/null
