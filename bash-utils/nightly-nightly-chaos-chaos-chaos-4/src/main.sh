#!/bin/bash

# Nightly Chaos Chaos Chaos
# A whimsical chaos engineering tool for testing system resilience

set -euo pipefail

# Configuration
DEFAULT_INTERFACE="eth0"
DEFAULT_DURATION=30
DEFAULT_CPU_CORES=2
DEFAULT_MEMORY_GB=1
DEFAULT_DISK_GB=1
DEFAULT_LATENCY=50
DEFAULT_PACKET_LOSS=5
DEFAULT_BANDWIDTH=100

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        error "This script requires root privileges. Please run with sudo."
        exit 1
    fi
}

# Check dependencies
check_dependencies() {
    local missing=()
    
    command -v tc >/dev/null 2>&1 || missing+=("tc")
    command -v systemctl >/dev/null 2>&1 || missing+=("systemctl")
    command -v stress >/dev/null 2>&1 || missing+=("stress")
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        error "Missing dependencies: ${missing[*]}"
        error "Please install the required tools and try again."
        exit 1
    fi
}

# Network chaos functions
apply_network_chaos() {
    local interface=${1:-$DEFAULT_INTERFACE}
    local latency=${2:-$DEFAULT_LATENCY}
    local packet_loss=${3:-$DEFAULT_PACKET_LOSS}
    local bandwidth=${4:-$DEFAULT_BANDWIDTH}
    
    log "Applying network chaos on interface $interface"
    log "Latency: ${latency}ms, Packet Loss: ${packet_loss}%, Bandwidth: ${bandwidth}Mbps"
    
    # Add network latency, packet loss, and bandwidth limit
    tc qdisc add dev "$interface" root handle 1: htb default 12
    tc class add dev "$interface" parent 1: classid 1:12 htb rate ${bandwidth}mbit burst 15k
    tc qdisc add dev "$interface" parent 1:12 netem delay ${latency}ms loss ${packet_loss}%
    
    success "Network chaos applied successfully"
}

# Service chaos functions
apply_service_chaos() {
    local action=${1:-restart}
    local service=${2:-}
    
    if [[ -z "$service" ]]; then
        # Get a random service
        service=$(systemctl list-units --type=service --state=running --no-pager --no-legend | awk '{print $1}' | head -20 | shuf -n 1)
        if [[ -z "$service" ]]; then
            warning "No running services found, skipping service chaos"
            return 0
        fi
    fi
    
    log "Applying service chaos: $action on service $service"
    
    case "$action" in
        restart)
            systemctl restart "$service"
            success "Service $service restarted"
            ;;
        stop)
            systemctl stop "$service"
            success "Service $service stopped"
            ;;
        start)
            systemctl start "$service"
            success "Service $service started"
            ;;
        *)
            error "Unknown service action: $action"
            return 1
            ;;
    esac
}

# Resource chaos functions
apply_resource_chaos() {
    local cpu_cores=${1:-$DEFAULT_CPU_CORES}
    local memory_gb=${2:-$DEFAULT_MEMORY_GB}
    local timeout=${3:-$DEFAULT_DURATION}
    
    log "Applying resource chaos"
    log "CPU cores: $cpu_cores, Memory: ${memory_gb}GB, Timeout: ${timeout}s"
    
    # Stress CPU and memory
    stress --cpu $cpu_cores --vm $memory_gb --timeout ${timeout}s &
    local stress_pid=$!
    
    log "Resource stress started with PID: $stress_pid"
    log "Waiting ${timeout} seconds for stress test to complete..."
    
    # Wait for stress to complete or timeout
    sleep $((timeout + 2))
    
    if kill -0 $stress_pid 2>/dev/null; then
        kill $stress_pid 2>/dev/null || true
        warning "Stress test was terminated after timeout"
    else
        success "Resource stress completed successfully"
    fi
}

# Time chaos functions
apply_time_chaos() {
    local offset=${1:--1}
    
    log "Applying time chaos: shifting system time by ${offset} hour(s)"
    
    # Backup current time
    local current_time=$(date '+%Y-%m-%d %H:%M:%S')
    log "Current time: $current_time"
    
    # Shift time
    date -s "$offset hours" >/dev/null 2>&1
    local new_time=$(date '+%Y-%m-%d %H:%M:%S')
    log "New time: $new_time"
    
    success "Time chaos applied successfully"
}

