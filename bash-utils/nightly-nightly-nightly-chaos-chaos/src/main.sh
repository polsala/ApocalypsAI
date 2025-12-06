#!/bin/bash

# Nightly Nightly Chaos Chaos Chaos
# A whimsical chaos engineering tool for resilience testing

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="/tmp/chaos_chaos_chaos.log"
PID_FILE="/tmp/chaos_chaos_chaos.pid"

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

# Print banner
print_banner() {
    print_color "$RED" "╔══════════════════════════════════════════════════════════════╗"
    print_color "$RED" "║                    CHAOS CHAOS CHAOS!                      ║"
    print_color "$RED" "║              Bringing Order to Disorder!                   ║"
    print_color "$RED" "╚══════════════════════════════════════════════════════════════╝"
    echo
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_color "$YELLOW" "Warning: Not running as root. Some chaos may not work properly."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Help function
show_help() {
    cat << EOF
Usage: $0 [OPTIONS]

A whimsical chaos engineering tool that injects controlled mayhem into systems.

OPTIONS:
    --chaos TYPE           Run chaos of specified type (all|network|service|resource|time)
    --latency MS           Network latency in milliseconds (default: 100)
    --packet-loss PERCENT  Packet loss percentage (default: 5)
    --bandwidth KBPS       Bandwidth limit in kilobits per second (default: 1000)
    --services LIST        Comma-separated list of services to chaos (default: random)
    --cpu PERCENT          CPU usage percentage for stress (default: 50)
    --memory MB            Memory usage in megabytes for stress (default: 512)
    --time-shift SECONDS   Time shift in seconds (default: 3600)
    --duration SECONDS     Duration of chaos in seconds (default: 60)
    --cleanup              Clean up all chaos effects
    --list                 List available services for chaos
    --help                 Show this help message

CHAOS TYPES:
    all        Run all chaos scenarios
    network    Network latency, packet loss, and bandwidth limiting
    service    Random service restarts and stops
    resource   CPU, memory, and disk I/O stress
    time       System time manipulation

EXAMPLES:
    $0 --chaos network --latency 200 --packet-loss 10
    $0 --chaos service --services nginx,ssh
    $0 --chaos resource --cpu 80 --memory 2048
    $0 --chaos time --time-shift 7200
    $0 --cleanup

EOF
}

# Check dependencies
check_dependencies() {
    local missing=()
    
    command -v tc &> /dev/null || missing+=("tc (iproute2)")
    command -v stress &> /dev/null || missing+=("stress")
    command -v systemctl &> /dev/null || missing+=("systemctl (systemd)")
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        print_color "$RED" "Error: Missing dependencies: ${missing[*]}"
        print_color "$YELLOW" "Please install the missing dependencies and try again."
        exit 1
    fi
}

# Network chaos functions
apply_network_chaos() {
    local latency=${1:-100}
    local packet_loss=${2:-5}
    local bandwidth=${3:-1000}
    
    print_color "$BLUE" "🔧 Applying network chaos..."
    log "Starting network chaos: latency=${latency}ms, packet_loss=${packet_loss}%, bandwidth=${bandwidth}kbps"
    
    # Save original state
    tc qdisc show dev lo | grep -q "qdisc" && tc qdisc del dev lo root 2>/dev/null || true
    
    # Apply network chaos
    tc qdisc add dev lo root handle 1: netem delay ${latency}ms loss ${packet_loss}%
    tc qdisc add dev lo parent 1:1 handle 10: tbf rate ${bandwidth}kbit burst 32kbit latency 400ms
    
    print_color "$GREEN" "✓ Network chaos applied successfully!"
}

# Service chaos functions
get_available_services() {
    systemctl list-unit-files --type=service --state=enabled | awk '{print $1}' | grep -v "UNIT FILE" | sort
}

apply_service_chaos() {
    local services=${1:-""}
    local chaos_level=${2:-"medium"}
    
    print_color "$BLUE" "🔧 Applying service chaos..."
    log "Starting service chaos"
    
    if [[ -z "$services" ]]; then
        # Get random services
        local all_services=($(get_available_services))
        local num_services=${#all_services[@]}
        local num_to_chaos=$((num_services > 3 ? 3 : num_services))
        
        for i in $(seq 1 $num_to_chaos); do
            local random_index=$((RANDOM % num_services))
            services+="${all_services[$random_index]},"
        done
        services=${services%,} # Remove trailing comma
    fi
    
    log "Chaos services: $services"
    
    IFS=',' read -ra SERVICE_ARRAY <<< "$services"
    
    for service in "${SERVICE_ARRAY[@]}"; do
        service=$(echo "$service" | xargs) # Trim whitespace
        
        if ! systemctl list-unit-files --type=service | grep -q "^$service"; then
            print_color "$YELLOW" "⚠ Service '$service' not found, skipping"
            continue
        fi
        
        local action=$((RANDOM % 3))
        case $action in
            0)
                print_color "$BLUE" "🔄 Restarting service: $service"
                systemctl restart "$service" 2>&1 | tee -a "$LOG_FILE"
                ;;
            1)
                print_color "$BLUE" "🛑 Stopping service: $service"
                systemctl stop "$service" 2>&1 | tee -a "$LOG_FILE"
                sleep 2
                print_color "$BLUE" "🚀 Starting service: $service"
                systemctl start "$service" 2>&1 | tee -a "$LOG_FILE"
                ;;
            2)
                print_color "$BLUE" "⚡ Reloading service: $service"
                systemctl reload "$service" 2>&1 | tee -a "$LOG_FILE" || true
                ;;
        esac
    done
    
    print_color "$GREEN" "✓ Service chaos applied successfully!"
}

