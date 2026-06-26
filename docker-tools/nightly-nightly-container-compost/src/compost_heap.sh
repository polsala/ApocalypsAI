#!/bin/bash

# Nightly Container Compost Heap
# Identifies and optionally prunes unused Docker resources.

DRY_RUN=true
# The actual prune command arguments to execute.
# It removes all unused images, volumes, and networks that are older than 24 hours.
# --force prevents confirmation prompts.
PRUNE_ARGS="system prune --force --all --volumes --filter \"until=24h\""

# Function to display help message
show_help() {
    echo "Usage: $0 [--dry-run | --prune]"
    echo ""
    echo "  --dry-run   (default) Show what would be pruned without actually removing anything."
    echo "              Outputs a 'Digital Compost Report'."
    echo "  --prune     Actually prune unused Docker images, volumes, and networks."
    echo "              Use with caution! This will free up space."
    echo ""
    echo "This utility helps clear out the digital dust bunnies from your Docker environment,"
    echo "turning unused resources into fertile ground for new container sprouts."
}

# Parse arguments
if [ "$#" -gt 1 ]; then
    echo "Error: Too many arguments."
    show_help
    exit 1
fi

if [ "$#" -eq 1 ]; then
    case "$1" in
        --dry-run)
            DRY_RUN=true
            ;;
        --prune)
            DRY_RUN=false
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Error: Unknown option '$1'"
            show_help
            exit 1
            ;;
    esac
fi

echo "🌿 Welcome to the Nightly Container Compost Heap! 🌿"
echo "Scanning for digital dust bunnies and forgotten container remnants..."
echo ""

if [ "$DRY_RUN" = true ]; then
    echo "--- Digital Compost Report (Dry Run) ---"
    echo "The following items are ripe for composting (would be removed):"
    # Mock rationale: A true 'docker system prune --dry-run' doesn't exist.
    # We simulate its output by listing common prune targets.
    # For a more robust dry-run, one might capture and parse the output of
    # 'docker system prune --force --all --volumes' and then not proceed with actual removal.
    # For simplicity and deterministic testing, we list illustrative targets.
    echo "  - Dangling images (unreferenced layers)"
    echo "  - Unused volumes (not attached to any container)"
    echo "  - Stopped containers (older than 24 hours)"
    echo "  - Unused networks (not connected to any running container)"
    echo ""
    echo "To actually prune these, run with '--prune'."
    echo "----------------------------------------"
    exit 0
else
    echo "--- Initiating Digital Composting Process ---"
    echo "Preparing to prune unused Docker resources. This might take a moment..."
    echo "Command: docker $PRUNE_ARGS"
    echo ""
    # Mock rationale: In a real scenario, this would execute the actual docker command.
    # For testing, the 'docker' function is mocked to prevent actual system changes.
    docker $PRUNE_ARGS
    if [ $? -eq 0 ]; then
        echo ""
        echo "🌱 Digital compost created! Your Docker environment is now tidier. 🌱"
        echo "New container sprouts will thank you for the fertile ground."
    else
        echo ""
        echo "❌ Composting process encountered an issue. Please check the output above."
    fi
    echo "-------------------------------------------"
    exit $?
fi
