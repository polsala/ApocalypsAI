#!/bin/bash

# Default values
DRY_RUN=false
FORCE_PRUNE=false
PRUNE_ALL=false
PRUNE_IMAGES=false
PRUNE_VOLUMES=false
PRUNE_NETWORKS=false
PRUNE_BUILD_CACHE=false

# Whimsical header
echo "🧹 ApocalypsAI Digital Dust Bunny Sweeper 🧹"
echo "---------------------------------------------"

# Function to display help message
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "A whimsical Docker utility to sweep away digital dust bunnies (stale images, volumes, and networks) and reclaim disk space."
    echo ""
    echo "Options:"
    echo "  -a, --all             Prune all unused Docker objects (images, volumes, networks, build cache)."
    echo "  -i, --images          Prune unused images."
    echo "  -v, --volumes         Prune unused volumes."
    echo "  -n, --networks        Prune unused networks."
    echo "  -b, --build-cache     Prune build cache."
    echo "  -d, --dry-run         Show what would be pruned without actually doing it."
    echo "  -f, --force           Do not prompt for confirmation (implies -a if no specific type is given)."
    echo "  -h, --help            Display this help message."
    echo ""
    echo "If no specific prune type (-i, -v, -n, -b) is provided, --all is assumed."
    echo "Using --force without --all or specific types will default to --all."
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -a|--all) PRUNE_ALL=true ;;
        -i|--images) PRUNE_IMAGES=true ;;
        -v|--volumes) PRUNE_VOLUMES=true ;;
        -n|--networks) PRUNE_NETWORKS=true ;;
        -b|--build-cache) PRUNE_BUILD_CACHE=true ;;
        -d|--dry-run) DRY_RUN=true ;;
        -f|--force) FORCE_PRUNE=true ;;
        -h|--help) show_help; exit 0 ;;
        *) echo "Unknown option: $1"; show_help; exit 1 ;;
    esac
    shift
done

# If no specific prune type is selected, assume --all
if ! $PRUNE_IMAGES && ! $PRUNE_VOLUMES && ! $PRUNE_NETWORKS && ! $PRUNE_BUILD_CACHE && ! $PRUNE_ALL; then
    PRUNE_ALL=true
fi

# Determine docker prune options
DOCKER_PRUNE_OPTS=""
if $FORCE_PRUNE; then
    DOCKER_PRUNE_OPTS+=" --force"
fi

# Mock rationale: In a real scenario, we'd execute 'docker'. For testing, we replace 'docker' with a mock function.
# This allows us to capture arguments and simulate output without needing a Docker daemon.
# The mock function will be defined in the test script.
if [ -z "$MOCK_DOCKER" ]; then
    DOCKER_CMD="docker"
else
    DOCKER_CMD="$MOCK_DOCKER"
fi

perform_prune() {
    local type_name="$1"
    local prune_cmd="$2"
    local dry_run_msg="$3"

    echo "Sweeping $type_name..."
    if $DRY_RUN; then
        echo "  (Dry Run) Would execute: $DOCKER_CMD $prune_cmd $DOCKER_PRUNE_OPTS"
        echo "  $dry_run_msg"
    else
        echo "  Executing: $DOCKER_CMD $prune_cmd $DOCKER_PRUNE_OPTS"
        $DOCKER_CMD $prune_cmd $DOCKER_PRUNE_OPTS
        if [ $? -ne 0 ]; then
            echo "  Error sweeping $type_name."
        else
            echo "  $type_name swept clean!"
        fi
    fi
    echo ""
}

if $PRUNE_ALL; then
    perform_prune "all unused Docker objects" "system prune --all --volumes" "This would prune all unused images, containers, networks, and volumes."
else
    if $PRUNE_IMAGES; then
        perform_prune "unused images" "image prune" "This would prune all dangling images."
    fi
    if $PRUNE_VOLUMES; then
        perform_prune "unused volumes" "volume prune" "This would prune all unused local volumes."
    fi
    if $PRUNE_NETWORKS; then
        perform_prune "unused networks" "network prune" "This would prune all unused networks."
    fi
    if $PRUNE_BUILD_CACHE; then
        perform_prune "build cache" "builder prune" "This would prune the build cache."
    fi
fi

echo "---------------------------------------------"
echo "🧹 Digital dust bunnies banished! Your Docker environment is sparkling clean. ✨"
