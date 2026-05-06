#!/bin/bash

# ApocalypsAI - Nightly System Health Reporter
# Classifier: bash-utils

# --- Configuration ---
MAX_PROCESSES=5 # Number of top processes to report

# --- Thematic Messages ---
TITLE="Apocalypse Survival Report"

CPU_WARN="The processors are groaning under the strain, like the last survivors of a digital plague."
CPU_OK="The core processors are humming, a faint echo of pre-collapse efficiency."

MEM_WARN="Memory reserves are dwindling, like water in the wasteland."
MEM_OK="Memory banks are stable, holding onto precious data like a survivor guards their rations."

DISK_WARN="Storage is becoming scarce, the digital archives are filling up!"
DISK_OK="Disk space is ample, for now. The data vaults are secure."

NET_WARN="Unusual network activity detected. Rogue signals or just the ghosts of the old world?"
NET_OK="Network channels are clear. No immediate digital threats detected."

PROCESS_WARN="These processes are hogging resources like warlords hoarding fuel."
PROCESS_OK="Essential processes are running smoothly, keeping the lights on."

# --- Helper Functions ---

print_header() {
    echo "=================================================="
    echo " $TITLE "
    echo " $(date '+%Y-%m-%d %H:%M:%S') "
    echo "=================================================="
    echo ""
}

print_section_header() {
    echo "### $1 ###"
    echo ""
}

print_metric() {
    echo "  - $1: $2"
}

print_warning() {
    echo "  * WARNING: $1"
}

print_ok() {
    echo "  * STATUS: $1"
}

# --- Main Logic ---

print_header

# CPU Usage
print_section_header "CPU Core Status"
CPU_LOAD=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')

if (( $(echo "${CPU_LOAD} > 80" | bc -l) )); then
    print_warning "$CPU_WARN"
else
    print_ok "$CPU_OK"
fi
print_metric "Current CPU Load" "${CPU_LOAD}%"

# Memory Usage
print_section_header "Memory Reserves"
MEM_INFO=$(free -h | grep Mem:)
SWAP_INFO=$(free -h | grep Swap:)

MEM_USED=$(echo $MEM_INFO | awk '{print $3}')
MEM_TOTAL=$(echo $MEM_INFO | awk '{print $2}')
MEM_PERCENT=$(echo "100 * $(free | awk '/^Mem:/ {print $3}') / $(free | awk '/^Mem:/ {print $2}')" | bc)

if (( $(echo "${MEM_PERCENT} > 85" | bc -l) )); then
    print_warning "$MEM_WARN"
else
    print_ok "$MEM_OK"
fi
print_metric "RAM Usage" "${MEM_USED}/${MEM_TOTAL} (${MEM_PERCENT}%)"
print_metric "Swap Usage" "$(echo $SWAP_INFO | awk '{print $3"/"$2}')"

# Disk Space
print_section_header "Resource Vaults (Disk Space)"
DISK_USAGE=$(df -h --exclude-type=tmpfs --exclude-type=devtmpfs)

if echo "$DISK_USAGE" | grep -q " 10%$"; then # Simple check for low space on any mount
    print_warning "$DISK_WARN"
else
    print_ok "$DISK_OK"
fi

echo "$DISK_USAGE"
echo ""

# Running Processes
print_section_header "Resource Hogs (Top Processes)"

if ps aux --sort=-%cpu | head -n $((MAX_PROCESSES + 1)) | tail -n $MAX_PROCESSES | grep -q ""; then
    print_metric "Top $MAX_PROCESSES Processes by CPU" ""
    ps aux --sort=-%cpu | head -n $((MAX_PROCESSES + 1)) | tail -n $MAX_PROCESSES
    echo ""
    print_ok "$PROCESS_OK"
else
    print_warning "$PROCESS_WARN"
fi

# Network Connections
print_section_header "Network Channels"
NET_CONNECTIONS=$(ss -tulnp)

if echo "$NET_CONNECTIONS" | grep -q ":80 " || echo "$NET_CONNECTIONS" | grep -q ":443 "; then # Basic check for common web ports
    print_ok "$NET_OK"
else
    print_warning "$NET_WARN"
fi

print_metric "Active Network Connections" ""
echo "$NET_CONNECTIONS"

echo ""
echo "--- End of Report --- "
