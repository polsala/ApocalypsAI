#!/bin/bash

set -euo pipefail

ECHOES_DIR="/app/echoes"

mkdir -p "${ECHOES_DIR}"

function show_help() {
    echo "Usage: echo-cli <command> [arguments]"
    echo ""
    echo "Commands:"
    echo "  capture <container_name_or_id> <echo_name>  - Captures envs and volumes of a running container."
    echo "  replay <echo_name> <image_name> [command...] - Launches a new container with captured config."
    echo "  list                                        - Lists all saved echoes."
    echo "  delete <echo_name>                          - Deletes a saved echo."
    echo "  --help                                      - Show this help message."
}

function capture_echo() {
    local container_id="$1"
    local echo_name="$2"

    if [[ -z "${container_id}" || -z "${echo_name}" ]]; then
        echo "Error: Both container ID/name and echo name are required for 'capture'." >&2
        show_help
        exit 1
    fi

    local echo_file="${ECHOES_DIR}/${echo_name}.json"

    if [[ -f "${echo_file}" ]]; then
        echo "Warning: Echo '${echo_name}' already exists. Overwriting." >&2
    fi

    echo "Inspecting container '${container_id}'..."
    local inspect_output
    inspect_output=$(docker inspect "${container_id}" 2>&1)

    if [[ $? -ne 0 ]]; then
        echo "Error inspecting container: ${inspect_output}" >&2
        exit 1
    fi

    local env_vars
    env_vars=$(echo "${inspect_output}" | jq -r '.[0].Config.Env[]' | sed 's/^/"/;s/=/"\:"/;s/$/"/' | paste -sd, -)

    local volumes_raw
    volumes_raw=$(echo "${inspect_output}" | jq -r '.[0].HostConfig.Binds[]?')

    local volumes_array=()
    if [[ -n "${volumes_raw}" ]]; then
        while IFS= read -r line; do
            volumes_array+=("\"${line}\"")
        done <<< "${volumes_raw}"
    fi
    local volumes_json=$(IFS=,; echo "${volumes_array[*]}")

    cat <<EOF > "${echo_file}"
{
  "env_vars": {
    $(echo "${env_vars}" | sed 's/,/,
    /g')
  },
  "volumes": [
    $(echo "${volumes_json}" | sed 's/,/,
    /g')
  ]
}
EOF

    echo "Echo '${echo_name}' captured successfully to '${echo_file}'."
}

function replay_echo() {
    local echo_name="$1"
    local image_name="$2"
    shift 2
    local cmd_args="$@"

    if [[ -z "${echo_name}" || -z "${image_name}" ]]; then
        echo "Error: Echo name and image name are required for 'replay'." >&2
        show_help
        exit 1
    }

    local echo_file="${ECHOES_DIR}/${echo_name}.json"

    if [[ ! -f "${echo_file}" ]]; then
        echo "Error: Echo '${echo_name}' not found at '${echo_file}'." >&2
        exit 1
    }

    echo "Loading echo '${echo_name}' from '${echo_file}'..."
    local env_json
    env_json=$(jq -r '.env_vars | to_entries[] | .key + "=" + .value' "${echo_file}")

    local volume_json
    volume_json=$(jq -r '.volumes[]' "${echo_file}")

    local docker_run_cmd=("docker" "run" "--rm")

    while IFS= read -r env_var; do
        docker_run_cmd+=("-e" "${env_var}")
    done <<< "${env_json}"

    while IFS= read -r volume_bind; do
        docker_run_cmd+=("-v" "${volume_bind}")
    done <<< "${volume_json}"

    docker_run_cmd+=("${image_name}")

    if [[ -n "${cmd_args}" ]]; then
        docker_run_cmd+=(${cmd_args})
    fi

    echo "Replaying echo '${echo_name}' with image '${image_name}'..."
    echo "Executing: ${docker_run_cmd[*]}"
    # Execute the constructed docker run command
    "${docker_run_cmd[@]}"
}

function list_echoes() {
    echo "Available Temporal Echoes:"
    local count=0
    for echo_file in "${ECHOES_DIR}"/*.json; do
        if [[ -f "${echo_file}" ]]; then
            echo "- $(basename "${echo_file}" .json)"
            count=$((count + 1))
        fi
    done
    if [[ "${count}" -eq 0 ]]; then
        echo "  (No echoes found)"
    fi
}

function delete_echo() {
    local echo_name="$1"

    if [[ -z "${echo_name}" ]]; then
        echo "Error: Echo name is required for 'delete'." >&2
        show_help
        exit 1
    fi

    local echo_file="${ECHOES_DIR}/${echo_name}.json"

    if [[ ! -f "${echo_file}" ]]; then
        echo "Error: Echo '${echo_name}' not found at '${echo_file}'." >&2
        exit 1
    fi

    rm "${echo_file}"
    echo "Echo '${echo_name}' deleted successfully."
}

case "$1" in
    "capture")
        shift
        capture_echo "$@"
        ;;
    "replay")
        shift
        replay_echo "$@"
        ;;
    "list")
        list_echoes
        ;;
    "delete")
        shift
        delete_echo "$@"
        ;;
    "--help"|-h)
        show_help
        ;;
    *)
        echo "Error: Unknown command '$1'." >&2
        show_help
        exit 1
        ;;
esac
