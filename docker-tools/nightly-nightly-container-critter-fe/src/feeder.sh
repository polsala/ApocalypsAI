#!/bin/bash

# Default interval in seconds
INTERVAL=${FEED_INTERVAL:-10}
# Containers to monitor (space-separated list of names or IDs)
MONITORED_CONTAINERS=${CRITTER_NAMES:-""} # If empty, monitor all non-critter-feeder containers

log() {
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $@"
}

# Function to perform a single round of monitoring and feeding
perform_single_round() {
  log "Checking on the critters..."
  
  local containers_to_check
  if [ -z "$MONITORED_CONTAINERS" ]; then
    # Monitor all containers except self
    containers_to_check=$(docker ps -a --format "{{.Names}}" | grep -v "critter-feeder")
  else
    containers_to_check="$MONITORED_CONTAINERS"
  fi

  for critter_name in $containers_to_check; do
    if [ -z "$critter_name" ]; then
      continue
    end

    local status=$(docker inspect --format '{{.State.Status}}' "$critter_name" 2>/dev/null)
    local running=$(docker inspect --format '{{.State.Running}}' "$critter_name" 2>/dev/null)
    local health=$(docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}n/a{{end}}' "$critter_name" 2>/dev/null)

    if [ -z "$status" ]; then
      log "Critter '$critter_name' not found or already removed. Skipping."
      continue
    fi

    log "Critter '$critter_name' status: $status, running: $running, health: $health"

    if [ "$status" == "exited" ] || [ "$running" == "false" ] || [ "$health" == "unhealthy" ]; then
      log "Critter '$critter_name' seems unwell ($status, $health). Attempting to feed (restart)..."
      if docker restart "$critter_name"; then
        log "Successfully fed (restarted) critter '$critter_name'."
      else
        log "Failed to feed (restart) critter '$critter_name'. It might be beyond help."
      fi
    else
      log "Critter '$critter_name' is happy and healthy."
    fi
  done
}

# Main loop for the feeder
main_feeder_loop() {
  log "Critter Feeder starting its rounds (interval: ${INTERVAL}s)..."
  while true; do
    perform_single_round
    sleep "$INTERVAL"
  done
}

# If this script is sourced, only define functions. If executed, run the main loop.
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main_feeder_loop
fi
