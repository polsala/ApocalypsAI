#!/bin/bash
set -euo pipefail

MODE=${1:-"all"} # all, images, volumes, networks
AGE=${2:-"24h"}  # e.g., 24h, 7d, 30m

echo "Starting Digital Dust Bunny Sweeper..."
echo "Mode: ${MODE}, Age threshold: ${AGE}"

# Ensure docker socket is available if running inside a container
# Mock rationale: This check is crucial for the utility's real-world operation.
# In tests, a dummy socket file is created to bypass this check and allow the mocked 'docker' command to be called.
if [ ! -S "/var/run/docker.sock" ]; then
    echo "Error: Docker socket /var/run/docker.sock not found. This utility needs access to the Docker daemon."
    echo "Please run with '-v /var/run/docker.sock:/var/run/docker.sock'"
    exit 1
fi

# Function to run docker prune with logging
run_prune() {
    local type=$1
    local subcommand=$2 # e.g., "system prune", "image prune"
    echo "--- Pruning ${type} older than ${AGE} ---"
    # Using --force to avoid interactive prompt
    if docker $subcommand --force --filter "until=${AGE}"; then
        echo "Successfully pruned ${type}."
    else
        echo "Warning: Failed to prune ${type}. Check logs for details."
    fi
    echo ""
}

case "$MODE" in
    all)
        run_prune "system" "system prune"
        ;;
    images)
        run_prune "images" "image prune"
        ;;
    volumes)
        run_prune "volumes" "volume prune"
        ;;
    networks)
        run_prune "networks" "network prune"
        ;;
    *)
        echo "Invalid mode: ${MODE}. Supported modes: all, images, volumes, networks."
        exit 1
        ;;
esac

echo "Digital Dust Bunny Sweeper finished."
