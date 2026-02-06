#!/bin/bash

# Default configuration
INTERVAL=${INTERVAL:-2}
PROC_ROOT=${PROC_ROOT:-/proc}
CPU_LOW_THRESHOLD=${CPU_LOW_THRESHOLD:-30}
CPU_HIGH_THRESHOLD=${CPU_HIGH_THRESHOLD:-70}
MEM_LOW_THRESHOLD=${MEM_LOW_THRESHOLD:-30}
MEM_HIGH_THRESHOLD=${MEM_HIGH_THRESHOLD:-70}

# ANSI color codes
RESET="\033[0m"
BG_GREEN="\033[42m" # Green background
FG_BLACK="\033[30m" # Black foreground
BG_YELLOW="\033[43m" # Yellow background
FG_BLACK="\033[30m" # Black foreground
BG_RED="\033[41m"   # Red background
FG_WHITE="\033[37m" # White foreground
BG_BLUE="\033[44m"  # Blue background
FG_WHITE="\033[37m" # White foreground

# Global variables for CPU calculation
PREV_TOTAL=0
PREV_IDLE=0

# Function to get CPU usage
get_cpu_usage() {
    # Read /proc/stat for CPU times
    # user nice system idle iowait irq softirq steal guest guest_nice
    # cpu 257724 0 100000 1000000 0 0 0 0 0 0
    read -r _ user nice system idle iowait irq softirq steal guest guest_nice < "$PROC_ROOT/stat"

    # Calculate total CPU time (excluding guest and guest_nice)
    local current_total=$((user + nice + system + idle + iowait + irq + softirq + steal))
    local current_idle=$((idle + iowait)) # idle + iowait is usually considered idle time

    # Persist previous values for calculation
    if (( PREV_TOTAL == 0 && PREV_IDLE == 0 )); then
        PREV_TOTAL=$current_total
        PREV_IDLE=$current_idle
        echo "0" # Return 0 for first call, as we need a previous reading
        return
    fi

    local diff_total=$((current_total - PREV_TOTAL))
    local diff_idle=$((current_idle - PREV_IDLE))

    local cpu_usage=0
    if (( diff_total > 0 )); then
        cpu_usage=$(( (diff_total - diff_idle) * 100 / diff_total ))
    fi

    PREV_TOTAL=$current_total
    PREV_IDLE=$current_idle

    echo "$cpu_usage"
}

# Function to get Memory usage
get_mem_usage() {
    # Read /proc/meminfo
    # MemTotal:        8000000 kB
    # MemFree:         2000000 kB
    # MemAvailable:    6000000 kB (more accurate for available memory)
    local mem_total_kb=$(grep MemTotal "$PROC_ROOT/meminfo" | awk '{print $2}')
    local mem_available_kb=$(grep MemAvailable "$PROC_ROOT/meminfo" | awk '{print $2}')

    local mem_used_kb=$((mem_total_kb - mem_available_kb))

    local mem_usage=0
    if (( mem_total_kb > 0 )); then
        mem_usage=$(( mem_used_kb * 100 / mem_total_kb ))
    fi
    echo "$mem_usage"
}

# Main loop
while true; do
    CPU_USAGE=$(get_cpu_usage)
    MEM_USAGE=$(get_mem_usage)

    # Skip first iteration for CPU as it needs previous values
    # The first CPU_USAGE will be 0, so we only proceed if it's not the very first run
    if (( PREV_TOTAL == 0 && PREV_IDLE == 0 )); then
        sleep "$INTERVAL"
        continue
    fi

    COLOR_BG=""
    COLOR_FG=""
    MOOD_MESSAGE=""

    # Determine mood based on CPU and Memory
    if (( CPU_USAGE >= CPU_HIGH_THRESHOLD || MEM_USAGE >= MEM_HIGH_THRESHOLD )); then
        COLOR_BG="$BG_RED"
        COLOR_FG="$FG_WHITE"
        MOOD_MESSAGE="Stressed"
    elif (( CPU_USAGE >= CPU_LOW_THRESHOLD || MEM_USAGE >= MEM_LOW_THRESHOLD )); then
        COLOR_BG="$BG_YELLOW"
        COLOR_FG="$FG_BLACK"
        MOOD_MESSAGE="Moderate"
    else
        COLOR_BG="$BG_BLUE" # Using blue for calm, as green might be too common
        COLOR_FG="$FG_WHITE"
        MOOD_MESSAGE="Calm"
    fi

    # Print the mood ring output
    echo -e "${COLOR_BG}${COLOR_FG} System Mood: ${MOOD_MESSAGE} (CPU: ${CPU_USAGE}%, Mem: ${MEM_USAGE}%) ${RESET}"

    sleep "$INTERVAL"
done
