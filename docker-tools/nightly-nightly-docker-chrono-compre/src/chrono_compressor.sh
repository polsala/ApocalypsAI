#!/bin/bash

set -euo pipefail

# Function to display help message
show_help() {
    echo "Usage: $0 <target_container> <resource_type> <value> <duration_seconds>"
    echo ""
    echo "A whimsical utility to temporarily throttle CPU or I/O resources for a target Docker container."
    echo "Useful for simulating resource scarcity and testing application resilience."
    echo ""
    echo "Arguments:"
    echo "  <target_container>  Name or ID of the Docker container to throttle."
    echo "  <resource_type>     Type of resource to throttle: 'cpu' or 'io'."
    echo "  <value>"
    echo "                      For 'cpu': CPU shares (integer, 2-1024). Lower value means less CPU."
    echo "                                 (Default is 1024. E.g., 100 for ~10% of default shares)."
    echo "                      For 'io': Block I/O weight (integer, 10-1000). Lower value means less I/O."
    echo "                                (Default is 500. E.g., 100 for ~20% of default weight)."
    echo "  <duration_seconds>  Duration in seconds to apply the throttling (integer)."
    echo ""
    echo "Examples:"
    echo "  # Throttle 'my-app' container's CPU to 100 shares for 30 seconds"
    echo "  docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \\"
    echo "    my-chrono-compressor my-app cpu 100 30"
    echo ""
    echo "  # Throttle 'db-server' container's I/O to 100 weight for 60 seconds"
    echo "  docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \\"
    echo "    my-chrono-compressor db-server io 100 60"
    exit 0
}

# Check for --help or insufficient arguments
if [[ "$#" -lt 4 || "$1" == "--help" ]]; then
    show_help
fi

TARGET_CONTAINER="$1"
RESOURCE_TYPE="$2"
VALUE="$3"
DURATION_SECONDS="$4"

# Validate arguments
if ! docker inspect "$TARGET_CONTAINER" &>/dev/null; then
    echo "Error: Target container '$TARGET_CONTAINER' not found or Docker daemon not accessible." >&2
    exit 1
fi

if [[ "$RESOURCE_TYPE" != "cpu" && "$RESOURCE_TYPE" != "io" ]]; then
    echo "Error: Invalid resource type. Must be 'cpu' or 'io'." >&2
    exit 1
fi

if ! [[ "$VALUE" =~ ^[0-9]+$ ]] || [[ "$VALUE" -lt 1 ]]; then
    echo "Error: Value must be a positive integer." >&2
    exit 1
fi

if ! [[ "$DURATION_SECONDS" =~ ^[0-9]+$ ]] || [[ "$DURATION_SECONDS" -lt 1 ]]; then
    echo "Error: Duration must be a positive integer in seconds." >&2
    exit 1
fi

echo "--- Chrono-Compressor Initiated ---"
echo "Target: $TARGET_CONTAINER"
echo "Resource: $RESOURCE_TYPE"
echo "Value: $VALUE"
echo "Duration: ${DURATION_SECONDS}s"
echo "-----------------------------------"

ORIGINAL_CPU_SHARES=""
ORIGINAL_BLKIO_WEIGHT=""

# Get original values before throttling
if [[ "$RESOURCE_TYPE" == "cpu" ]]; then
    ORIGINAL_CPU_SHARES=$(docker inspect "$TARGET_CONTAINER" --format '{{.HostConfig.CpuShares}}')
    echo "Original CPU Shares: $ORIGINAL_CPU_SHARES"
elif [[ "$RESOURCE_TYPE" == "io" ]]; then
    ORIGINAL_BLKIO_WEIGHT=$(docker inspect "$TARGET_CONTAINER" --format '{{.HostConfig.BlkioWeight}}')
    echo "Original Block I/O Weight: $ORIGINAL_BLKIO_WEIGHT"
fi

echo "Applying compression..."
if [[ "$RESOURCE_TYPE" == "cpu" ]]; then
    docker update --cpu-shares "$VALUE" "$TARGET_CONTAINER"
    echo "CPU shares set to $VALUE for $TARGET_CONTAINER."
elif [[ "$RESOURCE_TYPE" == "io" ]]; then
    docker update --blkio-weight "$VALUE" "$TARGET_CONTAINER"
    echo "Block I/O weight set to $VALUE for $TARGET_CONTAINER."
fi

echo "Waiting for ${DURATION_SECONDS} seconds..."
sleep "$DURATION_SECONDS"

echo "Releasing compression..."
if [[ "$RESOURCE_TYPE" == "cpu" ]]; then
    if [[ -n "$ORIGINAL_CPU_SHARES" ]]; then
        docker update --cpu-shares "$ORIGINAL_CPU_SHARES" "$TARGET_CONTAINER"
        echo "CPU shares restored to $ORIGINAL_CPU_SHARES for $TARGET_CONTAINER."
    else
        echo "Warning: Could not retrieve original CPU shares. Skipping restore." >&2
    fi
elif [[ "$RESOURCE_TYPE" == "io" ]]; then
    if [[ -n "$ORIGINAL_BLKIO_WEIGHT" ]]; then
        docker update --blkio-weight "$ORIGINAL_BLKIO_WEIGHT" "$TARGET_CONTAINER"
        echo "Block I/O weight restored to $ORIGINAL_BLKIO_WEIGHT for $TARGET_CONTAINER."
    else
        echo "Warning: Could not retrieve original Block I/O weight. Skipping restore." >&2
    fi
fi

echo "--- Chrono-Compression Complete ---"