# Resource chaos functions
apply_resource_chaos() {
    local cpu_percent=${1:-50}
    local memory_mb=${2:-512}
    local duration=${3:-60}
    
    print_color "$BLUE" "🔧 Applying resource chaos..."
    log "Starting resource chaos: cpu=${cpu_percent}%, memory=${memory_mb}MB, duration=${duration}s"
    
    # Start stress in background
    stress --cpu $(nproc) --timeout ${duration}s --verbose &
    local cpu_pid=$!
    
    stress --vm 1 --vm-bytes ${memory_mb}M --timeout ${duration}s --verbose &
    local mem_pid=$!
    
    # Save PIDs for cleanup
    echo "$cpu_pid" > "/tmp/stress_cpu.pid"
    echo "$mem_pid" > "/tmp/stress_mem.pid"
    
    print_color "$GREEN" "✓ Resource chaos applied successfully!"
    print_color "$YELLOW" "Resource chaos will run for ${duration} seconds..."
}

# Time chaos functions
apply_time_chaos() {
    local shift_seconds=${1:-3600}
    
    print_color "$BLUE" "🔧 Applying time chaos..."
    log "Starting time chaos: shift=${shift_seconds} seconds"
    
    # Get current time
    local current_time=$(date)
    local new_time=$(date -d "${shift_seconds} seconds" +"%Y-%m-%d %H:%M:%S")
    
    print_color "$YELLOW" "Current time: $current_time"
    print_color "$YELLOW" "Shifting time by ${shift_seconds} seconds..."
    
    # Apply time shift
    date -s "${shift_seconds} seconds" 2>&1 | tee -a "$LOG_FILE"
    
    print_color "$GREEN" "✓ Time chaos applied successfully!"
    print_color "$YELLOW" "New time: $(date)"
}

# Cleanup functions
cleanup_network() {
    print_color "$BLUE" "🧹 Cleaning up network chaos..."
    tc qdisc del dev lo root 2>/dev/null || true
    log "Network chaos cleaned up"
    print_color "$GREEN" "✓ Network chaos cleaned up!"
}

cleanup_services() {
    print_color "$BLUE" "🧹 Cleaning up service chaos..."
    log "Cleaning up service chaos"
    
    # Restart any services that were stopped
    systemctl list-units --type=service --state=failed | awk 'NR>1 {print $1}' | while read service; do
        if [[ -n "$service" ]]; then
            print_color "$BLUE" "🔄 Attempting to restart failed service: $service"
            systemctl restart "$service" 2>&1 | tee -a "$LOG_FILE" || true
        fi
    done
    
    print_color "$GREEN" "✓ Service chaos cleaned up!"
}

cleanup_resources() {
    print_color "$BLUE" "🧹 Cleaning up resource chaos..."
    log "Cleaning up resource chaos"
    
    # Kill stress processes
    if [[ -f "/tmp/stress_cpu.pid" ]]; then
        kill $(cat "/tmp/stress_cpu.pid") 2>/dev/null || true
        rm -f "/tmp/stress_cpu.pid"
    fi
    
    if [[ -f "/tmp/stress_mem.pid" ]]; then
        kill $(cat "/tmp/stress_mem.pid") 2>/dev/null || true
        rm -f "/tmp/stress_mem.pid"
    fi
    
    # Kill any remaining stress processes
    pkill -f "^stress" 2>/dev/null || true
    
    print_color "$GREEN" "✓ Resource chaos cleaned up!"
}

