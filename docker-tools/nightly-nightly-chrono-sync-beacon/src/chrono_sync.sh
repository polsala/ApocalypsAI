#!/bin/bash
set -euo pipefail

# Check if any container names were provided
if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <container_name_1> [container_name_2 ...]"
    echo "Synchronizes the system clocks of specified containers with the host's current UTC time."
    exit 1
fi

echo "Starting Chrono-Sync Beacon..."

# Get the current UTC time from the utility container.
# This container's time should be synchronized with the host's time.
CURRENT_UTC_TIME=$(date -u +"%Y-%m-%d %H:%M:%S")
echo "Host's current UTC time: $CURRENT_UTC_TIME"

# Iterate through all provided container names/IDs
for container_name in "$@"; do
    echo "Attempting to synchronize clock for container: $container_name"
    
    # Check if the container exists and is running
    if docker inspect "$container_name" &>/dev/null; then
        # Execute the date -s command inside the target container to set its time.
        # Using 'sh -c' for robustness across different container shells (e.g., bash, ash).
        if docker exec "$container_name" sh -c "date -u -s '$CURRENT_UTC_TIME'"; then
            echo "Successfully synchronized '$container_name' to $CURRENT_UTC_TIME"
        else
            echo "Failed to synchronize '$container_name'. Ensure 'date' command is available and permissions are correct within the target container."
        fi
    else
        echo "Error: Container '$container_name' not found or not running. Skipping."
    fi
done

echo "Chrono-Sync Beacon operation complete."
