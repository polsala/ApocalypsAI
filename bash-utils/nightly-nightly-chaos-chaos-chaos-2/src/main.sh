#!/bin/bash

# Nightly Chaos Chaos Chaos
# A whimsical chaos engineering tool for testing system resilience
# Usage: ./src/main.sh <chaos_type> <chaos_subtype> <parameters>

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="/tmp/chaos_chaos_chaos.log"
STATE_FILE="/tmp/chaos_state.json"
DEFAULT_DURATION=300  # 5 minutes in seconds

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
        print_color "$RED" "Error: This script requires root privileges. Please run with sudo."
        exit 1
    fi
}

# Check dependencies
check_dependencies() {
    local deps=()
    
    case "$1" in
        "network")
            deps+=("tc")
            ;;
        "resource")
            deps+=("stress")
            ;;
        "service")
            deps+=("systemctl")
            ;;
        "time")
            # No specific dependencies for time manipulation
            ;;
    esac
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            print_color "$RED" "Error: Required dependency '$dep' is not installed."
            exit 1
        fi
    done
}

# Initialize state file
init_state() {
    if [[ ! -f "$STATE_FILE" ]]; then
        echo '{}' > "$STATE_FILE"
    fi
}

# Save state
save_state() {
    local chaos_type=$1
    local chaos_subtype=$2
    local params=$3
    local timestamp=$(date +%s)
    
    # Simple state management using jq if available, otherwise basic file operations
    if command -v jq &> /dev/null; then
        jq --arg type "$chaos_type" --arg subtype "$chaos_subtype" --arg params "$params" --arg ts "$timestamp" '
            .chaos_events += [{
                "type": $type,
                "subtype": $subtype,
                "params": $params,
                "timestamp": ($ts | tonumber)
            }]
        ' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
    else
        echo "Chaos Event: $chaos_type $chaos_subtype $params at $(date)" >> "$STATE_FILE"
    fi
}

# Network chaos functions
network_chaos() {
    local subtype=$1
    shift
    local params=("$@")
    
    case "$subtype" in
        "latency")
            network_latency "${params[@]}"
            ;;
        "packet-loss")
            network_packet_loss "${params[@]}"
            ;;
        "bandwidth")
            network_bandwidth "${params[@]}"
            ;;
        *)
            print_color "$RED" "Error: Unknown network chaos subtype '$subtype'"
            print_color "$YELLOW" "Usage: network [latency|packet-loss|bandwidth] <parameters>"
            exit 1
            ;;
    esac
}

network_latency() {
    local delay=$1
    local interface=${2:-eth0}
    local duration=${3:-$DEFAULT_DURATION}
    
    print_color "$BLUE" "Injecting $delay latency on interface $interface for ${duration}s..."
    
    # Add latency
    tc qdisc add dev "$interface" root netem delay "$delay" 2>/dev/null || \
        tc qdisc change dev "$interface" root netem delay "$delay"
    
    save_state "network" "latency" "$delay $interface $duration"
    log "Applied latency: $delay on $interface"
    
    # Schedule cleanup
    (sleep "$duration" && cleanup_network "$interface") &
    
    print_color "$GREEN" "Latency chaos applied successfully!"
}

network_packet_loss() {
    local loss=$1
    local interface=${2:-eth0}
    local duration=${3:-$DEFAULT_DURATION}
    
    print_color "$BLUE" "Injecting $loss packet loss on interface $interface for ${duration}s..."
    
    # Add packet loss
    tc qdisc add dev "$interface" root netem loss "$loss" 2>/dev/null || \
        tc qdisc change dev "$interface" root netem loss "$loss"
    
    save_state "network" "packet-loss" "$loss $interface $duration"
    log "Applied packet loss: $loss on $interface"
    
    # Schedule cleanup
    (sleep "$duration" && cleanup_network "$interface") &
    
    print_color "$GREEN" "Packet loss chaos applied successfully!"
}

