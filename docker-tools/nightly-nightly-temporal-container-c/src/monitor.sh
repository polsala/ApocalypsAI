#!/bin/bash

# Nightly Temporal Container Chronometer
# Monitors Docker containers for uptime anomalies.

# Default thresholds (can be overridden by environment variables)
RECENT_START_THRESHOLD_MINUTES=${RECENT_START_THRESHOLD_MINUTES:-5} # Containers started within this many minutes are "recent"
LONG_RUNNING_THRESHOLD_DAYS=${LONG_RUNNING_THRESHOLD_DAYS:-30}    # Containers running longer than this many days are "long-running"

echo "--- Temporal Container Chronometer Report ---"
echo "Monitoring for containers recently started (within ${RECENT_START_THRESHOLD_MINUTES} minutes) or excessively long-running (over ${LONG_RUNNING_THRESHOLD_DAYS} days)."
echo "---------------------------------------------"

# Check if docker daemon is accessible
# Mock rationale: In tests, 'docker info' is mocked to simulate success or failure.
if ! docker info > /dev/null 2>&1; then
    echo "ERROR: Docker daemon not accessible. Ensure /var/run/docker.sock is mounted correctly."
    exit 1
fi

# Get all running containers with their names and status
# Format: "NAME\tSTATUS"
# Mock rationale: 'docker ps' output is mocked in tests to provide controlled scenarios.
docker ps --format "{{.Names}}\t{{.Status}}" | while IFS=$'\t' read -r name status; do
    # Extract uptime from status string, e.g., "Up 2 minutes", "Up 3 days"
    # status example: "Up 2 minutes (healthy)" or "Up 3 days"
    uptime_str=$(echo "$status" | sed -E 's/Up ([0-9]+ (seconds?|minutes?|hours?|days?)).*/\1/')

    # Convert uptime string to seconds for comparison
    uptime_seconds=0
    if [[ "$uptime_str" =~ ([0-9]+)\ (second|seconds) ]]; then
        uptime_seconds=$(( ${BASH_REMATCH[1]} ))
    elif [[ "$uptime_str" =~ ([0-9]+)\ (minute|minutes) ]]; then
        uptime_seconds=$(( ${BASH_REMATCH[1]} * 60 ))
    elif [[ "$uptime_str" =~ ([0-9]+)\ (hour|hours) ]]; then
        uptime_seconds=$(( ${BASH_REMATCH[1]} * 3600 ))
    elif [[ "$uptime_str" =~ ([0-9]+)\ (day|days) ]]; then
        uptime_seconds=$(( ${BASH_REMATCH[1]} * 86400 ))
    fi

    recent_start_threshold_seconds=$(( RECENT_START_THRESHOLD_MINUTES * 60 ))
    long_running_threshold_seconds=$(( LONG_RUNNING_THRESHOLD_DAYS * 86400 ))

    if [ "$uptime_seconds" -lt "$recent_start_threshold_seconds" ]; then
        echo "ANOMALY: Container '$name' has recently started. Uptime: $uptime_str"
    elif [ "$uptime_seconds" -gt "$long_running_threshold_seconds" ]; then
        echo "ANOMALY: Container '$name' is excessively long-running. Uptime: $uptime_str"
    else
        echo "NORMAL: Container '$name' is stable. Uptime: $uptime_str"
    fi
done

echo "---------------------------------------------"
echo "Temporal Chronometer Scan Complete."
