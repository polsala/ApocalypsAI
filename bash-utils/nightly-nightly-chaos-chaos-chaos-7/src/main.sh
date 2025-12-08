#!/bin/bash

# Nightly Chaos Chaos Chaos 7
# A whimsical Bash utility for chaos engineering

set -euo pipefail

# Configuration
NETWORK_INTERFACE="eth0"
SERVICE_NAME="ssh"
TIME_OFFSET="-1 hour"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
  echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
  echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
  echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Check if running as root
check_root() {
  if [[ $EUID -ne 0 ]]; then
    error "This script must be run as root for chaos effects."
    exit 1
  fi
}

# Network chaos: latency, packet loss, bandwidth
chaos_network() {
  log "Inducing network chaos..."
  
  # Add latency
  tc qdisc add dev $NETWORK_INTERFACE root netem delay 100ms 2>/dev/null || true
  
  # Add packet loss
  tc qdisc add dev $NETWORK_INTERFACE root netem loss 10% 2>/dev/null || true
  
  # Limit bandwidth
  tc qdisc add dev $NETWORK_INTERFACE root tbf rate 1mbit burst 32kbit latency 400ms 2>/dev/null || true
  
  log "Network chaos induced (latency, loss, bandwidth)."
}

# Resource chaos: CPU and memory stress
chaos_resource() {
  log "Inducing resource chaos..."
  
  # CPU stress
  stress --cpu 4 --timeout 60s &
  
  # Memory stress
  stress --vm 2 --vm-bytes 128M --timeout 60s &
  
  log "Resource chaos induced (CPU and memory stressors started)."
}

# Time chaos: adjust system time
chaos_time() {
  log "Inducing time chaos..."
  
  # Backup current time
  CURRENT_TIME=$(date '+%Y-%m-%d %H:%M:%S')
  echo "$CURRENT_TIME" > /tmp/chaos_time_backup
  
  # Adjust time
  date -s "$TIME_OFFSET"
  
  log "Time chaos induced (system time adjusted)."
}

# Service chaos: stop and start services
chaos_service() {
  log "Inducing service chaos..."
  
  # Stop service
  systemctl stop $SERVICE_NAME 2>/dev/null || true
  
  # Start service after delay
  (sleep 10 && systemctl start $SERVICE_NAME 2>/dev/null || true) &
  
  log "Service chaos induced (service stopped and scheduled to restart)."
}

# Cleanup: remove all chaos effects
cleanup() {
  log "Cleaning up chaos..."
  
  # Remove network chaos
  tc qdisc del dev $NETWORK_INTERFACE root 2>/dev/null || true
  
  # Restore time if backup exists
  if [[ -f /tmp/chaos_time_backup ]]; then
    RESTORE_TIME=$(cat /tmp/chaos_time_backup)
    date -s "$RESTORE_TIME"
    rm -f /tmp/chaos_time_backup
    log "Time restored from backup."
  fi
  
  # Ensure service is running
  systemctl start $SERVICE_NAME 2>/dev/null || true
  
  # Kill any stress processes
  pkill -f stress || true
  
  log "Chaos cleanup complete."
}

# Show help
show_help() {
  cat << EOF
Usage: $0 [OPTIONS]

Options:
  --scenario SCENARIO  Run a specific chaos scenario (network|resource|time|service)
  --cleanup            Remove all chaos effects
  --help               Show this help message

Examples:
  $0 --scenario network
  $0 --scenario resource
  $0 --cleanup

EOF
}

# Main execution
main() {
  local scenario=""
  
  # Parse arguments
  while [[ $# -gt 0 ]]; do
    case $1 in
      --scenario)
        scenario="$2"
        shift 2
        ;;
      --cleanup)
        cleanup
        exit 0
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
  
  # Check root for chaos scenarios
  if [[ -n "$scenario" ]]; then
    check_root
  fi
  
  case "$scenario" in
    network)
      chaos_network
      ;;
    resource)
      chaos_resource
      ;;
    time)
      chaos_time
      ;;
    service)
      chaos_service
      ;;
    "")
      error "No scenario specified. Use --help for usage."
      exit 1
      ;;
    *)
      error "Unknown scenario: $scenario. Use --help for valid scenarios."
      exit 1
      ;;
  esac
}

# Run main if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
