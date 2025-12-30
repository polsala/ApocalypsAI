#!/bin/bash

# Nightly Chaos Orchestrator
# A whimsical chaos engineering tool for testing system resilience

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="/tmp/chaos_orchestrator.log"
PID_FILE="/tmp/chaos_orchestrator.pid"
MAX_DURATION="1h"
DEFAULT_DURATION="30s"

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

# Error handling
error_exit() {
    log "${RED}ERROR: $1${NC}"
    cleanup
    exit 1
}

# Success message
success() {
    log "${GREEN}SUCCESS: $1${NC}"
}

# Warning message
warning() {
    log "${YELLOW}WARNING: $1${NC}"
}

# Info message
info() {
    log "${BLUE}INFO: $1${NC}"
}

# Help function
show_help() {
    cat << EOF
Nightly Chaos Orchestrator - Chaos Engineering Tool

Usage: $0 [OPTIONS]

OPTIONS:
    --scenario SCENARIO     Chaos scenario to run (network, resource, service, time, random)
    --duration DURATION     Duration of chaos (e.g., 30s, 1m, 2h)
    --services LIST         Comma-separated list of services for service chaos
    --action ACTION         Action for service chaos (restart, kill, freeze)
    --cpu PERCENT           CPU usage percentage for resource chaos
    --memory PERCENT        Memory usage percentage for resource chaos
    --latency MS            Network latency in milliseconds
    --packet-loss PERCENT   Packet loss percentage for network chaos
    --corruption PERCENT    Packet corruption percentage for network chaos
    --interval DURATION     Interval between chaos actions
    --report                Generate chaos report
    --history               Show chaos execution history
    --cleanup               Clean up chaos artifacts
    --help                  Show this help message

EXAMPLES:
    $0 --scenario network --duration 30s
    $0 --scenario resource --cpu 80 --memory 50 --duration 1m
    $0 --scenario service --services nginx,redis --action restart
    $0 --scenario random --duration 5m

EOF
}

# Parse duration string to seconds
parse_duration() {
    local duration="$1"
    local seconds=0
    
    if [[ "$duration" =~ ^([0-9]+)(s|m|h)$ ]]; then
        local value="${BASH_REMATCH[1]}"
        local unit="${BASH_REMATCH[2]}"
        
        case "$unit" in
            s) seconds=$((value)) ;;
            m) seconds=$((value * 60)) ;;
            h) seconds=$((value * 3600)) ;;
        esac
        
        # Enforce maximum duration
        local max_seconds=3600  # 1 hour
        if [ "$seconds" -gt "$max_seconds" ]; then
            error_exit "Duration cannot exceed $MAX_DURATION"
        fi
        
        echo "$seconds"
    else
        error_exit "Invalid duration format: $duration. Use format like 30s, 1m, 2h"
    fi
}

# Check if running as root (for some chaos operations)
check_root() {
    if [ "$EUID" -ne 0 ]; then
        warning "Some chaos operations require root privileges. Some features may be limited."
        return 1
    fi
    return 0
}

# Network chaos functions
network_chaos_start() {
    local latency="${1:-0}"
    local packet_loss="${2:-0}"
    local corruption="${3:-0}"
    
    info "Starting network chaos..."
    
    # Check if tc (traffic control) is available
    if ! command -v tc &> /dev/null; then
        warning "tc command not found. Network chaos requires traffic control tools."
        return 1
    fi
    
    # Create network namespace for testing if not root
    if ! check_root; then
        warning "Network chaos requires root privileges for full functionality."
    fi
    
    # Apply network delays and packet loss using tc
    if check_root; then
        # Backup original rules
        tc qdisc add dev lo root handle 1: prio &> /dev/null || true
        
        if [ "$latency" -gt 0 ]; then
            tc qdisc add dev lo parent 1:1 handle 10: netem delay "${latency}ms" &> /dev/null || true
            info "Added ${latency}ms latency to loopback interface"
        fi
        
        if [ "$packet_loss" -gt 0 ]; then
            tc qdisc add dev lo parent 1:1 handle 10: netem loss "${packet_loss}%" &> /dev/null || true
            info "Added ${packet_loss}% packet loss to loopback interface"
        fi
        
        if [ "$corruption" -gt 0 ]; then
            tc qdisc add dev lo parent 1:1 handle 10: netem corrupt "${corruption}%" &> /dev/null || true
            info "Added ${corruption}% packet corruption to loopback interface"
        fi
    else
        # Simulate network issues using iptables or other methods
        info "Simulating network issues (limited functionality without root)"
    fi
}

network_chaos_stop() {
    info "Stopping network chaos..."
    
    if check_root; then
        tc qdisc del dev lo root &> /dev/null || true
        tc qdisc del dev eth0 root &> /dev/null || true
        tc qdisc del dev wlan0 root &> /dev/null || true
    fi
}

