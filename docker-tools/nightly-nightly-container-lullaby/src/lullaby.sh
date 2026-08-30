#!/bin/bash

OPERATION=$1
shift # Remove the first argument (operation)

if [ -z "$OPERATION" ]; then
    echo "Usage: lullaby.sh <stop|pause> [container_name_1] [container_name_2]..."
    exit 1
fi

if [ "$#" -eq 0 ]; then
    echo "No containers specified. Exiting."
    exit 0
fi

case "$OPERATION" in
    stop)
        ACTION="stopping"
        ;;
    pause)
        ACTION="pausing"
        ;;
    *)
        echo "Invalid operation: $OPERATION. Must be 'stop' or 'pause'."
        exit 1
        ;;
esac

echo "Initiating container lullaby: $ACTION containers..."

SUCCESS_COUNT=0
FAIL_COUNT=0

for CONTAINER_NAME in "$@"; do
    echo "Attempting to $OPERATION container: $CONTAINER_NAME"
    # Check if the container exists (running or stopped)
    if docker ps -a --format "{{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
        if docker "$OPERATION" "$CONTAINER_NAME"; then
            echo "Successfully ${OPERATION}ped/paused $CONTAINER_NAME."
            SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        else
            echo "Failed to $OPERATION container: $CONTAINER_NAME. Docker command failed."
            FAIL_COUNT=$((FAIL_COUNT + 1))
        fi
    else
        echo "Container '$CONTAINER_NAME' not found or already gone. Skipping."
        FAIL_COUNT=$((FAIL_COUNT + 1)) # Count as a failure to find/operate
    fi
done

echo "Lullaby complete. Successfully $ACTION $SUCCESS_COUNT containers, failed on $FAIL_COUNT."
if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
fi
exit 0