network_bandwidth() {
    local rate=$1
    local interface=${2:-eth0}
    local duration=${3:-$DEFAULT_DURATION}
    
    print_color "$BLUE" "Throttling bandwidth to $rate on interface $interface for ${duration}s..."
    
    # Add bandwidth limit
    tc qdisc add dev "$interface" root tbf rate "$rate" burst 32kbit latency 400ms 2>/dev/null || \
        tc qdisc change dev "$interface" root tbf rate "$rate" burst 32kbit latency 400ms
    
    save_state "network" "bandwidth" "$rate $interface $duration"
    log "Applied bandwidth limit: $rate on $interface"
    
    # Schedule cleanup
    (sleep "$duration" && cleanup_network "$interface") &
    
    print_color "$GREEN" "Bandwidth chaos applied successfully!"
}

cleanup_network() {
    local interface=$1
    
    print_color "$YELLOW" "Cleaning up network chaos on interface $interface..."
    
    # Remove all qdiscs
    tc qdisc del dev "$interface" root 2>/dev/null || true
    tc qdisc del dev "$interface" ingress 2>/dev/null || true
    
    log "Cleaned up network chaos on $interface"
    print_color "$GREEN" "Network chaos cleaned up!"
}

# Resource chaos functions
resource_chaos() {
    local subtype=$1
    shift
    local params=("$@")
    
    case "$subtype" in
        "cpu")
            resource_cpu "${params[@]}"
            ;;
        "memory")
            resource_memory "${params[@]}"
            ;;
        *)
            print_color "$RED" "Error: Unknown resource chaos subtype '$subtype'"
            print_color "$YELLOW" "Usage: resource [cpu|memory] <parameters>"
            exit 1
            ;;
    esac
}

resource_cpu() {
    local utilization=$1
    local duration=${2:-$DEFAULT_DURATION}
    local cores=${3:-$(nproc)}
    
    print_color "$BLUE" "Spiking CPU usage to ${utilization}% on $cores cores for ${duration}s..."
    
    # Calculate number of workers needed for target utilization
    local workers=$((cores * utilization / 100))
    if [[ $workers -lt 1 ]]; then
        workers=1
    fi
    
    # Start stress test
    stress --cpu "$workers" --timeout "${duration}s" &
    local stress_pid=$!
    
    save_state "resource" "cpu" "$utilization $duration $cores $stress_pid"
    log "Started CPU stress: $utilization% for ${duration}s with $workers workers"
    
    print_color "$GREEN" "CPU chaos applied successfully!"
}

resource_memory() {
    local percentage=$1
    local duration=${2:-$DEFAULT_DURATION}
    local workers=${3:-1}
    
    # Get total memory in MB
    local total_mem=$(grep MemTotal /proc/meminfo | awk '{print $2}')
    local mem_to_consume=$((total_mem * percentage / 100 / 1024))
    
    print_color "$BLUE" "Consuming ${mem_to_consume}MB memory (${percentage}%) for ${duration}s..."
    
    # Start memory stress
    stress --vm "$workers" --vm-bytes "${mem_to_consume}M" --timeout "${duration}s" &
    local stress_pid=$!
    
    save_state "resource" "memory" "$percentage $duration $workers $mem_to_consume $stress_pid"
    log "Started memory stress: ${percentage}% (${mem_to_consume}MB) for ${duration}s"
    
    print_color "$GREEN" "Memory chaos applied successfully!"
}

# Service chaos functions
service_chaos() {
    local subtype=$1
    shift
    local service_name=$1
    local probability=${2:-50}
    
    print_color "$BLUE" "Preparing $subtype chaos for service '$service_name' with ${probability}% probability..."
    
    # Check if service exists
    if ! systemctl list-unit-files | grep -q "^$service_name"; then
        print_color "$RED" "Error: Service '$service_name' not found"
        exit 1
    fi
    
    # Generate random number to decide if chaos should be applied
    local rand=$((RANDOM % 100))
    
    if [[ $rand -lt $probability ]]; then
        case "$subtype" in
            "restart")
                print_color "$YELLOW" "Chaos triggered! Restarting service '$service_name'..."
                systemctl restart "$service_name"
                save_state "service" "restart" "$service_name"
                log "Restarted service: $service_name"
                print_color "$GREEN" "Service chaos applied successfully!"
                ;;
            "stop")
                print_color "$YELLOW" "Chaos triggered! Stopping service '$service_name'..."
                systemctl stop "$service_name"
                save_state "service" "stop" "$service_name"
                log "Stopped service: $service_name"
                print_color "$GREEN" "Service chaos applied successfully!"
                ;;
            *)
                print_color "$RED" "Error: Unknown service chaos subtype '$subtype'"
                exit 1
                ;;
        esac
    else
        print_color "$BLUE" "Chaos not triggered this time (random roll: $rand)"
        log "Service chaos skipped for $service_name (random roll: $rand)"
    fi
}

