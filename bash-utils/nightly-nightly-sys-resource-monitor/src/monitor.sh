#!/bin/bash

# --- Configuration ---

# Set CPU usage threshold (percentage)
CPU_THRESHOLD=80

# Set RAM usage threshold (percentage)
RAM_THRESHOLD=85

# Set Disk usage threshold (percentage for root partition '/'). Add more partitions as needed.
DISK_THRESHOLD=90

# Disk partitions to monitor (space-separated)
MONITORED_DISKS="/"

# --- Functions ---

# Function to get CPU usage percentage
get_cpu_usage() {
    # Mock rationale: Using a fixed value for deterministic testing.
    # In a real scenario, this would use 'top' or 'mpstat'.
    echo "50"
}

# Function to get RAM usage percentage
get_ram_usage() {
    # Mock rationale: Using a fixed value for deterministic testing.
    # In a real scenario, this would use 'free' or 'top'.
    echo "60"
}

# Function to get Disk usage percentage for a given mount point
get_disk_usage() {
    local mount_point="$1"
    # Mock rationale: Using a fixed value for deterministic testing.
    # In a real scenario, this would use 'df'.
    echo "70"
}

# Function to check if a value exceeds a threshold
check_threshold() {
    local value=$1
    local threshold=$2
    local resource_name=$3
    local mount_point_info=$4

    if (( value > threshold )); then
        echo "ALERT: High $resource_name detected! Current: ${value}%, Threshold: ${threshold}%${mount_point_info}"
    fi
}

# --- Main Logic ---

echo "--- System Resource Monitor Started ---"

# Monitor CPU
current_cpu=$(get_cpu_usage)
check_threshold "$current_cpu" "$CPU_THRESHOLD" "CPU Usage"

# Monitor RAM
current_ram=$(get_ram_usage)
check_threshold "$current_ram" "$RAM_THRESHOLD" "RAM Usage"

# Monitor Disk
for disk in $MONITORED_DISKS;
do
    current_disk=$(get_disk_usage "$disk")
    check_threshold "$current_disk" "$DISK_THRESHOLD" "Disk Usage" " on ${disk}"
done

echo "--- System Resource Monitor Finished ---"
