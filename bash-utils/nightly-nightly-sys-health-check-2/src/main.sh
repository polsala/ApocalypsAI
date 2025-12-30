#!/bin/bash

# ApocalypsAI - Nightly System Health Check

# --- Configuration ---
DISK_WARNING_PERCENT=85
MEMORY_WARNING_PERCENT=90

# --- Helper Functions ---

# Function to print a whimsical message based on status
print_status() {
    local message="$1"
    local level="$2"

    case "$level" in
        "OK")
            echo "\e[32m[OK]\e[0m $message"
            ;;
        "WARNING")
            echo "\e[33m[WARNING]\e[0m $message"
            ;;
        "CRITICAL")
            echo "\e[31m[CRITICAL]\e[0m $message"
            ;;
        *)
            echo "$message"
            ;;
    esac
}

# --- Main Logic ---

echo "\n--- ApocalypsAI System Health Check ---"

# 1. Disk Space Check

# Mock rationale: Using df command to simulate disk space check.
# In a real scenario, this would query the actual disk usage.
if command -v df &> /dev/null; then
    DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    if [[ "$DISK_USAGE" -ge "$DISK_WARNING_PERCENT" ]]; then
        print_status "Disk space is critically low! The wasteland is expanding! ($DISK_USAGE% used)" "CRITICAL"
    else
        print_status "Disk space is nominal. Plenty of room for bunkers. ($DISK_USAGE% used)" "OK"
    fi
else
    print_status "Could not check disk space. Assuming the worst."
fi

# 2. Memory Usage Check

# Mock rationale: Using free command to simulate memory usage check.
# In a real scenario, this would query the actual memory usage.
if command -v free &> /dev/null;
then
    # Get total and used memory in KB, then calculate percentage
    TOTAL_MEM=$(free | awk '/^Mem:/ {print $2}')
    USED_MEM=$(free | awk '/^Mem:/ {print $3}')
    MEMORY_USAGE=$(awk "BEGIN {printf \"%.0f\", ($USED_MEM / $TOTAL_MEM) * 100}")

    if [[ "$MEMORY_USAGE" -ge "$MEMORY_WARNING_PERCENT" ]]; then
        print_status "Memory is almost full! The system is struggling to breathe. ($MEMORY_USAGE% used)" "CRITICAL"
    elif [[ "$MEMORY_USAGE" -gt "$((MEMORY_WARNING_PERCENT - 10))" ]]; then
        print_status "Memory usage is high. Keep an eye on it. ($MEMORY_USAGE% used)" "WARNING"
    else
        print_status "Memory usage is within acceptable limits. The servers are humming. ($MEMORY_USAGE% used)" "OK"
    fi
else
    print_status "Could not check memory usage. Hope for the best."
fi

# 3. Running Processes Check

# Mock rationale: Using ps command to simulate process count.
# In a real scenario, this would query the actual number of processes.
if command -v ps &> /dev/null;
then
    PROCESS_COUNT=$(ps aux | wc -l)
    # Subtract 1 for the header line
    PROCESS_COUNT=$((PROCESS_COUNT - 1))

    if [[ "$PROCESS_COUNT" -gt "1000" ]]; then # Arbitrary threshold for 'too many'
        print_status "An alarming number of processes are running ($PROCESS_COUNT). Is something lurking?" "WARNING"
    else
        print_status "Process count is stable ($PROCESS_COUNT). The digital ghosts are quiet."
    fi
else
    print_status "Could not count processes. The silence is deafening."
fi

echo "\n--- End of Report ---"
