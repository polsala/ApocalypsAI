#!/bin/bash

# Nightly Chaos Chaos Chaos
# A whimsical chaos engineering toolkit

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Configuration
DEFAULT_DURATION="30s"
DEFAULT_CPU_CORES="1"
DEFAULT_MEMORY_MB="256"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
  echo -e "${GREEN}[CHAOS]${NC} $1"
}

warn() {
  echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
check_root() {
  if [[ $EUID -ne 0 ]]; then
    error "This script must be run as root for chaos injection"
    exit 1
  fi
}

# Check dependencies
check_deps() {
  local missing=()
  
  command -v tc >/dev/null 2>&1 || missing+=("tc")
  command -v stress >/dev/null 2>&1 || missing+=("stress")
  command -v systemctl >/dev/null 2>&1 || missing+=("systemctl")
  
  if [[ ${#missing[@]} -gt 0 ]]; then
    error "Missing dependencies: ${missing[*]}"
    error "Please install: apt-get install -y ${missing[*]}"
    exit 1
  fi
}

# Network chaos - add latency
chaos_network() {
  local duration="${1:-$DEFAULT_DURATION}"
  local latency="${2:-100ms}"
  
  log "Injecting network chaos: ${latency} latency for ${duration}"
  
  # Add network delay
  tc qdisc add dev lo root netem delay ${latency} 2>/dev/null || true
  
  # Schedule cleanup
  (sleep ${duration} && tc qdisc del dev lo root 2>/dev/null || true) &
  
  log "Network chaos scheduled. Cleanup in ${duration}"
}

# Service chaos - stop/start services randomly
chaos_service() {
  local service_name="${1:-}""
  
  if [[ -z "$service_name" ]]; then
    # Get random running service
    service_name=$(systemctl list-units --type=service --state=running --no-pager --no-legend | awk '{print $1}' | grep -v "systemd" | shuf -n 1)
    if [[ -z "$service_name" ]]; then
      warn "No running services found to chaos"
      return 0
    fi
  fi
  
  log "Injecting service chaos on: $service_name"
  
  # Stop service
  systemctl stop "$service_name" 2>/dev/null || true
  
  # Schedule restart
  (sleep 10 && systemctl start "$service_name" 2>/dev/null || true) &
  
  log "Service $service_name stopped. Will restart in 10s"
}

# Resource chaos - CPU and memory exhaustion
chaos_resource() {
  local cpu_cores="${1:-$DEFAULT_CPU_CORES}"
  local memory_mb="${2:-$DEFAULT_MEMORY_MB}"
  local duration="${3:-$DEFAULT_DURATION}"
  
  log "Injecting resource chaos: ${cpu_cores} cores, ${memory_mb}MB for ${duration}"
  
  # Start stress in background
  stress --cpu ${cpu_cores} --vm 1 --vm-bytes ${memory_mb}M --timeout ${duration} >/dev/null 2>&1 &
  local stress_pid=$!
  
  # Store PID for cleanup
  echo $stress_pid > /tmp/chaos_stress.pid
  
  log "Resource chaos started (PID: $stress_pid). Will cleanup in ${duration}"
}

# Random chaos - pick a random chaos mode
chaos_random() {
  local modes=("network" "service" "resource" "time")
  local mode=${modes[$RANDOM % ${#modes[@]}]}
  
  log "Random chaos mode selected: $mode"
  
  case $mode in
    "network")
      chaos_network "10s" "50ms"
      ;;
    "service")
      chaos_service
      ;;
    "resource")
      chaos_resource "1" "128" "10s"
      ;;
    "time")
      chaos_time "+5 minutes"
      ;;
  esac
}

# Time chaos - manipulate system time
chaos_time() {
  local offset="${1:-+1 hour}"
  
  log "Injecting time chaos: offset ${offset}"
  warn "Note: This is a demo. Real time manipulation requires additional privileges."
  
  # Show what time would be
  local new_time=$(date -d "${offset}")
  log "Current time would become: $new_time"
}

# Cleanup all chaos
cleanup() {
  log "Cleaning up all chaos..."
  
  # Clean network
  tc qdisc del dev lo root 2>/dev/null || true
  
  # Clean resources
  if [[ -f /tmp/chaos_stress.pid ]]; then
    local pid=$(cat /tmp/chaos_stress.pid)
    kill $pid 2>/dev/null || true
    rm -f /tmp/chaos_stress.pid
  fi
  
  # Clean stress processes
  pkill -f "stress --cpu" 2>/dev/null || true
  
  log "Cleanup complete!"
}

# Show help
show_help() {
  cat << EOF
Nightly Chaos Chaos Chaos - Whimsical Chaos Engineering Toolkit

Usage: $0 [OPTIONS]

OPTIONS:
  --mode MODE           Chaos mode: network|service|resource|random|time
  --duration DURATION   Duration for chaos (default: ${DEFAULT_DURATION})
  --service-name NAME   Service to disrupt (for service mode)
  --cpu-cores N         Number of CPU cores to stress (default: ${DEFAULT_CPU_CORES})
  --memory-mb N         Memory to consume in MB (default: ${DEFAULT_MEMORY_MB})
  --latency MS          Network latency in ms (default: 100ms)
  --offset TIME         Time offset (default: +1 hour)
  --cleanup             Clean up all chaos
  --help                Show this help

EXAMPLES:
  $0 --mode network --duration 30s --latency 200ms
  $0 --mode service --service-name nginx
  $0 --mode resource --cpu-cores 2 --memory-mb 512 --duration 60s
  $0 --mode random
  $0 --mode time --offset "+1 hour"
  $0 --cleanup

EOF
}

# Parse arguments
parse_args() {
  local mode=""
  local duration=""
  local service_name=""
  local cpu_cores=""
  local memory_mb=""
  local latency=""
  local offset=""
  local do_cleanup=false
  
  while [[ $# -gt 0 ]]; do
    case $1 in
      --mode)
        mode="$2"
        shift 2
        ;;
      --duration)
        duration="$2"
        shift 2
        ;;
      --service-name)
        service_name="$2"
        shift 2
        ;;
      --cpu-cores)
        cpu_cores="$2"
        shift 2
        ;;
      --memory-mb)
        memory_mb="$2"
        shift 2
        ;;
      --latency)
        latency="$2"
        shift 2
        ;;
      --offset)
        offset="$2"
        shift 2
        ;;
      --cleanup)
        do_cleanup=true
        shift
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
  
  # Execute based on mode
  if [[ "$do_cleanup" == true ]]; then
    cleanup
    exit 0
  fi
  
  if [[ -z "$mode" ]]; then
    error "Mode is required"
    show_help
    exit 1
  fi
  
  check_root
  check_deps
  
  case $mode in
    network)
      chaos_network "${duration:-$DEFAULT_DURATION}" "${latency:-100ms}"
      ;;
    service)
      chaos_service "$service_name"
      ;;
    resource)
      chaos_resource "${cpu_cores:-$DEFAULT_CPU_CORES}" "${memory_mb:-$DEFAULT_MEMORY_MB}" "${duration:-$DEFAULT_DURATION}"
      ;;
    random)
      chaos_random
      ;;
    time)
      chaos_time "${offset:--1 hour}"
      ;;
    *)
      error "Unknown chaos mode: $mode"
      show_help
      exit 1
      ;;
  esac
}

# Main execution
main() {
  parse_args "$@"
}

# Run main if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
