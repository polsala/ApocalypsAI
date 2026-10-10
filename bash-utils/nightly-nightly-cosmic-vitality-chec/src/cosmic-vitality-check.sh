#!/bin/bash

# Default thresholds (can be overridden by environment variables for testing)
CPU_THRESHOLD_HIGH=${CPU_THRESHOLD_HIGH:-80} # %
MEM_THRESHOLD_HIGH=${MEM_THRESHOLD_HIGH:-85} # %
DISK_THRESHOLD_HIGH=${DISK_THRESHOLD_HIGH:-90} # %

# Function to get CPU usage (idle percentage, then calculate busy)
get_cpu_usage() {
    # Mock rationale: In a real scenario, this would execute `top` or `mpstat`.
    # For testing, we'll mock the output of `top` to control CPU usage.
    local cpu_idle=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%*id.*/\1/")
    echo "scale=2; 100 - $cpu_idle" | bc
}

# Function to get Memory usage (used percentage)
get_mem_usage() {
    # Mock rationale: In a real scenario, this would execute `free`.
    # For testing, we'll mock the output of `free` to control memory usage.
    local mem_info=$(free -m | awk 'NR==2{print $3, $2}')
    local used_mem=$(echo $mem_info | awk '{print $1}')
    local total_mem=$(echo $mem_info | awk '{print $2}')
    if (( $(echo "$total_mem == 0" | bc -l) )); then
        echo "0.00"
    else
        echo "scale=2; ($used_mem * 100) / $total_mem" | bc
    fi
}

# Function to get Disk usage (root partition percentage)
get_disk_usage() {
    # Mock rationale: In a real scenario, this would execute `df`.
    # For testing, we'll mock the output of `df` to control disk usage.
    local disk_percent=$(df -h / | awk 'NR==2{print $5}' | sed 's/%//g')
    echo "$disk_percent"
}

main() {
    echo "🌌 Initiating Cosmic Vitality Scan... 🌌"
    echo "----------------------------------------"

    local cpu_usage=$(get_cpu_usage)
    local mem_usage=$(get_mem_usage)
    local disk_usage=$(get_disk_usage)

    local overall_vitality="OPTIMAL"
    local messages=()

    echo "CPU Core Resonance: ${cpu_usage}% utilized"
    if (( $(echo "$cpu_usage >= $CPU_THRESHOLD_HIGH" | bc -l) )); then
        messages+=("  - CPU Cores are humming a bit too intensely! Consider a moment of quiet contemplation.")
        overall_vitality="CRITICAL"
    elif (( $(echo "$cpu_usage >= ($CPU_THRESHOLD_HIGH / 2)" | bc -l) )); then
        messages+=("  - CPU Cores are resonating strongly. Keep an eye on those temporal fluctuations.")
        if [ "$overall_vitality" == "OPTIMAL" ]; then overall_vitality="ATTENTIVE"; fi
    fi

    echo "Memory Flow: ${mem_usage}% consumed"
    if (( $(echo "$mem_usage >= $MEM_THRESHOLD_HIGH" | bc -l) )); then
        messages+=("  - Memory Streams are overflowing! Your system's cosmic consciousness might be overwhelmed.")
        overall_vitality="CRITICAL"
    elif (( $(echo "$mem_usage >= ($MEM_THRESHOLD_HIGH / 2)" | bc -l) )); then
        messages+=("  - Memory Streams are flowing briskly. Ensure no ancient data spirits are clinging on.")
        if [ "$overall_vitality" == "OPTIMAL" ]; then overall_vitality="ATTENTIVE"; fi
    fi

    echo "Aetheric Storage: ${disk_usage}% occupied"
    if (( $(echo "$disk_usage >= $DISK_THRESHOLD_HIGH" | bc -l) )); then
        messages+=("  - Aetheric Storage is nearing capacity! Time to purge some forgotten relics from the void.")
        overall_vitality="CRITICAL"
    elif (( $(echo "$disk_usage >= ($DISK_THRESHOLD_HIGH / 2)" | bc -l) )); then
        messages+=("  - Aetheric Storage is comfortably full. A good time to organize your astral archives.")
        if [ "$overall_vitality" == "OPTIMAL" ]; then overall_vitality="ATTENTIVE"; fi
    fi

    echo "----------------------------------------"
    echo "Cosmic Vitality Status: $overall_vitality"

    if [ ${#messages[@]} -gt 0 ]; then
        echo "Observations from the Void:"
        for msg in "${messages[@]}"; do
            echo "$msg"
        done
        if [ "$overall_vitality" == "CRITICAL" ]; then
            echo "Urgent action required to restore cosmic balance!"
            return 1 # Indicate critical status
        fi
    else
        echo "All cosmic energies are in harmonious balance. Continue your journey through the temporal planes!"
    fi
    return 0 # Indicate healthy status
}

main "$@"
