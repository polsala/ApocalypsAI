#!/bin/bash

set -euo pipefail

# Configuration
OASIS_NAME="nightly-oasis-shell"
COMPOSE_FILE="$(dirname \"$0\")"/docker-compose.yml
WORK_DIR="$(dirname \"$0\")"/work

# Mock rationale: For testing purposes, we can override DOCKER_COMPOSE_CMD
# to point to a mock function instead of the real docker-compose binary.
# This allows deterministic, offline tests without requiring a Docker daemon.
: ${DOCKER_COMPOSE_CMD:=docker-compose}

log() {
    echo "[OasisAI] $*"
}

ensure_work_dir() {
    if [ ! -d "$WORK_DIR" ]; then
        log "Creating work directory: $WORK_DIR"
        mkdir -p "$WORK_DIR"
    fi
}

create_oasis() {
    log "Creating Ephemeral Dev Oasis '$OASIS_NAME'..."
    ensure_work_dir
    log "Building Docker image..."
    if ! $DOCKER_COMPOSE_CMD -f "$COMPOSE_FILE" build;
    then
        log "Error: Docker image build failed."
        exit 1
    fi
    log "Starting container '$OASIS_NAME' in detached mode..."
    if ! $DOCKER_COMPOSE_CMD -f "$COMPOSE_FILE" up -d;
    then
        log "Error: Docker container failed to start."
        exit 1
    fi
    log "Oasis '$OASIS_NAME' created and running. Use './src/oasis.sh enter' to access it."
}

enter_oasis() {
    log "Entering Ephemeral Dev Oasis '$OASIS_NAME'..."
    if ! $DOCKER_COMPOSE_CMD -f "$COMPOSE_FILE" ps --services --filter "status=running" | grep -q "oasis-shell"; then
        log "Error: Oasis '$OASIS_NAME' is not running. Please 'create' it first."
        exit 1
    fi
    log "Attaching to '$OASIS_NAME'. Type 'exit' or Ctrl+D to detach."
    # Use docker exec for a new shell, allowing multiple 'enter' sessions
    # and better handling of detached exits.
    docker exec -it "$OASIS_NAME" bash
    log "Exited Oasis '$OASIS_NAME'."
}

destroy_oasis() {
    log "Dismantling Ephemeral Dev Oasis '$OASIS_NAME'..."
    if ! $DOCKER_COMPOSE_CMD -f "$COMPOSE_FILE" down;
    then
        log "Error: Failed to stop and remove container '$OASIS_NAME'. It might not be running."
        exit 1
    fi
    log "Oasis '$OASIS_NAME' dismantled. Local work directory '$WORK_DIR' remains intact."
}

list_oasis() {
    log "Listing Ephemeral Dev Oasis status..."
    $DOCKER_COMPOSE_CMD -f "$COMPOSE_FILE" ps
}

case "$1" in
    create)
        create_oasis
        ;;
    enter)
        enter_oasis
        ;;
    destroy)
        destroy_oasis
        ;;
    list)
        list_oasis
        ;;
    *)
        log "Usage: $0 {create|enter|destroy|list}"
        exit 1
        ;;
esac
