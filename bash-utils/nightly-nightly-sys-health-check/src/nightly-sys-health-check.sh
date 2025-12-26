#!/bin/bash

# ApocalypsAI - Nightly System Health Check

# --- Configuration ---
# Define a whimsical name for the system
SYSTEM_NAME="The Citadel"

# Define the threshold for "critters" (processes) before it's considered busy
CRITTER_THRESHOLD=200

# Define the threshold for disk usage percentage before it's considered "full"
HOARD_THRESHOLD=85

# Define the threshold for load average before it's considered "burdened"
BURDEN_THRESHOLD=2.0

# Define the target host for ping tests
NETWORK_TARGET="8.8.8.8"

# --- Helper Functions ---

# Function to print a whimsical message
print_message() {
    local level="$1"
    local message="$2"
    case "$level" in
        "INFO")
            echo "[INFO] $message"
            ;;
        "WARN")
            echo "[WARN] $message"
            ;;
        "ERROR")
            echo "[ERROR] $message"
            ;;
        "WHIMSICAL")
            echo "✨ $message ✨"
            ;;
        *)
            echo "$message"
            ;;
    esac
}

# Function to check disk space
check_disk_space() {
    print_message "WHIMSICAL" "Checking the vastness of our digital hoard..."
    local disk_usage=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')

    if [ "$disk_usage" -ge "$HOARD_THRESHOLD" ]; then
        print_message "WARN" "The hoard is getting full! Usage: ${disk_usage}%"
    else
        print_message "INFO" "Hoard levels are acceptable. Usage: ${disk_usage}%"
    fi
}

# Function to check running processes
check_processes() {
    print_message "WHIMSICAL" "Counting the digital critters scurrying about..."
    local critter_count=$(ps aux | wc -l)
    # Subtract 1 for the header line
    critter_count=$((critter_count - 1))

    if [ "$critter_count" -ge "$CRITTER_THRESHOLD" ]; then
        print_message "WARN" "A veritable stampede of critters! Count: ${critter_count}"
    else
        print_message "INFO" "A peaceful gathering of critters. Count: ${critter_count}"
    fi
}

# Function to check network connectivity
check_network() {
    print_message "WHIMSICAL" "Testing the ethereal pathways to the outside world..."
    if ping -c 1 -W 2 "$NETWORK_TARGET" > /dev/null 2>&1; then
        print_message "INFO" "Signal strength is strong! We can reach $NETWORK_TARGET."
    else
        print_message "WARN" "Signal is weak or lost! Cannot reach $NETWORK_TARGET."
    fi
}

# Function to check system load
check_load() {
    print_message "WHIMSICAL" "Assessing the burden on our noble steed..."
    local load_avg=$(uptime | awk -F'load average:' '{ print $2 }' | sed 's/,/ /g' | awk '{print $1}')

    if (( $(echo "$load_avg > $BURDEN_THRESHOLD" | bc -l) )); then
        print_message "WARN" "The steed is feeling the burden! Load average: ${load_avg}"
    else
        print_message "INFO" "The steed carries its load with grace. Load average: ${load_avg}"
    fi
}

# --- Main Execution ---

print_message "WHIMSICAL" "Greetings, traveler! Initiating the nightly health check for $SYSTEM_NAME."

check_disk_space
check_processes
check_network
check_load

print_message "WHIMSICAL" "The nightly ritual is complete. May your systems be ever stable!"

exit 0
