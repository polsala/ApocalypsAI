#!/bin/bash

# Default thresholds if not set via environment variables
CPU_THRESHOLD=${CPU_THRESHOLD:-80}
RAM_THRESHOLD=${RAM_THRESHOLD:-85}
DISK_THRESHOLD=${DISK_THRESHOLD:-90}
DISK_PARTITION=${DISK_PARTITION:-/}

# Function to display resource usage and alerts
monitor_resources() {
    echo "--- System Resource Monitor ---"

    # Monitor CPU Usage
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
    echo "CPU Usage: ${cpu_usage}%"
    if (( $(echo "${cpu_usage} > ${CPU_THRESHOLD}" | bc -l) )); then
        echo "  ALERT: CPU usage (${cpu_usage}%) exceeds threshold (${CPU_THRESHOLD}%)"
    fi

    # Monitor RAM Usage
    ram_total=$(free -m | awk '/^Mem:/ {print $2}')
    ram_used=$(free -m | awk '/^Mem:/ {print $3}')
    ram_usage=$(awk "BEGIN {printf \"%.2f\", ($ram_used / $ram_total) * 100}")
    echo "RAM Usage: ${ram_usage}% (Total: ${ram_total}MB, Used: ${ram_used}MB)"
    if (( $(echo "${ram_usage} > ${RAM_THRESHOLD}" | bc -l) )); then
        echo "  ALERT: RAM usage (${ram_usage}%) exceeds threshold (${RAM_THRESHOLD}%)"
    fi

    # Monitor Disk Usage
    disk_usage=$(df -h "${DISK_PARTITION}" | awk 'NR==2 {print $5}' | sed 's/%//')
    echo "Disk Usage (${DISK_PARTITION}): ${disk_usage}%"
    if (( disk_usage > DISK_THRESHOLD )); then
        echo "  ALERT: Disk usage (${disk_usage}%) on ${DISK_PARTITION} exceeds threshold (${DISK_THRESHOLD}%)"
    fi

    echo "-------------------------------"
}

# Run the monitoring function
monitor_resources
