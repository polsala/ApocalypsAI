#!/bin/bash

# This is the entrypoint for the Docker container.
# It acts as a wrapper to call the Python script,
# handling the actual docker commands if not in test mode.

set -e

CONTAINER_NAME_OR_ID="$1"

if [ -z "$CONTAINER_NAME_OR_ID" ]; then
    echo "Usage: nightly-docker-chrono-drift <container_name_or_id>"
    exit 1
fi

# Check if we are in test mode (mock files are mounted)
if [ -f "/app/mock_image_inspect.json" ] && \
   [ -f "/app/mock_container_inspect.json" ] && \
   [ -f "/app/mock_container_ls.txt" ]; then
    echo "Running in TEST MODE with mock files."
    python3 /app/chrono_drift.py \
        --container-id "$CONTAINER_NAME_OR_ID" \
        --image-inspect-file "/app/mock_image_inspect.json" \
        --container-inspect-file "/app/mock_container_inspect.json" \
        --container-ls-file "/app/mock_container_ls.txt"
else
    echo "Running in LIVE MODE, interacting with Docker daemon."

    # Get image ID from container
    IMAGE_ID=$(docker inspect "$CONTAINER_NAME_OR_ID" --format '{{.Image}}')
    if [ -z "$IMAGE_ID" ]; then
        echo "Error: Could not get image ID for container '$CONTAINER_NAME_OR_ID'."
        exit 1
    fi

    # Get inspect data for image and container
    docker inspect "$IMAGE_ID" > /tmp/live_image_inspect.json
    docker inspect "$CONTAINER_NAME_OR_ID" > /tmp/live_container_inspect.json

    # Get filesystem listing for temporal marker check
    # We'll do a recursive list of / to check for the marker file
    # This might be slow for very large filesystems, but for a marker it's fine.
    docker exec "$CONTAINER_NAME_OR_ID" ls -R / > /tmp/live_container_ls.txt || true # Allow ls to fail if container is not running or has issues

    python3 /app/chrono_drift.py \
        --container-id "$CONTAINER_NAME_OR_ID" \
        --image-inspect-file "/tmp/live_image_inspect.json" \
        --container-inspect-file "/tmp/live_container_inspect.json" \
        --container-ls-file "/tmp/live_container_ls.txt"

    # Clean up temporary files
    rm -f /tmp/live_image_inspect.json /tmp/live_container_inspect.json /tmp/live_container_ls.txt
fi
