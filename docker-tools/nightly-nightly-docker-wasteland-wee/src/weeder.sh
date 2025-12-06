#!/bin/bash

# Default docker command, can be overridden for testing
DOCKER_CMD="${DOCKER_CMD:-docker}"

DRY_RUN=false
FORCE=false
PRUNE_IMAGES=false
PRUNE_CONTAINERS=false
PRUNE_VOLUMES=false
PRUNE_BUILD_CACHE=false
PRUNE_ALL=true # Default to pruning all if no specific flags are given

show_help() {
    echo "Usage: weeder.sh [OPTIONS]"
    echo "A containerized utility to prune unused Docker resources."
    echo ""
    echo "Options:"
    echo "  --dry-run             Show what would be pruned without actually removing anything."
    echo "  --force               Do not ask for confirmation before pruning."
    echo "  --images              Prune only dangling images."
    echo "  --containers          Prune only stopped containers."
    echo "  --volumes             Prune only unused volumes."
    echo "  --build-cache         Prune only build cache."
    echo "  --all                 Prune all (images, containers, volumes, build cache). This is the default."
    echo "  --help                Display this help message."
    echo ""
    echo "To run this utility, you typically mount the Docker socket:"
    echo "  docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-wasteland-weeder --dry-run"
    echo "  docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-wasteland-weeder --force --all"
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --dry-run) DRY_RUN=true; shift ;;
        --force) FORCE=true; shift ;;
        --images) PRUNE_IMAGES=true; PRUNE_ALL=false; shift ;;
        --containers) PRUNE_CONTAINERS=true; PRUNE_ALL=false; shift ;;
        --volumes) PRUNE_VOLUMES=true; PRUNE_ALL=false; shift ;;
        --build-cache) PRUNE_BUILD_CACHE=true; PRUNE_ALL=false; shift ;;
        --all) PRUNE_ALL=true; PRUNE_IMAGES=false; PRUNE_CONTAINERS=false; PRUNE_VOLUMES=false; PRUNE_BUILD_CACHE=false; shift ;;
        --help) show_help; exit 0 ;;
        *) echo "Unknown parameter: $1"; show_help; exit 1 ;;
    esac
done

# If no specific prune flags are set and --all is not explicitly set, default to --all
if [ "$PRUNE_IMAGES" = false ] && [ "$PRUNE_CONTAINERS" = false ] && [ "$PRUNE_VOLUMES" = false ] && [ "$PRUNE_BUILD_CACHE" = false ] && [ "$PRUNE_ALL" = false ]; then
    PRUNE_ALL=true
fi

if [ "$DRY_RUN" = true ]; then
    echo "Performing dry run..."
    if [ "$PRUNE_ALL" = true ] || [ "$PRUNE_IMAGES" = true ]; then
        echo "-- Dangling Images --"
        "$DOCKER_CMD" images -f dangling=true
    fi
    if [ "$PRUNE_ALL" = true ] || [ "$PRUNE_CONTAINERS" = true ]; then
        echo "-- Stopped Containers --"
        "$DOCKER_CMD" ps -a -f status=exited
    fi
    if [ "$PRUNE_ALL" = true ] || [ "$PRUNE_VOLUMES" = true ]; then
        echo "-- Unused Volumes --"
        "$DOCKER_CMD" volume ls -f dangling=true
    fi
    if [ "$PRUNE_ALL" = true ] || [ "$PRUNE_BUILD_CACHE" = true ]; then
        echo "-- Build Cache (approximate) --"
        # Mock rationale: 'docker builder prune --dry-run' is not a standard command.
        # For dry-run, we indicate that build cache would be considered.
        echo "  (Running 'docker builder prune' would reclaim space from build cache.)"
    fi
    echo "Dry run complete. No resources were removed."
else
    if [ "$FORCE" = false ]; then
        read -p "This will remove selected unused Docker resources. Are you sure? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Aborting."
            exit 1
        fi
    fi

    echo "Pruning Docker wasteland..."
    if [ "$PRUNE_ALL" = true ]; then
        "$DOCKER_CMD" system prune --force --volumes --all
    else
        if [ "$PRUNE_IMAGES" = true ]; then
            echo "Pruning dangling images..."
            "$DOCKER_CMD" image prune --force
        fi
        if [ "$PRUNE_CONTAINERS" = true ]; then
            echo "Pruning stopped containers..."
            "$DOCKER_CMD" container prune --force
        fi
        if [ "$PRUNE_VOLUMES" = true ]; then
            echo "Pruning unused volumes..."
            "$DOCKER_CMD" volume prune --force
        fi
        if [ "$PRUNE_BUILD_CACHE" = true ]; then
            echo "Pruning build cache..."
            "$DOCKER_CMD" builder prune --force
        fi
    fi
    echo "Wasteland weeded!"
fi
