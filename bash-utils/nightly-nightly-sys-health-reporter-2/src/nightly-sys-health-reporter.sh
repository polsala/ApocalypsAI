#!/bin/bash

# This script gathers system health metrics and presents them in a whimsical, apocalypse-ready format.

# --- Configuration ---
# Thresholds for 'survival readiness' score. Lower is better.
CPU_THRESHOLD=80
MEM_THRESHOLD=80
DISK_THRESHOLD=90

# --- Helper Functions ---

# Function to print a themed message
print_message() {
    local level="$1"
    local message="$2"
    case "$level" in
        "INFO")
            echo "\033[0;32m[INFO]\033[0m $message"
            ;;
        "WARN")
            echo "\033[0;33m[WARN]\033[0m $message"
            ;;
        "ERROR")
            echo "\033[0;31m[ERROR]\033[0m $message"
            ;;
        "SURVIVAL")
            echo "\033[1;36m[SURVIVAL]\033[0m $message"
            ;;
        *) echo "$message" ;;
    esac
}

# Function to get CPU usage percentage
get_cpu_usage() {
    # Using mpstat for a more robust CPU usage calculation
    # Mock rationale: mpstat is a standard utility, but for testing, we'll mock its output.
    if [ -z "$(command -v mpstat)" ]; then
        echo "Error: mpstat command not found. Cannot get CPU usage."
        return 1
    fi
    # Extracting idle percentage and calculating usage
    local idle_percent=$(mpstat 1 1 | awk '/Average:/ {print $NF}')
    if [ -z "$idle_percent" ]; then
        echo "Error: Could not parse mpstat output."
        return 1
    fi
    local cpu_usage=$(awk "BEGIN {printf \"%.0f\", 100 - $idle_percent}")
    echo "$cpu_usage"
}

# Function to get Memory usage percentage
get_mem_usage() {
    # Using free command to get memory usage
    # Mock rationale: free is a standard utility, but for testing, we'll mock its output.
    local mem_info=$(free -m | awk '/Mem:/ {print $3 " " $2}')
    if [ -z "$mem_info" ]; then
        echo "Error: Could not parse free output."
        return 1
    fi
    local used_mem=$(echo "$mem_info" | awk '{print $1}')
    local total_mem=$(echo "$mem_info" | awk '{print $2}')
    local mem_usage=$(awk "BEGIN {printf \"%.0f\", ($used_mem / $total_mem) * 100}")
    echo "$mem_usage"
}

# Function to get Disk usage percentage for root partition
get_disk_usage() {
    # Using df command to get disk usage for the root partition
    # Mock rationale: df is a standard utility, but for testing, we'll mock its output.
    local disk_info=$(df -h / | awk 'NR==2 {print $5 " " $2}')
    if [ -z "$disk_info" ]; then
        echo "Error: Could not parse df output."
        return 1
    fi
    local disk_usage=$(echo "$disk_info" | awk '{print $1}' | sed 's/%//')
    echo "$disk_usage"
}

# Function to check network interface status
get_network_status() {
    # Checking for active network interfaces (excluding loopback)
    # Mock rationale: ip is a standard utility, but for testing, we'll mock its output.
    local active_interfaces=$(ip -o link show | awk -F': ' '!/lo/ && $2 ~ /UP/ {print $2}')
    if [ -z "$active_interfaces" ]; then
        echo "No active network interfaces detected (excluding loopback)."
        return 1
    else
        echo "Active interfaces: $active_interfaces"
    fi
}

# Function to calculate survival readiness score
calculate_readiness_score() {
    local cpu=$1
    local mem=$2
    local disk=$3
    local score=0

    if [ "$cpu" -gt "$CPU_THRESHOLD" ]; then
        score=$((score + 1))
    fi
    if [ "$mem" -gt "$MEM_THRESHOLD" ]; then
        score=$((score + 1))
    fi
    if [ "$disk" -gt "$DISK_THRESHOLD" ]; then
        score=$((score + 1))
    fi
    echo "$score"
}

# --- Main Execution ---

print_message "SURVIVAL" "Initiating System Health Scan... The wasteland awaits!"

# Get CPU Usage
CPU_USAGE=$(get_cpu_usage)
if [ $? -ne 0 ]; then
    print_message "ERROR" "Failed to retrieve CPU usage."
    CPU_USAGE="N/A"
else
    print_message "INFO" "CPU Load: ${CPU_USAGE}%"
fi

# Get Memory Usage
MEM_USAGE=$(get_mem_usage)
if [ $? -ne 0 ]; then
    print_message "ERROR" "Failed to retrieve Memory usage."
    MEM_USAGE="N/A"
else
    print_message "INFO" "Memory Usage: ${MEM_USAGE}%"
fi

# Get Disk Usage
DISK_USAGE=$(get_disk_usage)
if [ $? -ne 0 ]; then
    print_message "ERROR" "Failed to retrieve Disk usage."
    DISK_USAGE="N/A"
else
    print_message "INFO" "Root Disk Usage: ${DISK_USAGE}%"
fi

# Get Network Status
NETWORK_STATUS=$(get_network_status)
if [ $? -ne 0 ]; then
    print_message "WARN" "Network Status: ${NETWORK_STATUS}"
else
    print_message "INFO" "Network Status: ${NETWORK_STATUS}"
fi

# Calculate Survival Readiness Score
if [[ "$CPU_USAGE" != "N/A" && "$MEM_USAGE" != "N/A" && "$DISK_USAGE" != "N/A" ]]; then
    READINESS_SCORE=$(calculate_readiness_score "$CPU_USAGE" "$MEM_USAGE" "$DISK_USAGE")
    case "$READINESS_SCORE" in
        0)
            print_message "SURVIVAL" "System is in peak condition! Ready for anything."
            ;;
        1)
            print_message "WARN" "System shows minor signs of strain. Keep an eye on it."
            ;;
        2)
            print_message "ERROR" "System is showing significant strain. Immediate attention required!"
            ;;
        3)
            print_message "ERROR" "System is on the brink! Evacuate immediately!"
            ;;
    esac
else
    print_message "ERROR" "Could not calculate survival readiness due to missing metrics."
fi

print_message "SURVIVAL" "System scan complete. Stay vigilant."

exit 0
