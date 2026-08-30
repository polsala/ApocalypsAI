#!/bin/bash

# Default values
PET_CONTAINERS=${PET_CONTAINERS:-}
PRUNE_ENABLED=${PRUNE_ENABLED:-"true"}
REFRESH_ENABLED=${REFRESH_ENABLED:-"false"}

log() {
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

check_health() {
  log "Checking health of pet containers..."
  if [ -z "$PET_CONTAINERS" ]; then
    log "No PET_CONTAINERS specified for health check."
    return 0
  fi

  IFS=',' read -ra ADDR <<< "$PET_CONTAINERS"
  for container_name in "${ADDR[@]}"; do
    container_name=$(echo "$container_name" | xargs) # Trim whitespace
    if [ -z "$container_name" ]; then continue; fi

    status=$(docker ps -a --filter "name=$container_name" --format "{{.Status}}" 2>/dev/null)
    if [ -z "$status" ]; then
      log "Critter '$container_name' not found."
    elif [[ "$status" == *"Up"* ]]; then
      log "Critter '$container_name' is healthy: $status"
    else
      log "Critter '$container_name' is unwell: $status"
      # Optionally, try to restart
      if [ "$REFRESH_ENABLED" = "true" ]; then
        log "Attempting to refresh unwell critter '$container_name'..."
        docker restart "$container_name" 2>/dev/null
        if [ $? -eq 0 ]; then
          log "Critter '$container_name' refreshed successfully."
        else
          log "Failed to refresh critter '$container_name'."
        fi
      fi
    fi
  done
}

perform_prune() {
  if [ "$PRUNE_ENABLED" = "true" ]; then
    log "Grooming the Docker environment (pruning unused images, volumes, networks)..."
    docker system prune -af --volumes
    log "Grooming complete."
  else
    log "Pruning is disabled."
  fi
}

main() {
  log "Starting Nightly Container Critter Caretaker..."
  check_health
  perform_prune
  log "Nightly Container Critter Caretaker finished."
}

main "$@"
