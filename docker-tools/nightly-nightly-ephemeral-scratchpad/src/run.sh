#!/bin/bash

# --- Configuration ---
IMAGE_NAME="apocalypsai/ephemeral-scratchpad"
CONTAINER_NAME_PREFIX="apocalypsai-scratchpad-"
TEMP_DIR_PREFIX="apocalypsai_scratchpad_"

# --- Functions ---
log_info() {
    echo "INFO: $1"
}

log_error() {
    echo "ERROR: $1" >&2
}

# --- Pre-checks ---
if ! command -v docker &> /dev/null; then
    log_error "Docker is not installed. Please install Docker to use this utility."
    exit 1
fi

# --- Build Image (if not exists) ---
if [[ "$(docker images -q $IMAGE_NAME 2> /dev/null)" == "" ]]; then
    log_info "Docker image '$IMAGE_NAME' not found. Building it now..."
    docker build -t $IMAGE_NAME . || {
        log_error "Failed to build Docker image '$IMAGE_NAME'."
        exit 1
    }
    log_info "Image '$IMAGE_NAME' built successfully."
else
    log_info "Docker image '$IMAGE_NAME' already exists."
fi

# --- Prepare Temporary Directory ---
HOST_TEMP_DIR=$(mktemp -d -t ${TEMP_DIR_PREFIX}XXXXXX)
if [ $? -ne 0 ]; then
    log_error "Failed to create a temporary directory on the host."
    exit 1
fi
log_info "Created temporary host directory: $HOST_TEMP_DIR"

# Ensure cleanup on exit
cleanup() {
    log_info "Cleaning up temporary host directory: $HOST_TEMP_DIR"
    rm -rf "$HOST_TEMP_DIR"
    log_info "Cleanup complete."
}
trap cleanup EXIT

# --- Run Container ---
log_info "Launching ephemeral scratchpad container..."
log_info "Your current directory will be mounted to /scratchpad/current_dir (read-only) inside the container."
log_info "Any files you create or modify in /scratchpad/host_mount will persist on your host at $HOST_TEMP_DIR until cleanup."

# Generate a unique container name
CONTAINER_NAME="${CONTAINER_NAME_PREFIX}$(date +%s)"

docker run \
    --name "$CONTAINER_NAME" \
    -it \
    --rm \
    -v "$(pwd):/scratchpad/current_dir:ro" \
    -v "$HOST_TEMP_DIR:/scratchpad/host_mount" \
    $IMAGE_NAME "$@"

if [ $? -ne 0 ]; then
    log_error "Container exited with an error."
    exit 1
fi

log_info "Ephemeral scratchpad session ended."
# Cleanup will be triggered by the trap EXIT
