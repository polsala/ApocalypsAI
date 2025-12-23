#!/bin/bash

# ApocalypsAI - nightly-sys-health-report

# --- Configuration ---
# Threshold for disk usage warning (percentage)
DISK_WARNING_THRESHOLD=80
# Number of top processes to display
TOP_PROCESS_COUNT=3
# Network host to ping for connectivity check
NETWORK_CHECK_HOST="8.8.8.8"

# --- Helper Functions ---

# Function to print a colored message
print_message() {
    local color="$1"
    local message="$2"
    case "$color" in
        "red") echo -e "\033[0;31m${message}\033[0m";;
        "green") echo -e "\033[0;32m${message}\033[0m";;
        "yellow") echo -e "\033[0;33m${message}\033[0m";;
        "blue") echo -e "\033[0;34m${message}\033[0m";;
        "cyan") echo -e "\033[0;36m${message}\033[0m";;
        "white") echo -e "\033[0;37m${message}\033[0m";;
        "bold") echo -e "\033[1m${message}\033[0m";;
        "reset") echo -e "\033[0m${message}";;
        *)
            echo "$message"
            ;;
    esac
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# --- Main Script ---

# Check for essential commands
if ! command_exists "uptime" || ! command_exists "df" || ! command_exists "free" || ! command_exists "ps" || ! command_exists "ping"; then
    print_message "red" "Error: Required system commands (uptime, df, free, ps, ping) not found. Please install them."
    exit 1
fi

# --- Report Header ---
print_message "cyan" "----------------------------------------"
print_message "cyan" "✨ ApocalypsAI System Health Report ✨"
print_message "cyan" "----------------------------------------"

# --- System Uptime ---
UPTIME=$(uptime -p | sed 's/up //')
print_message "green" "🚀 **System Uptime:** ${UPTIME}"

# --- Disk Space Status ---
print_message "yellow" "\n💾 **Disk Space Status:**"
DF_OUTPUT=$(df -h --output=source,pcent,target | tail -n +2)

while IFS= read -r line; do
    PARTITION=$(echo "$line" | awk '{print $1}')
    PERCENTAGE=$(echo "$line" | awk '{print $2}')
    MOUNTPOINT=$(echo "$line" | awk '{print $3}')

    # Remove '%' from percentage
    PERCENTAGE_NUM=${PERCENTAGE%?}

    if [ "$PERCENTAGE_NUM" -ge "$DISK_WARNING_THRESHOLD" ]; then
        STATUS="Uh oh, better start rationing those bits!"
        COLOR="red"
    else
        STATUS="Plenty of room for your digital survival guides."
        COLOR="green"
    fi
    print_message "white" "  - ${PARTITION} (${MOUNTPOINT}): ${PERCENTAGE} full. ${STATUS}"
done <<< "$DF_OUTPUT"

# --- Memory Usage ---
print_message "yellow" "\n🧠 **Memory Usage:**"
MEM_OUTPUT=$(free -h | tail -n +2)

TOTAL_MEM=$(echo "$MEM_OUTPUT" | awk '{print $2}')
USED_MEM=$(echo "$MEM_OUTPUT" | awk '{print $3}')
FREE_MEM=$(echo "$MEM_OUTPUT" | awk '{print $4}')

# Calculate percentage used (approximate for display)
# This is a bit tricky with free -h, so we'll use a simplified approach or rely on ps for a more accurate process-based view.
# For simplicity, we'll just display the values and add a whimsical comment.

print_message "white" "  - Total: ${TOTAL_MEM}"
print_message "white" "  - Used: ${USED_MEM} (The AI core is humming, but not overheating... yet.)"
print_message "white" "  - Free: ${FREE_MEM} (Still some breathing room for new apocalyptic strategies.)"

# --- Top Processes ---
print_message "yellow" "\n🔥 **Top Processes (by CPU %):**"
# Using ps aux --sort=-%cpu and head to get top processes
# We'll filter out the header line and then take the top N
PS_OUTPUT=$(ps aux --sort=-%cpu | tail -n +2 | head -n "$TOP_PROCESS_COUNT")

while IFS= read -r line;
    do
        PID=$(echo "$line" | awk '{print $2}')
        CPU_PERCENT=$(echo "$line" | awk '{print $3}')
        COMMAND=$(echo "$line" | awk '{$1=$2=$3=$4=""; print substr($0, index($0,$4))}' | sed 's/^[ 	]*//')
        print_message "white" "  - [${PID}] ${COMMAND} (${CPU_PERCENT}%): Simulating the end of days, as usual."
    done <<< "$PS_OUTPUT"

# --- Network Connectivity ---
print_message "yellow" "\n🌐 **Network Connectivity:**"

if ping -c 1 "$NETWORK_CHECK_HOST" > /dev/null 2>&1;
    then
        print_message "green" "  - Ping to ${NETWORK_CHECK_HOST}: Success! The digital highways are still open."
    else
        print_message "red" "  - Ping to ${NETWORK_CHECK_HOST}: Failed! The digital highways are down."
fi

# Add a check for a common domain name
if ping -c 1 "google.com" > /dev/null 2>&1;
    then
        print_message "green" "  - Ping to google.com: Success! We can still reach the old world."
    else
        print_message "red" "  - Ping to google.com: Failed! The old world is unreachable."
fi

# --- Overall Status ---
print_message "cyan" "\n🌟 **Overall System Status:** Mostly Stable. Keep an eye on that disk space!"
print_message "cyan" "----------------------------------------"

exit 0
