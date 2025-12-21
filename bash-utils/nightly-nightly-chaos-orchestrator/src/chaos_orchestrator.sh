#!/bin/bash

# Nightly Chaos Orchestrator
# A whimsical chaos engineering tool for testing system resilience
# Author: ApocalypsAI
# License: MIT

set -euo pipefail

# Configuration defaults
CHAOS_LEVEL="mild"
CHAOS_DURATION=300
CHAOS_INTERVAL=60
ENABLE_PROCESS_CHAOS=true
ENABLE_NETWORK_CHAOS=true
ENABLE_DISK_CHAOS=true
ENABLE_FILE_CHAOS=true
SAFETY_MODE=true
DRY_RUN=false
LOG_FILE="/tmp/chaos_orchestrator.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Critical processes that should never be killed
CRITICAL_PROCESSES=(
    "systemd"
    "kernel"
    "init"
    "sshd"
    "bash"
    "sh"
    "python"
    "python3"
    "java"
    "node"
    "nginx"
    "apache"
    "mysql"
    "postgres"
    "docker"
    "kubernetes"
)

# Critical paths that should never be touched
CRITICAL_PATHS=(
    "/bin"
    "/sbin"
    "/usr"
    "/etc"
    "/lib"
    "/lib64"
    "/boot"
    "/dev"
    "/proc"
    "/sys"
    "/tmp"
)

# Logging function
log() {
    local level="$1"
    local message="$2"
    local timestamp="$(date '+%Y-%m-%d %H:%M:%S')"
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

# Print colored output
print_status() {
    local color="$1"
    local message="$2"
    echo -e "${color}$message${NC}"
}

# Print usage information
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Nightly Chaos Orchestrator - Test your system's resilience!

OPTIONS:
    -l, --level LEVEL       Chaos level: mild, moderate, severe (default: mild)
    -d, --duration SECONDS  Duration to run chaos (default: 300)
    -i, --interval SECONDS  Interval between chaos events (default: 60)
    -c, --config FILE       Configuration file path
    --dry-run              Show what would happen without doing it
    --report               Generate chaos report
    -h, --help             Show this help message

EXAMPLES:
    $0                                    # Run with default settings
    $0 --level moderate --duration 600    # Moderate chaos for 10 minutes
    $0 --dry-run                          # See what would happen

SAFETY:
    Always use in controlled environments only!
    Never run on production systems.

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -l|--level)
                CHAOS_LEVEL="$2"
                shift 2
                ;;
            -d|--duration)
                CHAOS_DURATION="$2"
                shift 2
                ;;
            -i|--interval)
                CHAOS_INTERVAL="$2"
                shift 2
                ;;
            -c|--config)
                CONFIG_FILE="$2"
                shift 2
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --report)
                generate_report
                exit 0
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
}

# Load configuration file
load_config() {
    if [[ -n "${CONFIG_FILE:-}" && -f "$CONFIG_FILE" ]]; then
        log "INFO" "Loading configuration from $CONFIG_FILE"
        source "$CONFIG_FILE"
    fi
}

# Initialize logging
init_logging() {
    if [[ "$DRY_RUN" == "true" ]]; then
        LOG_FILE="/dev/null"
    else
        mkdir -p "$(dirname "$LOG_FILE")"
        echo "# Chaos Orchestrator Log - $(date)" > "$LOG_FILE"
    fi
}

# Check if running as root (required for some operations)
check_privileges() {
    if [[ $EUID -eq 0 ]]; then
        log "INFO" "Running with root privileges - full chaos capabilities enabled"
        return 0
    else
        log "WARN" "Not running as root - some chaos operations will be limited"
        return 1
    fi
}

# Check if system is in a safe state for chaos
check_safety() {
    if [[ "$SAFETY_MODE" == "true" ]]; then
        # Check if we're in a VM or container
        if [[ -f /proc/vz ]] || grep -q "qemu" /proc/cpuinfo 2>/dev/null; then
            log "INFO" "Detected virtualized environment - safety checks passed"
            return 0
        fi
        
        # Check disk space
        local disk_usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
        if [[ $disk_usage -gt 80 ]]; then
            log "ERROR" "Disk usage is above 80% - aborting for safety"
            return 1
        fi
        
        log "INFO" "Safety checks passed"
    fi
    return 0
}