# Time chaos functions
time_chaos() {
    local subtype=$1
    shift
    local params=("$@")
    
    case "$subtype" in
        "shift")
            time_shift "${params[@]}"
            ;;
        *)
            print_color "$RED" "Error: Unknown time chaos subtype '$subtype'"
            print_color "$YELLOW" "Usage: time [shift] <parameters>"
            exit 1
            ;;
    esac
}

time_shift() {
    local shift_amount=$1
    
    print_color "$BLUE" "Shifting system time by $shift_amount..."
    print_color "$YELLOW" "Warning: This may require special permissions and can affect system stability!"
    
    # Note: Direct time manipulation is dangerous and often restricted
    # This is a placeholder for more sophisticated time manipulation
    # that might be implemented using tools like chrony or ntpd
    
    case "$shift_amount" in
        +*)
            local seconds=${shift_amount#+}
            if [[ $seconds == *'s'* ]]; then
                seconds=${seconds%s}
            elif [[ $seconds == *'m'* ]]; then
                seconds=$((seconds% * 60))
            elif [[ $seconds == *'h'* ]]; then
                seconds=$((seconds% * 3600))
            fi
            print_color "$YELLOW" "Would shift time forward by ${seconds} seconds"
            log "Time shift chaos: forward by ${seconds} seconds"
            ;;
        -*)
            local seconds=${shift_amount#-}
            if [[ $seconds == *'s'* ]]; then
                seconds=${seconds%s}
            elif [[ $seconds == *'m'* ]]; then
                seconds=$((seconds% * 60))
            elif [[ $seconds == *'h'* ]]; then
                seconds=$((seconds% * 3600))
            fi
            print_color "$YELLOW" "Would shift time backward by ${seconds} seconds"
            log "Time shift chaos: backward by ${seconds} seconds"
            ;;
        *)
            print_color "$RED" "Error: Invalid time shift format. Use +1h, -30m, +120s, etc."
            exit 1
            ;;
    esac
    
    save_state "time" "shift" "$shift_amount"
    print_color "$GREEN" "Time chaos applied successfully!"
}

# Cleanup function
cleanup_all() {
    local chaos_type=${1:-all}
    
    print_color "$YELLOW" "Cleaning up all chaos effects..."
    
    case "$chaos_type" in
        "network"|"all")
            # Clean up all network interfaces
            for interface in $(ip link show | grep '^[0-9]' | awk -F': ' '{print $2}' | grep -v 'lo'); do
                cleanup_network "$interface"
            done
            ;;
        "resource")
            # Kill all stress processes
            pkill -f "^stress" 2>/dev/null || true
            log "Killed all stress processes"
            ;;
        "service")
            # Restart all services that were stopped
            # This is a simplified version - in practice, you'd track which services were affected
            print_color "$BLUE" "Note: Service cleanup requires manual intervention"
            print_color "$BLUE" "Consider restarting services that may have been affected"
            ;;
        "time")
            print_color "$BLUE" "Time chaos cleanup requires manual intervention"
            print_color "$BLUE" "Consider synchronizing time with NTP: sudo ntpdate -s time.nist.gov"
            ;;
        "all")
            # Clean up everything
            cleanup_all "network"
            cleanup_all "resource"
            cleanup_all "service"
            cleanup_all "time"
            ;;
        *)
            print_color "$RED" "Error: Unknown cleanup type '$chaos_type'"
            exit 1
            ;;
    esac
    
    log "Completed cleanup for type: $chaos_type"
    print_color "$GREEN" "Cleanup completed!"
}

