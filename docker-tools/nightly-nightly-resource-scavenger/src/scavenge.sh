#!/bin/bash
set -euo pipefail

# Nightly Resource Scavenger Script
# This script identifies resource-hungry running containers and stale (long-stopped) containers.

# Default thresholds
CPU_THRESHOLD=80         # CPU usage percentage
MEM_THRESHOLD_PERCENT=80 # Memory usage percentage
STALE_DAYS=7             # Days a stopped container is considered stale

# Parse arguments for custom thresholds
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --cpu-threshold) CPU_THRESHOLD="$2"; shift ;; # Custom CPU threshold
        --mem-threshold) MEM_THRESHOLD_PERCENT="$2"; shift ;; # Custom Memory threshold
        --stale-days) STALE_DAYS="$2"; shift ;; # Custom stale days threshold
        *) echo "Error: Unknown parameter '$1'"; exit 1 ;; # Handle unknown arguments
    esac
    shift # Move to the next argument
done

echo "--- Nightly Resource Scavenger Report ---"
echo "Thresholds: CPU > ${CPU_THRESHOLD}%, Memory > ${MEM_THRESHOLD_PERCENT}%, Stale > ${STALE_DAYS} days"
echo "Report generated on: $(date -u)"
echo ""

# Get current Unix timestamp for stale calculation
CURRENT_UNIX_TIME=$(date +%s)
STALE_SECONDS=$((STALE_DAYS * 24 * 60 * 60))

# --- Identify Stale Containers (Stopped for > STALE_DAYS days) ---
echo "### Stale Containers (Stopped for > ${STALE_DAYS} days) ###"
STALE_CONTAINERS_FOUND=0

# List all containers, including stopped ones, and parse their ID, Name, Status, and Creation Timestamp.
# The 'CreatedAt' format is like '2023-10-20 10:00:00 +0000 UTC'.
# We need to clean it to '2023-10-20 10:00:00 UTC' for BusyBox date to parse correctly.
# Mock rationale: 'docker ps -a' is mocked in tests to provide deterministic container data.
docker ps -a --format "{{.ID}}\t{{.Names}}\t{{.Status}}\t{{.CreatedAt}}" | while IFS=$'\t' read -r ID NAME STATUS CREATED_AT; do
    # Check if the container is in an 'Exited' state
    if [[ "$STATUS" == *"Exited"* ]]; then
        # Clean the CREATED_AT string for date -d parsing
        CLEAN_CREATED_AT=$(echo "$CREATED_AT" | sed 's/ +0000 UTC/ UTC/')
        
        # Convert creation date to Unix timestamp
        # Mock rationale: 'date -d' is mocked in tests to provide deterministic timestamps.
        CREATED_UNIX_TIME=$(date -d "$CLEAN_CREATED_AT" +%s)
        
        # Calculate the age of the container in seconds
        AGE_SECONDS=$((CURRENT_UNIX_TIME - CREATED_UNIX_TIME))

        # If the container's age exceeds the stale threshold, report it
        if (( AGE_SECONDS > STALE_SECONDS )); then
            echo "  - ID: $ID, Name: $NAME, Status: $STATUS, Created: $CREATED_AT (Age: $((AGE_SECONDS / (24*60*60))) days)"
            STALE_CONTAINERS_FOUND=$((STALE_CONTAINERS_FOUND + 1))
        fi
    fi
done

if [[ "$STALE_CONTAINERS_FOUND" -eq 0 ]]; then
    echo "  No stale containers found."
fi
echo ""

# --- Identify Resource-Hungry Running Containers (CPU > CPU_THRESHOLD% or Memory > MEM_THRESHOLD_PERCENT%) ---
echo "### Resource-Hungry Running Containers (CPU > ${CPU_THRESHOLD}% or Memory > ${MEM_THRESHOLD_PERCENT}%) ###"
RESOURCE_HUNGRY_FOUND=0

# Get real-time resource stats for all currently running containers.
# Mock rationale: 'docker stats' is mocked in tests to provide deterministic resource usage data.
docker stats --no-stream --format "{{.ID}}\t{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}" | while IFS=$'\t' read -r ID NAME CPU_PERC MEM_USAGE MEM_PERC; do
    # Extract numerical values from percentages (e.g., "95.00%" -> "95.00")
    CPU_VALUE=$(echo "$CPU_PERC" | sed 's/%//')
    MEM_VALUE=$(echo "$MEM_PERC" | sed 's/%//')

    # Bash arithmetic operations work with integers. We'll compare integer parts.
    CPU_INT=$(echo "$CPU_VALUE" | cut -d'.' -f1) # Get integer part of CPU percentage
    MEM_INT=$(echo "$MEM_VALUE" | cut -d'.' -f1) # Get integer part of Memory percentage

    # Check if CPU or Memory usage exceeds their respective thresholds
    if (( CPU_INT >= CPU_THRESHOLD )) || (( MEM_INT >= MEM_THRESHOLD_PERCENT )); then
        echo "  - ID: $ID, Name: $NAME, CPU: $CPU_PERC, Memory: $MEM_USAGE ($MEM_PERC)"
        RESOURCE_HUNGRY_FOUND=$((RESOURCE_HUNGRY_FOUND + 1))
    fi
done

if [[ "$RESOURCE_HUNGRY_FOUND" -eq 0 ]]; then
    echo "  No resource-hungry containers found."
fi
echo ""

echo "--- Report End ---"