cleanup_time() {
    print_color "$BLUE" "🧹 Cleaning up time chaos..."
    log "Cleaning up time chaos"
    
    # Reset time to NTP sync if available
    if command -v timedatectl &> /dev/null; then
        timedatectl set-ntp true 2>&1 | tee -a "$LOG_FILE"
        sleep 2
        timedatectl set-ntp false 2>&1 | tee -a "$LOG_FILE"
    fi
    
    print_color "$GREEN" "✓ Time chaos cleaned up!"
}

cleanup_all() {
    print_color "$RED" "🧹 Cleaning up ALL chaos..."
    cleanup_network
    cleanup_services
    cleanup_resources
    cleanup_time
    rm -f "$PID_FILE"
    log "All chaos cleaned up"
    print_color "$GREEN" "✓ All chaos has been cleaned up successfully!"
}

# List available services
list_services() {
    print_color "$BLUE" "📋 Available services for chaos:"
    get_available_services | head -20 | while read service; do
        echo "  - $service"
    done
    
    local total=$(get_available_services | wc -l)
    print_color "$YELLOW" "Total available services: $total"
}

# Main execution function
main() {
    local chaos_type=""
    local latency=100
    local packet_loss=5
    local bandwidth=1000
    local services=""
    local cpu_percent=50
    local memory_mb=512
    local time_shift=3600
    local duration=60
    local cleanup=false
    local list=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --chaos)
                chaos_type="$2"
                shift 2
                ;;
            --latency)
                latency="$2"
                shift 2
                ;;
            --packet-loss)
                packet_loss="$2"
                shift 2
                ;;
            --bandwidth)
                bandwidth="$2"
                shift 2
                ;;
            --services)
                services="$2"
                shift 2
                ;;
            --cpu)
                cpu_percent="$2"
                shift 2
                ;;
            --memory)
                memory_mb="$2"
                shift 2
                ;;
            --time-shift)
                time_shift="$2"
                shift 2
                ;;
            --duration)
                duration="$2"
                shift 2
                ;;
            --cleanup)
                cleanup=true
                shift
                ;;
            --list)
                list=true
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

# Print banner
print_banner

# Handle list option
if [[ "$list" == true ]]; then
    list_services
    exit 0
fi

# Handle cleanup option
if [[ "$cleanup" == true ]]; then
    cleanup_all
    exit 0
fi

# Validate chaos type
if [[ -z "$chaos_type" ]]; then
    print_color "$RED" "Error: --chaos option is required"
    show_help
    exit 1
fi

# Check root access
check_root

# Check dependencies
check_dependencies

# Record PID
echo $$ > "$PID_FILE"

# Execute chaos
log "Starting chaos execution: type=$chaos_type"

case "$chaos_type" in
    all)
        apply_network_chaos "$latency" "$packet_loss" "$bandwidth"
        apply_service_chaos "$services"
        apply_resource_chaos "$cpu_percent" "$memory_mb" "$duration"
        apply_time_chaos "$time_shift"
        
        print_color "$GREEN" "✓ All chaos applied! Waiting for duration..."
        sleep "$duration"
        
        cleanup_all
        ;;
    network)
        apply_network_chaos "$latency" "$packet_loss" "$bandwidth"
        print_color "$GREEN" "✓ Network chaos applied! Waiting for duration..."
        sleep "$duration"
        cleanup_network
        ;;
    service)
        apply_service_chaos "$services"
        print_color "$GREEN" "✓ Service chaos applied!"
        ;;
    resource)
        apply_resource_chaos "$cpu_percent" "$memory_mb" "$duration"
        print_color "$GREEN" "✓ Resource chaos applied! Waiting for duration..."
        sleep "$duration"
        cleanup_resources
        ;;
    time)
        apply_time_chaos "$time_shift"
        print_color "$GREEN" "✓ Time chaos applied! Waiting for duration..."
        sleep "$duration"
        cleanup_time
        ;;
    *)
        print_color "$RED" "Error: Invalid chaos type: $chaos_type"
        print_color "$YELLOW" "Valid types: all, network, service, resource, time"
        exit 1
        ;;
esac

log "Chaos execution completed"
print_color "$GREEN" "🎉 Chaos execution completed successfully!"
print_color "$BLUE" "Check the log file: $LOG_FILE"
}

# Trap to ensure cleanup on exit
trap 'cleanup_all; exit' EXIT INT TERM

# Run main function with all arguments
main "$@"
