#!/bin/bash

set -euo pipefail

# Helper function for logging
log() {
  echo "[PocketDimension] $@" >&2
}

# Ensure docker is available
if ! command -v docker &> /dev/null; then
    log "Error: Docker CLI not found. Please ensure Docker is installed and accessible."
    exit 1
fi

# Function to generate consistent names
get_container_name() {
  echo "pd-$1"
}

get_volume_name() {
  echo "pd-$1-vol"
}

# --- Commands ---

cmd_create() {
  local dimension_name="$1"
  local image="$2"

  if [ -z "$dimension_name" ] || [ -z "$image" ]; then
    log "Usage: create <dimension_name> <image>"
    exit 1
  fi

  local container_name=$(get_container_name "$dimension_name")
  local volume_name=$(get_volume_name "$dimension_name")

  if docker ps -a --format "{{.Names}}" | grep -q "^${container_name}$"; then
    log "Error: Dimension '$dimension_name' (container '$container_name') already exists."
    exit 1
  fi

  log "Creating volume '$volume_name'...
"
  docker volume create "$volume_name" > /dev/null

  log "Creating and starting container '$container_name' from image '$image'...
"
  docker run -d \
    --name "$container_name" \
    -v "$volume_name":/data \
    "$image" \
    tail -f /dev/null # Keep container running
  log "Dimension '$dimension_name' created successfully."
}

cmd_enter() {
  local dimension_name="$1"

  if [ -z "$dimension_name" ]; then
    log "Usage: enter <dimension_name>"
    exit 1
  fi

  local container_name=$(get_container_name "$dimension_name")

  if ! docker ps --format "{{.Names}}" | grep -q "^${container_name}$"; then
    log "Error: Dimension '$dimension_name' (container '$container_name') is not running or does not exist."
    log "Use 'create' to make it, or 'docker start $container_name' if it's stopped."
    exit 1
  fi

  log "Entering dimension '$dimension_name'...
"
  docker exec -it "$container_name" bash || docker exec -it "$container_name" sh
}

cmd_run() {
  local dimension_name="$1"
  shift
  local command_to_run="$@"

  if [ -z "$dimension_name" ] || [ -z "$command_to_run" ]; then
    log "Usage: run <dimension_name> <command...>"
    exit 1
  fi

  local container_name=$(get_container_name "$dimension_name")

  if ! docker ps --format "{{.Names}}" | grep -q "^${container_name}$"; then
    log "Error: Dimension '$dimension_name' (container '$container_name') is not running or does not exist."
    log "Use 'create' to make it, or 'docker start $container_name' if it's stopped."
    exit 1
  fi

  log "Running command in dimension '$dimension_name': $command_to_run
"
  docker exec "$container_name" bash -c "$command_to_run" || docker exec "$container_name" sh -c "$command_to_run"
}

cmd_snapshot() {
  local dimension_name="$1"
  local snapshot_tag="$2"

  if [ -z "$dimension_name" ] || [ -z "$snapshot_tag" ]; then
    log "Usage: snapshot <dimension_name> <snapshot_tag>"
    exit 1
  fi

  local container_name=$(get_container_name "$dimension_name")

  if ! docker ps -a --format "{{.Names}}" | grep -q "^${container_name}$"; then
    log "Error: Dimension '$dimension_name' (container '$container_name') does not exist."
    exit 1
  fi

  log "Creating snapshot '$snapshot_tag' for dimension '$dimension_name'...
"
  docker commit "$container_name" "$snapshot_tag" > /dev/null
  log "Snapshot '$snapshot_tag' created successfully."
}

cmd_list() {
  log "Active Pocket Dimensions:"
  echo "------------------------"
  docker ps -a --filter "name=^pd-" --format "table {{.Names}}\t{{.Image}}\t{{.Status}}" | sed 's/pd-//' | column -t
  echo "------------------------"
}

cmd_destroy() {
  local dimension_name="$1"

  if [ -z "$dimension_name" ]; then
    log "Usage: destroy <dimension_name>"
    exit 1
  fi

  local container_name=$(get_container_name "$dimension_name")
  local volume_name=$(get_volume_name "$dimension_name")

  if ! docker ps -a --format "{{.Names}}" | grep -q "^${container_name}$"; then
    log "Warning: Dimension '$dimension_name' (container '$container_name') does not exist. Skipping container removal."
  else
    log "Stopping and removing container '$container_name'...
"
    docker stop "$container_name" > /dev/null || true # Ignore if already stopped
    docker rm "$container_name" > /dev/null
    log "Container '$container_name' removed."
  fi

  if ! docker volume ls --format "{{.Name}}" | grep -q "^${volume_name}$"; then
    log "Warning: Volume '$volume_name' does not exist. Skipping volume removal."
  else
    log "Removing volume '$volume_name'...
"
    docker volume rm "$volume_name" > /dev/null
    log "Volume '$volume_name' removed."
  fi

  log "Dimension '$dimension_name' destroyed."
}

cmd_help() {
  echo "Usage: pocket-dimension-manager <command> [arguments]"
  echo ""
  echo "Commands:"
  echo "  create <dimension_name> <image>        Create a new pocket dimension."
  echo "  enter <dimension_name>                 Enter an interactive shell in a dimension."
  echo "  run <dimension_name> <command...>      Execute a command in a dimension."
  echo "  snapshot <dimension_name> <snapshot_tag> Create an image snapshot of a dimension."
  echo "  list                                   List all active pocket dimensions."
  echo "  destroy <dimension_name>               Destroy a pocket dimension (container and volume)."
  echo "  --help                                 Show this help message."
  echo ""
  echo "Example:"
  echo "  docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \\"
  echo "    apocalypsai/pocket-dimension-manager create my-dev-env ubuntu:latest"
}

# --- Main logic ---
case "$1" in
  create)
    shift
    cmd_create "$@"
    ;;
  enter)
    shift
    cmd_enter "$@"
    ;;
  run)
    shift
    cmd_run "$@"
    ;;
  snapshot)
    shift
    cmd_snapshot "$@"
    ;;
  list)
    cmd_list
    ;;
  destroy)
    shift
    cmd_destroy "$@"
    ;;
  --help|-h)
    cmd_help
    ;;
  *)
    log "Error: Unknown command '$1'"
    cmd_help
    exit 1
    ;;
esac