# Get random process to kill
get_random_process() {
    local pids=($(ps -eo pid --no-headers | grep -v "^\s*1\s*$"))
    local random_pid=${pids[$RANDOM % ${#pids[@]}]}
    
    # Check if process is critical
    local process_name=$(ps -p $random_pid -o comm= 2>/dev/null || echo "")
    
    if [[ -n "$process_name" ]]; then
        for critical in "${CRITICAL_PROCESSES[@]}"; do
            if [[ "$process_name" == *"$critical"* ]]; then
                log "DEBUG" "Skipping critical process: $process_name"
                return 1
            fi
        done
        echo "$random_pid:$process_name"
        return 0
    fi
    return 1
}

# Kill random process
chaos_kill_process() {
    if [[ "$ENABLE_PROCESS_CHAOS" != "true" ]]; then
        return 0
    fi
    
    local process_info=$(get_random_process)
    if [[ -n "$process_info" ]]; then
        local pid=$(echo "$process_info" | cut -d: -f1)
        local name=$(echo "$process_info" | cut -d: -f2)
        
        if [[ "$DRY_RUN" == "true" ]]; then
            log "DRY_RUN" "Would kill process $name (PID: $pid)"
            return 0
        fi
        
        log "CHAOS" "Killing process $name (PID: $pid)"
        if kill -TERM "$pid" 2>/dev/null; then
            log "INFO" "Successfully killed process $name"
            sleep 2
            # Force kill if still running
            kill -KILL "$pid" 2>/dev/null || true
        else
            log "WARN" "Failed to kill process $name"
        fi
    fi
}

# Add network latency
chaos_network_latency() {
    if [[ "$ENABLE_NETWORK_CHAOS" != "true" ]]; then
        return 0
    fi
    
    # Only run if we have tc command and root privileges
    if ! command -v tc &> /dev/null; then
        log "WARN" "tc command not found - skipping network chaos"
        return 0
    fi
    
    if [[ $EUID -ne 0 ]]; then
        log "WARN" "Root privileges required for network chaos - skipping"
        return 0
    fi
    
    # Get network interface
    local interface=$(ip route | grep default | awk '{print $5}' | head -1)
    if [[ -z "$interface" ]]; then
        log "WARN" "No network interface found - skipping network chaos"
        return 0
    fi
    
    # Determine delay based on chaos level
    local delay=50
    case "$CHAOS_LEVEL" in
        "moderate") delay=200 ;;
        "severe") delay=500 ;;
    esac
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log "DRY_RUN" "Would add ${delay}ms latency to interface $interface"
        return 0
    fi
    
    log "CHAOS" "Adding ${delay}ms latency to interface $interface"
    
    # Clean up any existing qdisc
    tc qdisc del dev "$interface" root 2>/dev/null || true
    
    # Add new qdisc with delay
    tc qdisc add dev "$interface" root netem delay "${delay}ms"
    
    # Schedule removal after a short time
    (
        sleep 30
        tc qdisc del dev "$interface" root 2>/dev/null || true
        log "INFO" "Removed network latency from $interface"
    ) &
}

# Fill disk space temporarily
chaos_fill_disk() {
    if [[ "$ENABLE_DISK_CHAOS" != "true" ]]; then
        return 0
    fi
    
    # Check current disk usage
    local disk_usage=$(df /tmp | tail -1 | awk '{print $5}' | sed 's/%//')
    if [[ $disk_usage -gt 70 ]]; then
        log "WARN" "Disk usage already high ($disk_usage%) - skipping disk chaos"
        return 0
    fi
    
    # Determine fill size based on chaos level
    local fill_size=100
    case "$CHAOS_LEVEL" in
        "moderate") fill_size=500 ;;
        "severe") fill_size=1000 ;;
    esac
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log "DRY_RUN" "Would fill ${fill_size}MB of disk space"
        return 0
    fi
    
    log "CHAOS" "Filling ${fill_size}MB of disk space"
    
    # Create temporary file
    local temp_file="/tmp/chaos_$(date +%s)_$RANDOM"
    dd if=/dev/zero of="$temp_file" bs=1M count=$fill_size 2>/dev/null || true
    
    # Schedule cleanup
    (
        sleep 60
        rm -f "$temp_file"
        log "INFO" "Cleaned up temporary disk fill file"
    ) &
}

# Create file system errors
chaos_file_errors() {
    if [[ "$ENABLE_FILE_CHAOS" != "true" ]]; then
        return 0
    fi
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log "DRY_RUN" "Would create temporary file system errors"
        return 0
    fi
    
    log "CHAOS" "Creating temporary file system errors"
    
    # Create a read-only bind mount to simulate file system errors
    local temp_dir="/tmp/chaos_mount_$$"
    mkdir -p "$temp_dir"
    
    # Try to create a read-only mount (requires root)
    if [[ $EUID -eq 0 ]]; then
        mount --bind /tmp "$temp_dir" 2>/dev/null || true
        mount -o remount,ro "$temp_dir" 2>/dev/null || true
        
        # Schedule unmount
        (
            sleep 30
            umount "$temp_dir" 2>/dev/null || true
            rmdir "$temp_dir" 2>/dev/null || true
            log "INFO" "Removed temporary file system error"
        ) &
    else
        # Without root, just create some problematic files
        touch "$temp_dir/.hidden_chaos_file"
        chmod 000 "$temp_dir/.hidden_chaos_file" 2>/dev/null || true
        
        (
            sleep 30
            chmod 644 "$temp_dir/.hidden_chaos_file" 2>/dev/null || true
            rm -rf "$temp_dir"
        ) &
    fi
}

