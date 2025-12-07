#!/bin/bash

# Nightly Chaos Chaos Chaos 5
# A whimsical chaos engineering tool for resilience testing

set -euo pipefail

# Configuration
SCRIPT_NAME="$(basename "$0")"
LOG_FILE="/tmp/chaos_chaos_chaos_5.log"
NETWORK_INTERFACE="eth0"
DEFAULT_DURATION=60

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Print colored output
print_color() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_color "$RED" "Error: This script requires root privileges."
        echo "Please run with sudo: sudo $SCRIPT_NAME"
        exit 1
    fi
}

# Check if command exists
check_command() {
    local cmd=$1
    if ! command -v "$cmd" &> /dev/null; then
        print_color "$RED" "Error: Required command '$cmd' not found."
        exit 1
    fi
}

# Show help
show_help() {
    cat << EOF
${BLUE}Nightly Chaos Chaos Chaos 5${NC}

A whimsical chaos engineering tool for resilience testing

Usage:
    $SCRIPT_NAME [OPTIONS]

Options:
    --scenario SCENARIO    Chaos scenario to execute
                           Available: network-latency, service-disruption,
                           resource-exhaustion, random, time-manipulation
    --duration SECONDS     Duration for chaos (default: $DEFAULT_DURATION)
    --service NAME         Service name for disruption scenario
    --cpu PERCENT          CPU usage percentage for resource exhaustion
    --memory PERCENT       Memory usage percentage for resource exhaustion
    --offset SECONDS       Time offset in seconds for time manipulation
    --interface NAME       Network interface (default: $NETWORK_INTERFACE)
    --cleanup              Remove all chaos effects
    --help                 Show this help message

Examples:
    $SCRIPT_NAME --scenario network-latency --duration 60
    $SCRIPT_NAME --scenario service-disruption --service nginx
    $SCRIPT_NAME --scenario resource-exhaustion --cpu 80 --memory 50
    $SCRIPT_NAME --scenario random --duration 30
    $SCRIPT_NAME --scenario time-manipulation --offset -300
    $SCRIPT_NAME --cleanup

EOF
}

# Cleanup all chaos effects
cleanup() {
    print_color "$YELLOW" "🧹 Cleaning up all chaos effects..."
    
    # Remove network latency
    if tc qdisc show dev "$NETWORK_INTERFACE" 2>/dev/null | grep -q netem; then
        tc qdisc del dev "$NETWORK_INTERFACE" root 2>/dev/null || true
        log "Removed network latency from $NETWORK_INTERFACE"
    fi
    
    # Stop stress processes
    local stress_pids=$(pgrep -f "^stress " || true)
    if [[ -n "$stress_pids" ]]; then
        kill $stress_pids 2>/dev/null || true
        log "Stopped stress processes: $stress_pids"
    fi
    
    # Restart any stopped services (basic recovery)
    local stopped_services=$(systemctl list-units --type=service --state=failed --no-pager -q | awk '{print $1}' | grep -v "^UNIT" || true)
    if [[ -n "$stopped_services" ]]; then
        echo "$stopped_services" | while read service; do
            if [[ -n "$service" ]]; then
                systemctl restart "$service" 2>/dev/null || true
                log "Restarted failed service: $service"
            fi
        done
    fi
    
    # Reset system time if it was modified (basic check)
    hwclock --hctosys 2>/dev/null || true
    log "Reset system time from hardware clock"
    
    print_color "$GREEN" "✅ Cleanup complete!"
}

# Network latency scenario
scenario_network_latency() {
    local duration=${1:-$DEFAULT_DURATION}
    local delay=${2:-100}
    
    print_color "$BLUE" "🕸️  Injecting network latency ($delay ms) for $duration seconds..."
    
    # Add network delay
    tc qdisc add dev "$NETWORK_INTERFACE" root netem delay ${delay}ms 2>/dev/null || {
        tc qdisc change dev "$NETWORK_INTERFACE" root netem delay ${delay}ms
    }
    log "Added ${delay}ms network delay on $NETWORK_INTERFACE"
    
    # Wait for duration
    sleep "$duration"
    
    # Remove network delay
    tc qdisc del dev "$NETWORK_INTERFACE" root 2>/dev/null || true
    log "Removed network delay from $NETWORK_INTERFACE"
    
    print_color "$GREEN" "✅ Network latency test complete!"
}

# Service disruption scenario
scenario_service_disruption() {
    local service_name=$1
    local duration=${2:-$DEFAULT_DURATION}
    
    if [[ -z "$service_name" ]]; then
        print_color "$RED" "Error: Service name is required for service-disruption scenario"
        exit 1
    fi
    
    # Check if service exists
    if ! systemctl list-unit-files --type=service -q | grep -q "^$service_name.service"; then
        print_color "$RED" "Error: Service '$service_name' not found"
        exit 1
    fi
    
    print_color "$BLUE" "🛑 Stopping service '$service_name' for $duration seconds..."
    
    # Stop service
    systemctl stop "$service_name"
    log "Stopped service: $service_name"
    
    # Wait for duration
    sleep "$duration"
    
    # Restart service
    systemctl start "$service_name"
    log "Restarted service: $service_name"
    
    print_color "$GREEN" "✅ Service disruption test complete!"
}

