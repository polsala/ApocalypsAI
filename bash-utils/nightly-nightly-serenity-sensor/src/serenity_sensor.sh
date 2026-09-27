#!/bin/bash

# Nightly System Serenity Sensor

# Configuration (can be overridden by environment variables or arguments)
DISK_THRESHOLD_CRITICAL=${DISK_THRESHOLD_CRITICAL:-90} # %
DISK_THRESHOLD_STRESSED=${DISK_THRESHOLD_STRESSED:-80} # %
MEM_THRESHOLD_CRITICAL=${MEM_THRESHOLD_CRITICAL:-90}   # %
MEM_THRESHOLD_STRESSED=${MEM_THRESHOLD_STRESSED:-80}   # %
LOAD_AVG_THRESHOLD_CRITICAL=${LOAD_AVG_THRESHOLD_CRITICAL:-5.0} # for 1-min avg
LOAD_AVG_THRESHOLD_STRESSED=${LOAD_AVG_THRESHOLD_STRESSED:-2.0} # for 1-min avg
CRITICAL_SERVICES=${CRITICAL_SERVICES:-"sshd cron"} # Space-separated list of services

# --- Helper Functions (for mocking in tests) ---

# Mock rationale: These functions wrap system commands to allow easy mocking
# by redefining them in tests. This ensures deterministic test results.

get_disk_usage() {
    df -P / | awk 'NR==2 {print $5}' | sed 's/%//'
}

get_mem_usage() {
    free | awk '/Mem:/ {printf "%.0f\n", $3/$2*100}'
}

get_load_average() {
    uptime | awk -F'load average: ' '{print $2}' | awk -F', ' '{print $1}'
}

is_service_active() {
    local service_name="$1"
    systemctl is-active "$service_name" &>/dev/null
}

# --- Serenity Checks ---

check_disk_serenity() {
    local usage=$(get_disk_usage)
    if [[ -z "$usage" ]]; then
        echo "  🕳️ Disk Serenity: UNKNOWN (Could not retrieve usage)"
        return 1
    fi

    if (( usage >= DISK_THRESHOLD_CRITICAL )); then
        echo "  🚨 Disk Serenity: CRITICAL! Disk space is at ${usage}%! Time for a digital declutter! 🧹"
        return 1
    elif (( usage >= DISK_THRESHOLD_STRESSED )); then
        echo "  ⚠️ Disk Serenity: STRESSED. Disk space is at ${usage}%. Consider archiving old logs. 📦"
        return 0
    else
        echo "  ✅ Disk Serenity: PEACEFUL. Disk space is at ${usage}%. Plenty of room to breathe. 🧘"
        return 0
    fi
}

check_mem_serenity() {
    local usage=$(get_mem_usage)
    if [[ -z "$usage" ]]; then
        echo "  🕳️ Memory Serenity: UNKNOWN (Could not retrieve usage)"
        return 1
    fi

    if (( usage >= MEM_THRESHOLD_CRITICAL )); then
        echo "  🚨 Memory Serenity: CRITICAL! Memory usage is at ${usage}%! Your system is gasping for air! 🌬️"
        return 1
    elif (( usage >= MEM_THRESHOLD_STRESSED )); then
        echo "  ⚠️ Memory Serenity: STRESSED. Memory usage is at ${usage}%. Perhaps a short nap (restart) would help? 😴"
        return 0
    else
        echo "  ✅ Memory Serenity: PEACEFUL. Memory usage is at ${usage}%. All thoughts are clear. ✨"
        return 0
    fi
}

check_cpu_load_serenity() {
    local load_avg=$(get_load_average)
    if [[ -z "$load_avg" ]]; then
        echo "  🕳️ CPU Load Serenity: UNKNOWN (Could not retrieve load average)"
        return 1
    fi

    # Convert to float for comparison using bc
    local load_avg_float=$(echo "$load_avg" | cut -d'.' -f1).$(echo "$load_avg" | cut -d'.' -f2)
    local critical_float=$(echo "$LOAD_AVG_THRESHOLD_CRITICAL" | cut -d'.' -f1).$(echo "$LOAD_AVG_THRESHOLD_CRITICAL" | cut -d'.' -f2)
    local stressed_float=$(echo "$LOAD_AVG_THRESHOLD_STRESSED" | cut -d'.' -f1).$(echo "$LOAD_AVG_THRESHOLD_STRESSED" | cut -d'.' -f2)

    if (( $(echo "$load_avg_float >= $critical_float" | bc -l) )); then
        echo "  🚨 CPU Load Serenity: CRITICAL! 1-min load average is ${load_avg}! Your CPU is running a marathon! 🏃"
        return 1
    elif (( $(echo "$load_avg_float >= $stressed_float" | bc -l) )); then
        echo "  ⚠️ CPU Load Serenity: STRESSED. 1-min load average is ${load_avg}. It needs a moment of quiet. 🤫"
        return 0
    else
        echo "  ✅ CPU Load Serenity: PEACEFUL. 1-min load average is ${load_avg}. Gently humming along. 🎶"
        return 0
    fi
}

check_service_serenity() {
    local overall_status=0
    echo "  Services Serenity:"
    for service in $CRITICAL_SERVICES; do
        if is_service_active "$service"; then
            echo "    ✅ Service '$service': Active. All systems go! 🚀"
        else
            echo "    🚨 Service '$service': INACTIVE! This needs attention! 🛑"
            overall_status=1
        fi
    done
    return $overall_status
}

# --- Main Report ---

generate_serenity_report() {
    local overall_serenity=0

    echo "--- Nightly System Serenity Report ($(date)) ---"
    echo ""

    check_disk_serenity || overall_serenity=1
    check_mem_serenity || overall_serenity=1
    check_cpu_load_serenity || overall_serenity=1
    check_service_serenity || overall_serenity=1

    echo ""
    if (( overall_serenity == 0 )); then
        echo "✨ Overall System Serenity: ALL IS WELL. The digital garden is thriving. Enjoy the peace! ✨"
    else
        echo "⚡ Overall System Serenity: CONCERNS DETECTED. Some aspects require your gentle attention. 🚧"
    fi
    echo "-------------------------------------------------"
    return $overall_serenity
}

# Run the report if the script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    generate_serenity_report "$@"
fi
