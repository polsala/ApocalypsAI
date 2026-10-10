#!/bin/bash

set -euo pipefail

SNAPSHOT_BASE_DIR="/snapshots" # This directory will be mounted from the 'temporal-echo-data' volume
DOCKER_SOCKET="/var/run/docker.sock"

# Helper function to run docker commands from within the container
# This requires the host's docker socket to be mounted into this container.
run_docker_cmd() {
    docker -H unix://${DOCKER_SOCKET} "$@"
}

# Function to check if a volume exists on the host Docker daemon
volume_exists() {
    local volume_name="$1"
    run_docker_cmd volume inspect "${volume_name}" > /dev/null 2>&1
}

# Function to create a temporary container to interact with a target volume
create_temp_container() {
    local volume_name="$1"
    local container_name="temp-volume-echo-$(date +%s%N)"

    echo "Creating temporary container '${container_name}' to access volume '${volume_name}'..." >&2
    run_docker_cmd run --rm -d \
        --name "${container_name}" \
        -v "${volume_name}":/target_volume \
        alpine:latest sleep infinity > /dev/null

    echo "${container_name}"
}

# Function to remove a temporary container
remove_temp_container() {
    local container_name="$1"
    echo "Removing temporary container '${container_name}'..." >&2
    run_docker_cmd rm -f "${container_name}" > /dev/null
}

# Command: capture <volume_name> [snapshot_name]
cmd_capture() {
    local volume_name="$1"
    local snapshot_name="${2:-$(date +%Y%m%d%H%M%S)}" # Default to timestamp if not provided

    if ! volume_exists "${volume_name}"; then
        echo "Error: Docker volume '${volume_name}' does not exist." >&2
        exit 1
    fi

    local volume_snapshot_dir="${SNAPSHOT_BASE_DIR}/${volume_name}"
    mkdir -p "${volume_snapshot_dir}"

    local snapshot_file="${volume_snapshot_dir}/${snapshot_name}.tar.gz"

    echo "Capturing echo for volume '${volume_name}' as '${snapshot_name}'..."

    local temp_container_id=$(create_temp_container "${volume_name}")
    
    # Execute tar inside the temporary container to archive the volume contents to stdout,
    # then redirect that stdout to a file on the host (via the mounted /snapshots volume).
    run_docker_cmd exec "${temp_container_id}" tar -czf - -C /target_volume . > "${snapshot_file}"

    remove_temp_container "${temp_container_id}"

    echo "Echo captured successfully to ${snapshot_file}"
}

# Command: list <volume_name>
cmd_list() {
    local volume_name="$1"

    local volume_snapshot_dir="${SNAPSHOT_BASE_DIR}/${volume_name}"

    if [ ! -d "${volume_snapshot_dir}" ]; then
        echo "No echoes found for volume '${volume_name}'."
        exit 0
    fi

    echo "Temporal Echoes for volume '${volume_name}':"
    find "${volume_snapshot_dir}" -maxdepth 1 -type f -name "*.tar.gz" -printf "%f\n" | sed 's/\.tar\.gz$//' | sort
}

# Command: restore <volume_name> <snapshot_name>
cmd_restore() {
    local volume_name="$1"
    local snapshot_name="$2"

    if [ -z "${snapshot_name}" ]; then
        echo "Error: Snapshot name is required for restore command." >&2
        exit 1
    }

    if ! volume_exists "${volume_name}"; then
        echo "Error: Docker volume '${volume_name}' does not exist." >&2
        exit 1
    fi

    local snapshot_file="${SNAPSHOT_BASE_DIR}/${volume_name}/${snapshot_name}.tar.gz"

    if [ ! -f "${snapshot_file}" ]; then
        echo "Error: Snapshot '${snapshot_name}' not found for volume '${volume_name}'." >&2
        exit 1
    fi

    echo "Restoring volume '${volume_name}' from echo '${snapshot_name}'..."

    local temp_container_id=$(create_temp_container "${volume_name}")

    # Clear existing contents of the target volume inside the temporary container
    echo "Clearing existing contents of volume '${volume_name}'..." >&2
    run_docker_cmd exec "${temp_container_id}" sh -c "rm -rf /target_volume/* /target_volume/.* 2>/dev/null || true"

    # Pipe the snapshot file's content into tar -xzf - running inside the temporary container,
    # extracting it to the target volume.
    echo "Extracting snapshot contents..." >&2
    run_docker_cmd exec -i "${temp_container_id}" tar -xzf - -C /target_volume < "${snapshot_file}"

    remove_temp_container "${temp_container_id}"

    echo "Volume '${volume_name}' restored successfully from echo '${snapshot_name}'."
}

# Main script logic
case "$1" in
    capture)
        shift
        cmd_capture "$@"
        ;;
    list)
        shift
        cmd_list "$@"
        ;;
    restore)
        shift
        cmd_restore "$@"
        ;;
    help|--help|-h|"")
        echo "Usage: echo_manager.sh <command> <volume_name> [snapshot_name]"
        echo ""
        echo "Commands:"
        echo "  capture <volume_name> [snapshot_name] - Capture a snapshot of a Docker volume."
        echo "  list <volume_name>                  - List available snapshots for a Docker volume."
        echo "  restore <volume_name> <snapshot_name> - Restore a Docker volume from a snapshot."
        echo ""
        echo "Requires Docker daemon access via /var/run/docker.sock and 'temporal-echo-data' volume mounted at /snapshots."
        exit 0
        ;;
    *)
        echo "Error: Unknown command '$1'" >&2
        exit 1
        ;;
esac
