#!/bin/bash

# nightly-sys-health-check.sh
# A whimsical yet useful bash script to perform a quick system health check.

# --- Configuration ---
# Number of top processes to display
TOP_PROCESS_COUNT=5

# --- Functions ---

# Function to display disk usage for the root partition
check_disk_usage() {
    echo "--- Disk Usage (Root Partition) ---"
    df -h / | awk 'NR==2 {print "Total: " $2 " Used: " $3 " Avail: " $4 " Use%: " $5}'
    echo ""
}

# Function to display memory usage
check_memory_usage() {
    echo "--- Memory Usage ---"
    free -h | awk '/^Mem:/ {print "Total: " $2 " Used: " $3 " Free: " $4 " Use%: " $5}'
    echo ""
}

# Function to display top running processes by CPU usage
check_running_processes() {
    echo "--- Top $TOP_PROCESS_COUNT Running Processes (CPU) ---"
    ps aux --sort=-%cpu | awk 'NR<=1 || NR<='$(($TOP_PROCESS_COUNT + 1))' {print $1 "\t" $2 "\t" $3 "\t" $11}'
    echo ""
}

# --- Main Execution ---

echo "===================================="
echo " ApocalypsAI System Health Check "
echo "===================================="
echo "Timestamp: $(date)"
echo ""

check_disk_usage
check_memory_usage
check_running_processes

echo "===================================="
echo " Health check complete. Stay vigilant! "
echo "===================================="
