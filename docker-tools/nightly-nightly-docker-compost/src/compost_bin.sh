#!/bin/bash

# Nightly Docker Compost Bin - Prunes Docker resources

# Default options
PRUNE_IMAGES=0
PRUNE_CONTAINERS=0
PRUNE_VOLUMES=0
FORCE_PRUNE=""
DRY_RUN=0

# Function to display help message
show_help() {
    echo "Usage: compost_bin.sh [OPTIONS]"
    echo "A containerized utility to prune unused Docker images, stopped containers, and dangling volumes."
    echo ""
    echo "Options:"
    echo "  -a, --all           Prune all unused images (not just dangling), stopped containers, and dangling volumes. (Default if no specific prune options)"
    echo "  -i, --images        Prune only dangling and unused images."
    echo "  -c, --containers    Prune only stopped containers."
    echo "  -v, --volumes       Prune only dangling volumes."
    echo "  -d, --dry-run       Simulate the pruning process without deleting anything."
    echo "  -f, --force         Do not prompt for confirmation. Use with caution!"
    echo "  -h, --help          Display this help message."
    echo ""
    echo "Examples:"
    echo "  compost_bin.sh --all --force"
    echo "  compost_bin.sh --images --dry-run"
    echo "  compost_bin.sh --containers --volumes"
}

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    key="$1"
    case $key in
        -a|--all)
        PRUNE_IMAGES=1
        PRUNE_CONTAINERS=1
        PRUNE_VOLUMES=1
        shift # past argument
        ;;
        -i|--images)
        PRUNE_IMAGES=1
        shift # past argument
        ;;
        -c|--containers)
        PRUNE_CONTAINERS=1
        shift # past argument
        ;;
        -v|--volumes)
        PRUNE_VOLUMES=1
        shift # past argument
        ;;
        -f|--force)
        FORCE_PRUNE="-f"
        shift # past argument
        ;;
        -d|--dry-run)
        DRY_RUN=1
        shift # past argument
        ;;
        -h|--help)
        show_help
        exit 0
        ;;
        *)
        echo "Unknown option: $key"
        show_help
        exit 1
        ;;
    esac
done

# If no specific prune options are set, default to --all
if [[ $PRUNE_IMAGES -eq 0 && $PRUNE_CONTAINERS -eq 0 && $PRUNE_VOLUMES -eq 0 ]]; then
    PRUNE_IMAGES=1
    PRUNE_CONTAINERS=1
    PRUNE_VOLUMES=1
fi

# Function to execute or dry-run a docker command
execute_prune() {
    local cmd="$@"
    if [[ $DRY_RUN -eq 1 ]]; then
        echo "DRY RUN: Would execute: docker $cmd"
    else
        echo "Executing: docker $cmd"
        docker $cmd
        if [ $? -ne 0 ]; then
            echo "Error executing: docker $cmd" >&2
        fi
    fi
}

echo "Starting Docker Compost Bin cleanup..."

if [[ $PRUNE_IMAGES -eq 1 && $PRUNE_CONTAINERS -eq 1 && $PRUNE_VOLUMES -eq 1 ]]; then
    echo "Performing full system prune (images, containers, volumes)."
    execute_prune system prune -a $FORCE_PRUNE
else
    if [[ $PRUNE_IMAGES -eq 1 ]]; then
        echo "Pruning unused images."
        execute_prune image prune -a $FORCE_PRUNE
    fi
    if [[ $PRUNE_CONTAINERS -eq 1 ]]; then
        echo "Pruning stopped containers."
        execute_prune container prune $FORCE_PRUNE
    fi
    if [[ $PRUNE_VOLUMES -eq 1 ]]; then
        echo "Pruning dangling volumes."
        execute_prune volume prune $FORCE_PRUNE
    fi
fi

echo "Docker Compost Bin cleanup complete!"
