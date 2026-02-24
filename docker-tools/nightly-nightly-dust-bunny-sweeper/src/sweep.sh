#!/bin/bash

REPORT_ONLY=true

# Function to display help message
show_help() {
    echo "Usage: sweep.sh [--prune]"
    echo ""
    echo "A containerized utility to sweep away digital dust bunnies: old Docker images, containers, and volumes."
    echo ""
    echo "Options:"
    echo "  --prune      Actually remove the identified resources. By default, it only reports."
    echo "  --help       Display this help message."
}

# Parse arguments
for arg in "$@"; do
    case $arg in
        --prune)
        REPORT_ONLY=false
        shift
        ;;
        --help)
        show_help
        exit 0
        ;;
        *)
        echo "Unknown option: $arg"
        show_help
        exit 1
        ;;
    esac
done

echo "ApocalypsAI Digital Dust Bunny Sweeper Report"
echo "---------------------------------------------"

# Find dangling images
echo "\n--- Dangling Images (untagged layers) ---"
DANGLING_IMAGES=$(docker images -f "dangling=true" -q)
if [ -z "$DANGLING_IMAGES" ]; then
    echo "No dangling images found."
else
    docker images -f "dangling=true"
    if [ "$REPORT_ONLY" = false ]; then
        echo "Pruning dangling images..."
        docker rmi $DANGLING_IMAGES
        echo "Dangling images pruned."
    fi
fi

# Find exited containers
echo "\n--- Exited Containers ---"
EXITED_CONTAINERS=$(docker ps -a -f "status=exited" -q)
if [ -z "$EXITED_CONTAINERS" ]; then
    echo "No exited containers found."
else
    docker ps -a -f "status=exited"
    if [ "$REPORT_ONLY" = false ]; then
        echo "Removing exited containers..."
        docker rm $EXITED_CONTAINERS
        echo "Exited containers removed."
    fi
fi

# Find unused volumes
echo "\n--- Unused Volumes ---"
# docker volume ls -f "dangling=true" lists volumes not used by any container
UNUSED_VOLUMES=$(docker volume ls -f "dangling=true" -q)
if [ -z "$UNUSED_VOLUMES" ]; then
    echo "No unused volumes found."
else
    docker volume ls -f "dangling=true"
    if [ "$REPORT_ONLY" = false ]; then
        echo "Pruning unused volumes..."
        docker volume rm $UNUSED_VOLUMES
        echo "Unused volumes pruned."
    fi
fi

echo "\n---------------------------------------------"
if [ "$REPORT_ONLY" = true ]; then
    echo "Report complete. Run with '--prune' to remove identified resources."
else
    echo "Cleanup complete."
fi