# Random chaos functions
apply_random_chaos() {
    local chaos_type=("network" "services" "resources" "time")
    local random_type=${chaos_type[$RANDOM % ${#chaos_type[@]}]}
    
    log "Random chaos selected: $random_type"
    
    case "$random_type" in
        network)
            local interfaces=("eth0" "eth1" "wlan0" "enp0s3")
            local interface=${interfaces[$RANDOM % ${#interfaces[@]}]}
            local latency=$((RANDOM % 200 + 10))
            local packet_loss=$((RANDOM % 20 + 1))
            local bandwidth=$((RANDOM % 500 + 50))
            apply_network_chaos "$interface" $latency $packet_loss $bandwidth
            ;;
        services)
            local actions=("restart" "stop" "start")
            local action=${actions[$RANDOM % ${#actions[@]}]}
            apply_service_chaos "$action"
            ;;
        resources)
            local cpu_cores=$((RANDOM % 4 + 1))
            local memory_gb=$((RANDOM % 4 + 1))
            local timeout=$((RANDOM % 60 + 10))
            apply_resource_chaos $cpu_cores $memory_gb $timeout
            ;;
        time)
            local offset=$((RANDOM % 24 - 12))
            apply_time_chaos $offset
            ;;
    esac
}

# Cleanup functions
cleanup_network() {
    local interface=${1:-$DEFAULT_INTERFACE}
    
    log "Cleaning up network chaos on interface $interface"
    
    # Remove traffic control rules
    tc qdisc del dev "$interface" root 2>/dev/null || true
    tc qdisc del dev "$interface" ingress 2>/dev/null || true
    
    success "Network chaos cleaned up"
}

cleanup_services() {
    log "Cleaning up service chaos"
    # Note: Services that were stopped will need manual restart
    # This is intentional for chaos engineering
    warning "Services that were stopped will need manual restart"
    success "Service chaos cleanup completed"
}

cleanup_resources() {
    log "Cleaning up resource chaos"
    
    # Kill any running stress processes
    pkill -f "stress" 2>/dev/null || true
    
    success "Resource chaos cleaned up"
}

cleanup_time() {
    log "Cleaning up time chaos"
    
    # Sync time with NTP
    if command -v timedatectl >/dev/null 2>&1; then
        timedatectl set-ntp true 2>/dev/null || true
        timedatectl set-ntp false 2>/dev/null || true
    fi
    
    # Try to sync with NTP pool
    ntpdate -s time.nist.gov 2>/dev/null || true
    
    success "Time chaos cleaned up"
}

cleanup_all() {
    log "Cleaning up all chaos effects"
    cleanup_network
    cleanup_services
    cleanup_resources
    cleanup_time
    success "All chaos effects cleaned up"
}

# Help function
show_help() {
    cat << EOF
Nightly Chaos Chaos Chaos - Chaos Engineering Tool

Usage: $0 [OPTIONS]

OPTIONS:
    --all                   Run all chaos scenarios
    --network              Apply network chaos
    --services             Apply service chaos
    --resources            Apply resource chaos
    --time                 Apply time chaos
    --random               Apply random chaos
    --cleanup              Clean up all chaos effects
    --help                 Show this help message

NETWORK OPTIONS:
    --interface INTERFACE  Network interface (default: $DEFAULT_INTERFACE)
    --latency MS           Network latency in milliseconds (default: $DEFAULT_LATENCY)
    --packet-loss PERCENT  Packet loss percentage (default: $DEFAULT_PACKET_LOSS)
    --bandwidth MBPS       Bandwidth limit in Mbps (default: $DEFAULT_BANDWIDTH)

SERVICE OPTIONS:
    --action ACTION        Service action: restart, stop, start (default: restart)
    --service NAME         Specific service name (random if not specified)

RESOURCE OPTIONS:
    --cpu CORES            Number of CPU cores to stress (default: $DEFAULT_CPU_CORES)
    --memory GB            Amount of memory to stress in GB (default: $DEFAULT_MEMORY_GB)
    --timeout SECONDS      Duration of stress test in seconds (default: $DEFAULT_DURATION)

TIME OPTIONS:
    --offset HOURS         Time offset in hours (default: -1)

EXAMPLES:
    $0 --all
    $0 --network --interface eth0 --latency 100
    $0 --services --action restart --service nginx
    $0 --resources --cpu 4 --memory 2 --timeout 60
    $0 --time --offset -2
    $0 --random
    $0 --cleanup

EOF
}

# Parse arguments
parse_args() {
    local action=""
    local interface="$DEFAULT_INTERFACE"
    local latency="$DEFAULT_LATENCY"
    local packet_loss="$DEFAULT_PACKET_LOSS"
    local bandwidth="$DEFAULT_BANDWIDTH"
    local service_action="restart"
    local service_name=""
    local cpu_cores="$DEFAULT_CPU_CORES"
    local memory_gb="$DEFAULT_MEMORY_GB"
    local timeout="$DEFAULT_DURATION"
    local time_offset="-1"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --all)
                action="all"
                shift
                ;;
            --network)
                action="network"
                shift
                ;;
            --services)
                action="services"
                shift
                ;;
            --resources)
                action="resources"
                shift
                ;;
            --time)
                action="time"
                shift
                ;;
            --random)
                action="random"
                shift
                ;;
            --cleanup)
                action="cleanup"
                shift
                ;;
            --interface)
                interface="$2"
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
            --action)
                service_action="$2"
                shift 2
                ;;
            --service)
                service_name="$2"
                shift 2
                ;;
            --cpu)
                cpu_cores="$2"
                shift 2
                ;;
            --memory)
                memory_gb="$2"
                shift 2
                ;;
            --timeout)
                timeout="$2"
                shift 2
                ;;
            --offset)
                time_offset="$2"
                shift 2
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Execute action
    case "$action" in
        all)
            check_root
            check_dependencies
            apply_network_chaos "$interface" $latency $packet_loss $bandwidth
            apply_service_chaos "$service_action" "$service_name"
            apply_resource_chaos $cpu_cores $memory_gb $timeout
            apply_time_chaos $time_offset
            ;;
        network)
            check_root
            check_dependencies
            apply_network_chaos "$interface" $latency $packet_loss $bandwidth
            ;;
        services)
            check_root
            check_dependencies
            apply_service_chaos "$service_action" "$service_name"
            ;;
        resources)
            check_root
            check_dependencies
            apply_resource_chaos $cpu_cores $memory_gb $timeout
            ;;
        time)
            check_root
            check_dependencies
            apply_time_chaos $time_offset
            ;;
        random)
            check_root
            check_dependencies
            apply_random_chaos
            ;;
        cleanup)
            check_root
            cleanup_all
            ;;
        "")
            error "No action specified"
            show_help
            exit 1
            ;;
    esac
}

# Main execution
main() {
    log "Starting Nightly Chaos Chaos Chaos"
    parse_args "$@"
    success "Chaos engineering session completed"
}

# Run main if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
