#!/bin/bash

# nightly-sys-health-check
# A whimsical bash script for system health checks.

# --- Configuration ---
# Thresholds for disk space and memory usage (in percentage)
DISK_WARNING_THRESHOLD=85
MEMORY_WARNING_THRESHOLD=80

# --- Helper Functions ---

# Function to print a status message with a whimsical prefix
print_status() {
    local status_type="$1"
    local message="$2"
    local color="\033[0m"

    case "$status_type" in
        "OK")
            color="\033[0;32m" # Green
            prefix="[SURVIVAL CONFIRMED] "
            ;; 
        "WARNING")
            color="\033[0;33m" # Yellow
            prefix="[CAUTION ADVISED] "
            ;; 
        "CRITICAL")
            color="\033[0;31m" # Red
            prefix="[IMMINENT DOOM] "
            ;; 
        *) 
            prefix="[INFO] "
            ;; 
    esac
    echo -e "${color}${prefix}${message}\033[0m"
}

# --- Main Logic ---

echo "--- ApocalypsAI System Health Check ---"

# 1. Check Disk Space

# Get disk usage percentage for the root partition
# Mock rationale: In a real scenario, this would use `df -hP /` and parse output. 
# For testing, we'll simulate values.
if [ -z "$MOCK_DISK_USAGE" ]; then
    DISK_USAGE=$(df -hP / | awk 'NR==2 {print $5}' | sed 's/%//')
else
    DISK_USAGE="$MOCK_DISK_USAGE"
fi

if [ "$DISK_USAGE" -ge "$DISK_WARNING_THRESHOLD" ]; then
    print_status "CRITICAL" "Disk space is critically low! Prepare for resource rationing! ($DISK_USAGE% used)"
elif [ "$DISK_USAGE" -ge "$MEMORY_WARNING_THRESHOLD" ]; then
    print_status "WARNING" "Disk space is getting tight. Consider clearing out old bunkers. ($DISK_USAGE% used)"
else
    print_status "OK" "Disk space is sufficient for the last stand! ($DISK_USAGE% used)"
fi

# 2. Check Memory Usage

# Get memory usage percentage
# Mock rationale: In a real scenario, this would use `free -m` and parse output.
# For testing, we'll simulate values.
if [ -z "$MOCK_MEMORY_USAGE" ]; then
    MEM_TOTAL=$(free | awk '/^Mem:/ {print $2}')
    MEM_USED=$(free | awk '/^Mem:/ {print $3}')
    MEMORY_USAGE=$(awk "BEGIN {printf \"%d\", ($MEM_USED / $MEM_TOTAL) * 100}")
else
    MEMORY_USAGE="$MOCK_MEMORY_USAGE"
fi

if [ "$MEMORY_USAGE" -ge "$MEMORY_WARNING_THRESHOLD" ]; then
    print_status "CRITICAL" "Memory usage is critical! Your system is struggling to keep up with the apocalypse! ($MEMORY_USAGE% used)"
elif [ "$MEMORY_USAGE" -ge "$DISK_WARNING_THRESHOLD" ]; then # Re-using DISK_WARNING_THRESHOLD for a second warning level
    print_status "WARNING" "Memory usage is high. Consider shutting down non-essential operations. ($MEMORY_USAGE% used)"
else
    print_status "OK" "Memory usage is nominal. Plenty of RAM for your escape pod! ($MEMORY_USAGE% used)"
fi

# 3. Check Running Processes (simple count for now)

# Mock rationale: In a real scenario, this might check for specific critical processes or anomalies.
# For testing, we'll simulate a count.
if [ -z "$MOCK_PROCESS_COUNT" ]; then
    PROCESS_COUNT=$(ps aux | wc -l)
    # Subtract 1 for the header line
    PROCESS_COUNT=$((PROCESS_COUNT - 1))
else
    PROCESS_COUNT="$MOCK_PROCESS_COUNT"
fi

# Arbitrary threshold for 'too many' processes
PROCESS_ALERT_THRESHOLD=200

if [ "$PROCESS_COUNT" -gt "$PROCESS_ALERT_THRESHOLD" ]; then
    print_status "WARNING" "High number of running processes detected ($PROCESS_COUNT). Potential resource drain or unexpected activity."
else
    print_status "OK" "Process count is within expected limits ($PROCESS_COUNT). All systems nominal."
fi

echo "--- Health Check Complete ---"