# Help function
show_help() {
    cat << EOF
Nightly Chaos Chaos Chaos - Whimsical Chaos Engineering Tool

Usage: $0 <chaos_type> <chaos_subtype> <parameters>

CHAOS TYPES:
  network     Network-related chaos (latency, packet loss, bandwidth)
  resource    Resource-related chaos (CPU, memory)
  service     Service-related chaos (restart, stop)
  time        Time-related chaos (shift)
  cleanup     Clean up chaos effects
  help        Show this help message

NETWORK CHAOS:
  $0 network latency <delay> [interface] [duration]
    Example: $0 network latency 100ms eth0 300
  
  $0 network packet-loss <percentage> [interface] [duration]
    Example: $0 network packet-loss 10% eth0 300
  
  $0 network bandwidth <rate> [interface] [duration]
    Example: $0 network bandwidth 1Mbps eth0 300

RESOURCE CHAOS:
  $0 resource cpu <utilization> [duration] [cores]
    Example: $0 resource cpu 80 300 4
  
  $0 resource memory <percentage> [duration] [workers]
    Example: $0 resource memory 50 300 2

SERVICE CHAOS:
  $0 service restart <service_name> [probability]
    Example: $0 service restart apache2 75
  
  $0 service stop <service_name> [probability]
    Example: $0 service stop nginx 50

TIME CHAOS:
  $0 time shift <amount>
    Example: $0 time shift +1h
    Example: $0 time shift -30m

CLEANUP:
  $0 cleanup [type]
    Types: network, resource, service, time, all
    Example: $0 cleanup network
    Example: $0 cleanup all

OPTIONS:
  --duration <seconds>  Set duration for chaos effects
  --dry-run            Show what would be done without executing

EXAMPLES:
  $0 network latency 150ms
  $0 resource cpu 90 --duration 600
  $0 service restart mysql 80
  $0 cleanup all

EOF
}

# Dry run mode
dry_run() {
    print_color "$YELLOW" "DRY RUN MODE - The following actions would be performed:"
    print_color "$BLUE" "Chaos Type: $1"
    print_color "$BLUE" "Chaos Subtype: $2"
    print_color "$BLUE" "Parameters: $3"
    print_color "$GREEN" "No actual changes were made."
}

# Main function
main() {
    # Initialize
    init_state
    
    # Check if help is requested
    if [[ ${1:-} == "help" ]] || [[ ${1:-} == "--help" ]] || [[ ${1:-} == "-h" ]]; then
        show_help
        exit 0
    fi
    
    # Check if enough arguments
    if [[ $# -lt 2 ]]; then
        print_color "$RED" "Error: Insufficient arguments"
        show_help
        exit 1
    fi
    
    local chaos_type=$1
    shift
    local chaos_subtype=$1
    shift
    
    # Check for dry run
    local dry_run_mode=false
    if [[ " $@ " == *" --dry-run "* ]]; then
        dry_run_mode=true
        # Remove --dry-run from arguments
        set -- $(echo "$@" | sed 's/--dry-run//')
    fi
    
    # Handle cleanup separately
    if [[ $chaos_type == "cleanup" ]]; then
        cleanup_all "$chaos_subtype"
        exit 0
    fi
    
    # Check dependencies
    check_dependencies "$chaos_type"
    
    # Check root privileges for most operations
    if [[ $chaos_type != "help" ]] && [[ $chaos_type != "time" ]] || [[ $dry_run_mode == false ]]; then
        check_root
    fi
    
    # Execute chaos
    case "$chaos_type" in
        "network")
            if [[ $dry_run_mode == true ]]; then
                dry_run "network" "$chaos_subtype" "$@"
            else
                network_chaos "$chaos_subtype" "$@"
            fi
            ;;
        "resource")
            if [[ $dry_run_mode == true ]]; then
                dry_run "resource" "$chaos_subtype" "$@"
            else
                resource_chaos "$chaos_subtype" "$@"
            fi
            ;;
        "service")
            if [[ $dry_run_mode == true ]]; then
                dry_run "service" "$chaos_subtype" "$@"
            else
                service_chaos "$chaos_subtype" "$@"
            fi
            ;;
        "time")
            if [[ $dry_run_mode == true ]]; then
                dry_run "time" "$chaos_subtype" "$@"
            else
                time_chaos "$chaos_subtype" "$@"
            fi
            ;;
        *)
            print_color "$RED" "Error: Unknown chaos type '$chaos_type'"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