# Generate chaos report
generate_report() {
    if [[ ! -f "$LOG_FILE" ]]; then
        echo "No log file found at $LOG_FILE"
        return 1
    fi
    
    echo "=== Chaos Orchestrator Report ==="
    echo "Log file: $LOG_FILE"
    echo "Generated: $(date)"
    echo ""
    
    echo "--- Summary ---"
    echo "Total chaos events: $(grep -c "CHAOS" "$LOG_FILE")"
    echo "Process kills: $(grep -c "Killing process" "$LOG_FILE")"
    echo "Network latency events: $(grep -c "Adding.*ms latency" "$LOG_FILE")"
    echo "Disk fill events: $(grep -c "Filling.*MB" "$LOG_FILE")"
    echo "File system errors: $(grep -c "Creating temporary file system errors" "$LOG_FILE")"
    echo ""
    
    echo "--- Recent Events ---"
    tail -20 "$LOG_FILE"
    echo ""
    
    echo "--- Recommendations ---"
    local process_kills=$(grep -c "Killing process" "$LOG_FILE")
    local network_events=$(grep -c "Adding.*ms latency" "$LOG_FILE")
    
    if [[ $process_kills -gt 5 ]]; then
        echo "⚠️  High process kill rate detected - consider implementing process resurrection"
    fi
    
    if [[ $network_events -gt 3 ]]; then
        echo "⚠️  Frequent network latency - implement timeout and retry mechanisms"
    fi
    
    if [[ $process_kills -eq 0 && $network_events -eq 0 ]]; then
        echo "✅ No chaos events detected - system may be too stable or chaos level too low"
    fi
}

# Main chaos execution loop
run_chaos() {
    local start_time=$(date +%s)
    local end_time=$((start_time + CHAOS_DURATION))
    
    log "INFO" "Starting chaos orchestration with level: $CHAOS_LEVEL"
    log "INFO" "Duration: ${CHAOS_DURATION}s, Interval: ${CHAOS_INTERVAL}s"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        print_status "$YELLOW" "DRY RUN MODE - No actual chaos will be performed"
    fi
    
    while [[ $(date +%s) -lt $end_time ]]; do
        # Select random chaos type
        local chaos_types=("process" "network" "disk" "file")
        local random_type=${chaos_types[$RANDOM % ${#chaos_types[@]}]}
        
        case "$random_type" in
            "process")
                chaos_kill_process
                ;;
            "network")
                chaos_network_latency
                ;;
            "disk")
                chaos_fill_disk
                ;;
            "file")
                chaos_file_errors
                ;;
        esac
        
        # Wait for next interval
        sleep "$CHAOS_INTERVAL"
    done
    
    log "INFO" "Chaos orchestration completed"
    print_status "$GREEN" "Chaos session finished! Check the log at $LOG_FILE"
}

# Cleanup function
cleanup() {
    log "INFO" "Cleaning up chaos artifacts"
    
    # Remove any network latency
    local interface=$(ip route | grep default | awk '{print $5}' | head -1)
    if [[ -n "$interface" ]]; then
        tc qdisc del dev "$interface" root 2>/dev/null || true
    fi
    
    # Clean up any temporary files
    find /tmp -name "chaos_*" -type f -delete 2>/dev/null || true
    find /tmp -name "chaos_mount_*" -type d -exec umount {} \; 2>/dev/null || true
    find /tmp -name "chaos_mount_*" -type d -delete 2>/dev/null || true
    
    log "INFO" "Cleanup completed"
}

# Signal handlers
trap cleanup EXIT
trap 'log "INFO" "Chaos orchestration interrupted"; exit 1' INT TERM

# Main execution
main() {
    print_status "$BLUE" "=== Nightly Chaos Orchestrator ==="
    print_status "$BLUE" "Testing your system's resilience since 2024"
    echo ""
    
    # Parse arguments
    parse_args "$@"
    
    # Load configuration
    load_config
    
    # Initialize
    init_logging
    
    # Check prerequisites
    check_privileges
    check_safety
    
    # Run chaos
    run_chaos
    
    # Generate report
    if [[ "$DRY_RUN" != "true" ]]; then
        echo ""
        generate_report
    fi
}

# Run if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