# Resource exhaustion scenario
scenario_resource_exhaustion() {
    local duration=${1:-$DEFAULT_DURATION}
    local cpu_percent=${2:-50}
    local memory_percent=${3:-30}
    
    print_color "$BLUE" "🔥 Exhausting resources (CPU: ${cpu_percent}%, Memory: ${memory_percent}%) for $duration seconds..."
    
    # Calculate CPU cores and memory
    local cpu_cores=$(nproc)
    local cpu_workers=$((cpu_cores * cpu_percent / 100))
    local memory_gb=$(free -g | awk '/^Mem:/{print $2}')
    local memory_mb=$((memory_gb * 1024 * memory_percent / 100))
    
    # Start stress test
    stress --cpu "$cpu_workers" --timeout "${duration}s" --vm 1 --vm-bytes "${memory_mb}M" &
    local stress_pid=$!
    log "Started stress test (PID: $stress_pid) - CPU: $cpu_workers, Memory: ${memory_mb}M"
    
    # Wait for duration
    sleep "$duration"
    
    # Wait for stress to finish
    wait $stress_pid
    log "Stress test completed"
    
    print_color "$GREEN" "✅ Resource exhaustion test complete!"
}

# Random chaos scenario
scenario_random() {
    local duration=${1:-$DEFAULT_DURATION}
    local scenarios=("network-latency" "service-disruption" "resource-exhaustion")
    local random_scenario=${scenarios[$RANDOM % ${#scenarios[@]}]}
    
    print_color "$BLUE" "🎲 Random chaos scenario selected: $random_scenario"
    
    case "$random_scenario" in
        "network-latency")
            scenario_network_latency "$duration" "$(($RANDOM % 500 + 50))"
            ;;
        "service-disruption")
            # Get a random running service
            local services=$(systemctl list-units --type=service --state=running --no-pager -q | awk '{print $1}' | grep -v "^UNIT" | head -20)
            if [[ -z "$services" ]]; then
                print_color "$YELLOW" "No running services found, skipping service disruption"
                return 0
            fi
            local random_service=$(echo "$services" | shuf -n 1)
            scenario_service_disruption "$random_service" "$duration"
            ;;
        "resource-exhaustion")
            scenario_resource_exhaustion "$duration" "$(($RANDOM % 80 + 10))" "$(($RANDOM % 70 + 10))"
            ;;
    esac
}

# Time manipulation scenario
scenario_time_manipulation() {
    local offset=${1:-300}
    
    print_color "$BLUE" "⏰ Manipulating time by ${offset} seconds..."
    
    # Get current time
    local current_time=$(date +%s)
    local new_time=$((current_time + offset))
    
    # Set system time
    date -s "@$new_time" 2>/dev/null || {
        print_color "$YELLOW" "Warning: Could not set system time (requires root)"
    }
    log "Set system time from $current_time to $new_time (offset: $offset)"
    
    # Wait a moment
    sleep 2
    
    # Reset time
    hwclock --hctosys 2>/dev/null || true
    log "Reset system time from hardware clock"
    
    print_color "$GREEN" "✅ Time manipulation test complete!"
}

# Parse command line arguments
parse_args() {
    local scenario=""
    local duration=$DEFAULT_DURATION
    local service=""
    local cpu_percent=50
    local memory_percent=30
    local offset=300
    local cleanup=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --scenario)
                scenario="$2"
                shift 2
                ;;
            --duration)
                duration="$2"
                shift 2
                ;;
            --service)
                service="$2"
                shift 2
                ;;
            --cpu)
                cpu_percent="$2"
                shift 2
                ;;
            --memory)
                memory_percent="$2"
                shift 2
                ;;
            --offset)
                offset="$2"
                shift 2
                ;;
            --interface)
                NETWORK_INTERFACE="$2"
                shift 2
                ;;
            --cleanup)
                cleanup=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                print_color "$RED" "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Validate arguments
    if [[ "$cleanup" == "true" ]]; then
        cleanup
        exit 0
    fi
    
    if [[ -z "$scenario" ]]; then
        print_color "$RED" "Error: Scenario is required"
        show_help
        exit 1
    fi
    
    # Execute scenario
    case "$scenario" in
        network-latency)
            check_root
            check_command tc
            scenario_network_latency "$duration"
            ;;
        service-disruption)
            check_root
            check_command systemctl
            scenario_service_disruption "$service" "$duration"
            ;;
        resource-exhaustion)
            check_root
            check_command stress
            scenario_resource_exhaustion "$duration" "$cpu_percent" "$memory_percent"
            ;;
        random)
            check_root
            check_command tc
            check_command stress
            check_command systemctl
            scenario_random "$duration"
            ;;
        time-manipulation)
            check_root
            scenario_time_manipulation "$offset"
            ;;
        *)
            print_color "$RED" "Error: Unknown scenario '$scenario'"
            show_help
            exit 1
            ;;
    esac
}

# Main execution
main() {
    log "Starting Nightly Chaos Chaos Chaos 5"
    print_color "$BLUE" "🧪 Welcome to Nightly Chaos Chaos Chaos 5!"
    print_color "$BLUE" "⚠️  Use with caution - this is chaos engineering!"
    echo
    
    parse_args "$@"
    
    log "Chaos engineering session completed"
    print_color "$GREEN" "🎉 Chaos session complete! Check $LOG_FILE for details."
}

# Run main if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
