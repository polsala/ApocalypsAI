#!/bin/bash

set -euo pipefail

# --- Helper Functions ---

log_info() {
    echo "[INFO] $@"
}

log_error() {
    echo "[ERROR] $@" >&2
}

# --- Core Functions ---

build_chamber() {
    local chamber_name="$1"
    local dockerfile_path="$2"
    shift 2
    local build_args="$@"

    if [ -z "${chamber_name}" ] || [ -z "${dockerfile_path}" ]; then
        log_error "Usage: build_chamber <chamber_name> <dockerfile_path> [docker_build_args...]"
        return 1
    fi

    log_info "Building temporal chamber: ${chamber_name} from ${dockerfile_path}"
    # Ensure the Dockerfile exists
    if [ ! -f "${dockerfile_path}" ]; then
        log_error "Dockerfile not found at: ${dockerfile_path}"
        return 1
    fi

    local dockerfile_dir
    dockerfile_dir=$(dirname "${dockerfile_path}")

    docker build -t "${chamber_name}:latest" -f "${dockerfile_path}" ${build_args} "${dockerfile_dir}"
    log_info "Chamber '${chamber_name}' built successfully."
}

run_chamber() {
    local chamber_name="$1"
    local command="$2"

    if [ -z "${chamber_name}" ] || [ -z "${command}" ]; then
        log_error "Usage: run_chamber <chamber_name> <command>"
        return 1
    fi

    log_info "Running command in chamber '${chamber_name}': ${command}"
    docker run --rm "${chamber_name}:latest" bash -c "${command}"
}

enter_chamber() {
    local chamber_name="$1"

    if [ -z "${chamber_name}" ]; then
        log_error "Usage: enter_chamber <chamber_name>"
        return 1
    fi

    log_info "Entering temporal chamber: ${chamber_name}"
    docker run -it --rm "${chamber_name}:latest"
}

list_chambers() {
    log_info "Listing available temporal chambers:"
    docker images --filter "label=description=Temporal Development Chamber Base Image" --format "{{.Repository}}	{{.Tag}}"
}

clean_chamber() {
    local chamber_name="$1"

    if [ -z "${chamber_name}" ]; then
        log_error "Usage: clean_chamber <chamber_name>"
        return 1
    fi

    log_info "Cleaning up chamber: ${chamber_name}"
    docker rmi "${chamber_name}:latest"
    log_info "Chamber '${chamber_name}' removed."
}

# --- Main Script Logic ---

if [ "$#" -eq 0 ]; then
    log_error "No command provided."
    echo "Usage: $0 <command> [args...]"
    echo "Commands: build, run, enter, list, clean"
    exit 1
fi

command="$1"
shift

case "${command}" in
    build)
        build_chamber "$@"
        ;;
    run)
        run_chamber "$@"
        ;;
    enter)
        enter_chamber "$@"
        ;;
    list)
        list_chambers
        ;;
    clean)
        clean_chamber "$@"
        ;;
    *)
        log_error "Unknown command: ${command}"
        echo "Usage: $0 <command> [args...]"
        echo "Commands: build, run, enter, list, clean"
        exit 1
        ;;
esac