# Resource chaos functions
resource_chaos_start() {
    local cpu_percent="${1:-50}"
    local memory_percent="${2:-50}"
    
    info "Starting resource chaos..."
    
    # CPU stress
    if [ "$cpu_percent" -gt 0 ]; then
        local cpu_cores=$(nproc)
        local cpu_workers=$((cpu_cores * cpu_percent / 100))
        
        if [ "$cpu_workers" -lt 1 ]; then
            cpu_workers=1
        fi
        
        info "Starting $cpu_workers CPU stress workers"
        for i in $(seq 1 "$cpu_workers"); do
            (while true; do :; done) &
        done
    fi
    
    # Memory stress
    if [ "$memory_percent" -gt 0 ]; then
        local total_mem=$(free -m | awk 'NR==2{printf "%.0f", $2}')
        local mem_to_consume=$((total_mem * memory_percent / 100))
        
        info "Consuming ${mem_to_consume}MB of memory"
        # Create memory-consuming process
        dd if=/dev/zero of=/dev/shm/chaos_mem bs=1M count="$mem_to_consume" &> /dev/null &
    fi
}

resource_chaos_stop() {
    info "Stopping resource chaos..."
    
    # Kill CPU stress processes
    pkill -f "while true; do :; done" &> /dev/null || true
    
    # Clean up memory consumption
    rm -f /dev/shm/chaos_mem &> /dev/null || true
    sync
}

# Service chaos functions
service_chaos_start() {
    local services="$1"
    local action="${2:-restart}"
    
    info "Starting service chaos on: $services"
    
    IFS=',' read -ra SERVICE_ARRAY <<< "$services"
    
    for service in "${SERVICE_ARRAY[@]}"; do
        case "$action" in
            restart)
                if systemctl is-active --quiet "$service" 2>/dev/null; then
                    info "Restarting service: $service"
                    systemctl restart "$service" &> /dev/null || warning "Failed to restart $service"
                else
                    warning "Service $service is not active"
                fi
                ;;
            kill)
                if systemctl is-active --quiet "$service" 2>/dev/null; then
                    info "Killing service: $service"
                    systemctl stop "$service" &> /dev/null || warning "Failed to stop $service"
                else
                    warning "Service $service is not active"
                fi
                ;;
            freeze)
                if systemctl is-active --quiet "$service" 2>/dev/null; then
                    info "Freezing service: $service"
                    systemctl kill --signal=STOP "$service" &> /dev/null || warning "Failed to freeze $service"
                else
                    warning "Service $service is not active"
                fi
                ;;
            *)
                warning "Unknown service action: $action"
                ;;
        esac
    done
}

service_chaos_stop() {
    info "Stopping service chaos..."
    # Services are typically left in their current state for testing purposes
    # Could add logic to restore original state if needed
}

# Time chaos functions
 time_chaos_start() {
    local time_factor="${1:-1}"
    
    info "Starting time chaos with factor: $time_factor"
    
    # Note: Actual time manipulation requires kernel modules or specialized tools
    # This is a placeholder for time-related chaos
    if [ "$time_factor" != "1" ]; then
        warning "Time manipulation requires specialized tools and root privileges"
        info "Logging time manipulation attempt for simulation purposes"
    fi
}

 time_chaos_stop() {
    info "Stopping time chaos..."
    # Restore normal time if manipulation was applied
}

# Random chaos function
random_chaos_start() {
    local scenarios=("network" "resource" "service" "time")
    local random_scenario="${scenarios[$RANDOM % ${#scenarios[@]}]}"
    
    info "Random chaos selected: $random_scenario"
    
    case "$random_scenario" in
        network)
            local latency=$((RANDOM % 500))
            local packet_loss=$((RANDOM % 50))
            network_chaos_start "$latency" "$packet_loss" "0"
            ;;
        resource)
            local cpu=$((RANDOM % 90 + 10))
            local memory=$((RANDOM % 80 + 10))
            resource_chaos_start "$cpu" "$memory"
            ;;
        service)
            # Try to find some common services to mess with
            local common_services=("nginx" "apache2" "redis" "mysql" "postgresql")
            local service="${common_services[$RANDOM % ${#common_services[@]}]}"
            local actions=("restart" "kill" "freeze")
            local action="${actions[$RANDOM % ${#actions[@]}]}"
            service_chaos_start "$service" "$action"
            ;;
        time)
            local factor=$((RANDOM % 5 + 1))
            time_chaos_start "$factor"
            ;;
    esac
}

random_chaos_stop() {
    network_chaos_stop
    resource_chaos_stop
    service_chaos_stop
    time_chaos_stop
}

# Cleanup function
cleanup() {
    info "Cleaning up chaos artifacts..."
    
    network_chaos_stop
    resource_chaos_stop
    service_chaos_stop
    time_chaos_stop
    
    # Remove PID file
    rm -f "$PID_FILE"
    
    success "Cleanup completed"
}

