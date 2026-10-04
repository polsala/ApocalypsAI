#!/bin/bash

# Default thresholds
DEFAULT_CPU_THRESHOLD=80 # Percentage
DEFAULT_MEM_THRESHOLD=80 # Percentage
DEFAULT_DISK_THRESHOLD=90 # Percentage
DEFAULT_DISK_PATH="/"

# Omen messages
OMENS_CPU=(
    "The CPU core hums with an unnatural fervor, a sign of impending digital maelstrom!"
    "A spectral load weighs heavily on the processor; the gears of fate grind slowly."
    "Beware the flickering CPU lights, for they foretell a tempest of computations!"
    "The silicon heart races, a frantic beat against the coming storm."
)
OMENS_MEM=(
    "Memory's grasp loosens, and whispers of the void consume precious bytes."
    "The RAM shimmers with an ethereal glow, stretched thin by unseen forces."
    "A vast emptiness threatens to swallow the system's thoughts; memory wanes."
    "The well of memory runs dry, a parched landscape awaiting the deluge."
)
OMENS_DISK=(
    "The digital earth groans, its storage capacity nearing a critical mass."
    "Beware the encroaching data shadows; disk space dwindles like sand in an hourglass."
    "The archives of the apocalypse swell; disk space is a fleeting luxury."
    "The storage monolith trembles, burdened by the weight of forgotten data."
)

# Function to get CPU usage (idle percentage)
get_cpu_idle() {
    # Mock rationale: In tests, this function will be overridden to return a fixed value.
    # For actual execution, it parses 'top' output.
    if command -v top &> /dev/null; then
        # Get CPU idle percentage from top, average over 1 second
        # This is a common way to get CPU usage on Linux
        top -bn1 | grep "Cpu(s)" | \
            awk '{print $8}' | cut -d'.' -f1
    else
        echo "0" # Fallback if top is not available
    fi
}

# Function to get Memory usage (used percentage)
get_mem_used() {
    # Mock rationale: In tests, this function will be overridden to return a fixed value.
    # For actual execution, it parses 'free' output.
    if command -v free &> /dev/null; then
        # Get total and used memory in MB, calculate percentage
        read -r _ total_mem used_mem <<< $(free -m | grep Mem: | awk '{print $2, $3}')
        if [[ "$total_mem" -gt 0 ]]; then
            echo $(( (used_mem * 100) / total_mem ))
        else
            echo "0"
        fi
    else
        echo "0" # Fallback if free is not available
    fi
}

# Function to get Disk usage (used percentage)
get_disk_used() {
    local path="$1"
    # Mock rationale: In tests, this function will be overridden to return a fixed value.
    # For actual execution, it parses 'df' output.
    if command -v df &> /dev/null; then
        # Get disk usage percentage for a given path
        df -h "$path" 2>/dev/null | grep "$path" | awk '{print $5}' | sed 's/%//'
    else
        echo "0" # Fallback if df is not available
    fi
}

# Function to pick a random omen
pick_omen() {
    local -n omens_array="$1" # Use nameref for array
    local num_omens=${#omens_array[@]}
    if [[ "$num_omens" -eq 0 ]]; then
        echo "No omens available for this category."
        return 1
    fi
    # Mock rationale: In tests, RANDOM will be controlled or the function mocked.
    # For actual execution, it picks a random element.
    echo "${omens_array[$(( RANDOM % num_omens ))]}"
}

# Main logic
main() {
    local cpu_threshold="${1:-$DEFAULT_CPU_THRESHOLD}"
    local mem_threshold="${2:-$DEFAULT_MEM_THRESHOLD}"
    local disk_threshold="${3:-$DEFAULT_DISK_THRESHOLD}"
    local disk_path="${4:-$DEFAULT_DISK_PATH}"
    local log_file="${5}"

    local current_cpu_idle=$(get_cpu_idle)
    local current_cpu_used=$((100 - current_cpu_idle))
    local current_mem_used=$(get_mem_used)
    local current_disk_used=$(get_disk_used "$disk_path")

    local omen_triggered=false
    local output_message=""

    output_message+="Resource Omen Scan Report ($(date +'%Y-%m-%d %H:%M:%S')):\n"
    output_message+="  CPU Usage: ${current_cpu_used}% (Threshold: ${cpu_threshold}%)\n"
    output_message+="  Memory Usage: ${current_mem_used}% (Threshold: ${mem_threshold}%)\n"
    output_message+="  Disk Usage (${disk_path}): ${current_disk_used}% (Threshold: ${disk_threshold}%)\n"

    if [[ "$current_cpu_used" -ge "$cpu_threshold" ]]; then
        output_message+="  CPU OMEN: $(pick_omen OMENS_CPU)\n"
        omen_triggered=true
    fi

    if [[ "$current_mem_used" -ge "$mem_threshold" ]]; then
        output_message+="  MEMORY OMEN: $(pick_omen OMENS_MEM)\n"
        omen_triggered=true
    fi

    if [[ "$current_disk_used" -ge "$disk_threshold" ]]; then
        output_message+="  DISK OMEN: $(pick_omen OMENS_DISK)\n"
        omen_triggered=true
    fi

    if ! $omen_triggered; then
        output_message+="  All systems nominal. The void slumbers... for now.\n"
    fi

    echo -e "$output_message"

    if [[ -n "$log_file" ]]; then
        echo -e "$output_message" >> "$log_file"
        echo "Report logged to $log_file"
    fi

    if $omen_triggered; then
        return 1 # Indicate an omen was triggered
    else
        return 0 # Indicate no omen was triggered
    fi
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
