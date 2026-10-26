#!/bin/bash

set -e

CONTAINER_BASE_IMAGE="" # Stored for cleanup
CONTAINER_NAME=""
SNAPSHOT_PREFIX=""

# Function to check if a container exists
_container_exists() {
    docker ps -a --format "{{.Names}}" | grep -q "^$1$"
}

# Function to check if an image exists
_image_exists() {
    docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "^$1$"
}

# Function to stop and remove a container if it exists
_stop_and_remove_container() {
    if _container_exists "$1"; then
        echo "Stopping and removing container: $1"
        docker stop "$1" > /dev/null 2>&1 || true
        docker rm "$1" > /dev/null 2>&1 || true
    fi
}

# Function to remove an image if it exists
_remove_image() {
    if _image_exists "$1"; then
        echo "Removing image: $1"
        docker rmi "$1" > /dev/null 2>&1 || true
    fi
}

# --- Commands ---

cmd_init() {
    local base_image="$1"
    local container_name="$2"
    if [ -z "$base_image" ] || [ -z "$container_name" ]; then
        echo "Usage: init <base_image> <container_name>"
        exit 1
    }

    CONTAINER_BASE_IMAGE="$base_image"
    CONTAINER_NAME="$container_name"
    SNAPSHOT_PREFIX="${container_name}-snapshot"

    echo "Initializing Temporal Echo Chamber for container: $container_name from image: $base_image"

    # Ensure no existing container or initial snapshot
    _stop_and_remove_container "$container_name"
    _remove_image "${SNAPSHOT_PREFIX}-initial"

    echo "Pulling base image: $base_image"
    docker pull "$base_image" > /dev/null

    echo "Creating initial container: $container_name"
    docker run -d --name "$container_name" "$base_image" sleep infinity > /dev/null

    echo "Taking initial snapshot: ${SNAPSHOT_PREFIX}-initial"
    docker commit "$container_name" "${SNAPSHOT_PREFIX}-initial" > /dev/null
    echo "Initialization complete. Container '$container_name' is running."
}

cmd_snapshot() {
    local container_name="$1"
    local snapshot_tag="$2"
    if [ -z "$container_name" ] || [ -z "$snapshot_tag" ]; then
        echo "Usage: snapshot <container_name> <snapshot_tag>"
        exit 1
    }

    SNAPSHOT_PREFIX="${container_name}-snapshot"
    local full_snapshot_tag="${SNAPSHOT_PREFIX}-${snapshot_tag}"

    if ! _container_exists "$container_name"; then
        echo "Error: Container '$container_name' does not exist or is not running. Please 'init' first."
        exit 1
    }

    echo "Taking snapshot of '$container_name' as image: $full_snapshot_tag"
    _remove_image "$full_snapshot_tag" # Remove if exists to avoid conflicts
    docker commit "$container_name" "$full_snapshot_tag" > /dev/null
    echo "Snapshot '$snapshot_tag' created."
}

cmd_rewind() {
    local container_name="$1"
    local snapshot_tag="$2"
    if [ -z "$container_name" ] || [ -z "$snapshot_tag" ]; then
        echo "Usage: rewind <container_name> <snapshot_tag>"
        exit 1
    }

    SNAPSHOT_PREFIX="${container_name}-snapshot"
    local full_snapshot_tag="${SNAPSHOT_PREFIX}-${snapshot_tag}"

    if ! _image_exists "$full_snapshot_tag"; then
        echo "Error: Snapshot image '$full_snapshot_tag' does not exist. Please take a snapshot first."
        exit 1
    }

    echo "Rewinding container '$container_name' to snapshot: $full_snapshot_tag"
    _stop_and_remove_container "$container_name"

    echo "Recreating container '$container_name' from snapshot image."
    docker run -d --name "$container_name" "$full_snapshot_tag" sleep infinity > /dev/null
    echo "Rewind complete. Container '$container_name' is running from snapshot '$snapshot_tag'."
}

cmd_run() {
    local container_name="$1"
    shift
    local command="$@"
    if [ -z "$container_name" ] || [ -z "$command" ]; then
        echo "Usage: run <container_name> <command>"
        exit 1
    }

    if ! _container_exists "$container_name"; then
        echo "Error: Container '$container_name' does not exist or is not running. Please 'init' first."
        exit 1
    }

    echo "Running command in '$container_name': $command"
    docker exec "$container_name" sh -c "$command"
}

cmd_cleanup() {
    local container_name="$1"
    if [ -z "$container_name" ]; then
        echo "Usage: cleanup <container_name>"
        exit 1
    }

    SNAPSHOT_PREFIX="${container_name}-snapshot"

    echo "Cleaning up Temporal Echo Chamber for container: $container_name"
    _stop_and_remove_container "$container_name"

    # Remove all images starting with the snapshot prefix
    echo "Removing associated snapshot images..."
    docker images --format "{{.Repository}}:{{.Tag}}" | grep "^${SNAPSHOT_PREFIX}-" | while read -r img; do
        _remove_image "$img"
    done
    echo "Cleanup complete."
}

# Main script logic
case "$1" in
    init)
        cmd_init "$2" "$3"
        ;;
    snapshot)
        cmd_snapshot "$2" "$3"
        ;;
    rewind)
        cmd_rewind "$2" "$3"
        ;;
    run)
        shift # remove 'run'
        local container_name_for_run="$1"
        shift # remove container_name
        cmd_run "$container_name_for_run" "$@"
        ;;
    cleanup)
        cmd_cleanup "$2"
        ;;
    *)
        echo "Usage: $0 {init|snapshot|rewind|run|cleanup} ..."
        exit 1
        ;;
esac