# Generate chaos report
 generate_report() {
    info "Generating chaos report..."
    
    local report_file="/tmp/chaos_report_$(date +%Y%m%d_%H%M%S).txt"
    
    cat > "$report_file" << EOF
# Chaos Engineering Report

**Generated:** $(date)
**Duration:** $DURATION seconds
**Scenario:** $SCENARIO

## System Information
- Hostname: $(hostname)
- OS: $(uname -s)
- Kernel: $(uname -r)
- CPU Cores: $(nproc)
- Total Memory: $(free -h | awk 'NR==2{print $2}')

## Chaos Applied
$CHAOS_SUMMARY

## System Response
$(free -h)

$(df -h)

## Log Summary
$(tail -20 "$LOG_FILE")

EOF
    
    success "Report generated: $report_file"
    cat "$report_file"
}

# Show chaos history
show_history() {
    info "Showing chaos execution history..."
    
    if [ -f "$LOG_FILE" ]; then
        grep "CHAOS STARTED\|CHAOS ENDED\|ERROR\|SUCCESS" "$LOG_FILE" | tail -20
    else
        warning "No chaos history found"
    fi
}

# Main execution function
main() {
    local scenario=""
    local duration="$DEFAULT_DURATION"
    local services=""
    local action="restart"
    local cpu_percent="50"
    local memory_percent="50"
    local latency="0"
    local packet_loss="0"
    local corruption="0"
    local interval="0"
    local report=false
    local history=false
    local cleanup_only=false
    
    # Parse command line arguments
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
            --services)
                services="$2"
                shift 2
                ;;
            --action)
                action="$2"
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
            --latency)
                latency="$2"
                shift 2
                ;;
            --packet-loss)
                packet_loss="$2"
                shift 2
                ;;
            --corruption)
                corruption="$2"
                shift 2
                ;;
            --interval)
                interval="$2"
                shift 2
                ;;
            --report)
                report=true
                shift
                ;;
            --history)
                history=true
                shift
                ;;
            --cleanup)
                cleanup_only=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                error_exit "Unknown option: $1"
                ;;
        esac
    done
    
    # Validate inputs
    if [ -z "$scenario" ] && [ "$history" = false ] && [ "$cleanup_only" = false ]; then
        error_exit "Scenario is required. Use --help for usage information."
    fi
    
    if [ "$scenario" != "" ] && [[ ! "$scenario" =~ ^(network|resource|service|time|random)$ ]]; then
        error_exit "Invalid scenario: $scenario. Must be one of: network, resource, service, time, random"
    fi
    
    if [ "$cpu_percent" -lt 0 ] || [ "$cpu_percent" -gt 100 ]; then
        error_exit "CPU percentage must be between 0 and 100"
    fi
    
    if [ "$memory_percent" -lt 0 ] || [ "$memory_percent" -gt 100 ]; then
        error_exit "Memory percentage must be between 0 and 100"
    fi
    
    if [ "$packet_loss" -lt 0 ] || [ "$packet_loss" -gt 100 ]; then
        error_exit "Packet loss percentage must be between 0 and 100"
    fi
    
    if [ "$corruption" -lt 0 ] || [ "$corruption" -gt 100 ]; then
        error_exit "Packet corruption percentage must be between 0 and 100"
    fi
    
    # Convert duration to seconds
    DURATION=$(parse_duration "$duration")
    
    # Handle special commands
    if [ "$history" = true ]; then
        show_history
        exit 0
    fi
    
    if [ "$cleanup_only" = true ]; then
        cleanup
        exit 0
    fi
    
    # Start chaos
    info "CHAOS STARTED: Scenario=$scenario, Duration=${DURATION}s"
    echo $$ > "$PID_FILE"
    
    # Record chaos summary for report
    CHAOS_SUMMARY="Scenario: $scenario\nDuration: ${DURATION}s"
    
    case "$scenario" in
        network)
            network_chaos_start "$latency" "$packet_loss" "$corruption"
            ;;
        resource)
            resource_chaos_start "$cpu_percent" "$memory_percent"
            ;;
        service)
            if [ -z "$services" ]; then
                error_exit "Services list is required for service chaos"
            fi
            service_chaos_start "$services" "$action"
            ;;
        time)
            time_chaos_start
            ;;
        random)
            random_chaos_start
            ;;
    esac
    
    # Wait for duration
    sleep "$DURATION"
    
    # Stop chaos
    case "$scenario" in
        network)
            network_chaos_stop
            ;;
        resource)
            resource_chaos_stop
            ;;
        service)
            service_chaos_stop
            ;;
        time)
            time_chaos_stop
            ;;
        random)
            random_chaos_stop
            ;;
    esac
    
    info "CHAOS ENDED: Scenario=$scenario, Duration=${DURATION}s"
    
    # Generate report if requested
    if [ "$report" = true ]; then
        generate_report
    fi
    
    success "Chaos orchestration completed successfully"
}

# Trap signals for cleanup
trap cleanup EXIT

# Run main function with all arguments
main "$@"
