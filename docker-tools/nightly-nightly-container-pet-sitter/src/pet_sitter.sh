#!/bin/sh

# Nightly Container Pet Sitter
# Monitors specified Docker containers, restarts them if stopped, and reports resource usage.

# --- Configuration Defaults ---
PET_CONTAINERS="${PET_CONTAINERS:-}" # Comma-separated list of container names/IDs
RESTART_ON_STOP="${RESTART_ON_STOP:-false}" # Set to 'true' to restart stopped containers
CHECK_INTERVAL_SECONDS="${CHECK_INTERVAL_SECONDS:-60}" # How often to check (in seconds)

# --- Helper Functions ---
log_message() {
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# --- Main Loop ---
log_message "Nightly Container Pet Sitter is starting up..."

if [ -z "$PET_CONTAINERS" ]; then
  log_message "ERROR: PET_CONTAINERS environment variable is not set. No pets to sit!"
  exit 1
fi

# Convert comma-separated string to an array of container names
IFS=',' read -r -a container_names_array <<< "$PET_CONTAINERS"

while true; do
  log_message "Nightly Container Pet Sitter is making its rounds..."

  for container_name in "${container_names_array[@]}"; do
    container_name=$(echo "$container_name" | xargs) # Trim whitespace
    if [ -z "$container_name" ]; then
      continue
    }

    log_message "Checking on pet: $container_name"

    # Get container ID and status
    # Mock rationale: In tests, 'docker inspect' is mocked to return predefined ID and status.
    container_info=$(docker inspect -f '{{.ID}} {{.State.Status}}' "$container_name" 2>/dev/null)
    if [ $? -ne 0 ]; then
      log_message "WARNING: Pet '$container_name' not found or Docker daemon inaccessible. Skipping."
      continue
    fi

    container_id=$(echo "$container_info" | awk '{print $1}')
    container_status=$(echo "$container_info" | awk '{print $2}')

    case "$container_status" in
      "running")
        log_message "Pet '$container_name' is happily purring."
        # Get resource usage
        # Mock rationale: In tests, 'docker stats' is mocked to return fixed CPU/Mem values.
        stats=$(docker stats --no-stream --format "{{.CPUPerc}}\t{{.MemUsage}}" "$container_id" 2>/dev/null)
        if [ $? -eq 0 ] && [ -n "$stats" ]; then
          cpu_perc=$(echo "$stats" | awk '{print $1}')
          mem_usage=$(echo "$stats" | awk '{print $2}')
          log_message "  CPU: ${cpu_perc}, Mem: ${mem_usage}"
        else
          log_message "  Could not retrieve resource stats for '$container_name'."
        fi
        ;;
      "exited")
        log_message "Pet '$container_name' found sleeping."
        if [ "$RESTART_ON_STOP" = "true" ]; then
          log_message "  Attempting to wake up '$container_name'...";
          # Mock rationale: In tests, 'docker start' is mocked to always succeed.
          if docker start "$container_id" >/dev/null 2>&1; then
            log_message "  Successfully woke up '$container_name'. It's now running."
          else
            log_message "  Failed to wake up '$container_name'. Manual intervention may be needed."
          fi
        else
          log_message "  Auto-restart is disabled for '$container_name'. It remains asleep."
        fi
        ;;
      "paused")
        log_message "Pet '$container_name' is paused. Consider unpausing it."
        ;;
      *) # Other statuses like 'restarting', 'dead', etc.
        log_message "Pet '$container_name' is in an unusual state: $container_status."
        ;;
    esac
  done

  log_message "All pets checked. Will check again in $CHECK_INTERVAL_SECONDS seconds."
  sleep "$CHECK_INTERVAL_SECONDS"
done
