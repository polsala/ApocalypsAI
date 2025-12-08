#!/bin/bash

# Nightly Chaos Chaos Chaos
# A whimsical-yet-useful Bash utility for orchestrating chaos experiments

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORT_DIR="$SCRIPT_DIR/../reports"
LOG_FILE="$REPORT_DIR/chaos.log"

# Ensure report directory exists
mkdir -p "$REPORT_DIR"

# Logging function
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# Cleanup function
cleanup() {
  log "Starting cleanup..."
  
  # Docker cleanup
  if command -v docker &> /dev/null; then
    log "Cleaning up Docker containers..."
    docker ps -aq --filter "label=chaos-experiment" | xargs -r docker stop
    docker ps -aq --filter "label=chaos-experiment" | xargs -r docker rm
  fi
  
  # Kubernetes cleanup
  if command -v kubectl &> /dev/null; then
    log "Cleaning up Kubernetes resources..."
    kubectl delete pods -l chaos-experiment=true --ignore-not-found=true
  fi
  
  log "Cleanup completed."
}

# Network chaos scenario
chaos_network() {
  log "Executing network chaos scenario..."
  
  if command -v tc &> /dev/null; then
    # Add network latency
    sudo tc qdisc add dev lo root netem delay 100ms 50ms distribution normal
    sleep 5
    sudo tc qdisc del dev lo root
    log "Network latency added and removed."
  else
    log "tc not found, skipping network chaos."
  fi
}

# Resource chaos scenario
chaos_resource() {
  log "Executing resource chaos scenario..."
  
  if command -v docker &> /dev/null; then
    # Create a resource-intensive container
    docker run -d --label chaos-experiment=true --name chaos-container alpine sleep 60
    sleep 10
    docker stop chaos-container
    docker rm chaos-container
    log "Resource chaos container created and removed."
  else
    log "Docker not found, skipping resource chaos."
  fi
}

# Service chaos scenario
chaos_service() {
  log "Executing service chaos scenario..."
  
  if command -v systemctl &> /dev/null; then
    # Try to restart a non-critical service (if available)
    if systemctl list-unit-files | grep -q ssh; then
      sudo systemctl restart ssh
      log "SSH service restarted."
    else
      log "SSH service not available, skipping service chaos."
    fi
  else
    log "systemctl not found, skipping service chaos."
  fi
}

# Time chaos scenario
chaos_time() {
  log "Executing time chaos scenario..."
  
  # Manipulate system time (requires root)
  if [[ $EUID -eq 0 ]]; then
    # Save current time
    CURRENT_TIME=$(date)
    # Set time forward by 1 hour
    date -s "+1 hour"
    sleep 2
    # Restore original time
    date -s "$CURRENT_TIME"
    log "System time manipulated and restored."
  else
    log "Root privileges not available, skipping time chaos."
  fi
}

# Kubernetes chaos scenario
chaos_kubernetes() {
  log "Executing Kubernetes chaos scenario..."
  
  if command -v kubectl &> /dev/null; then
    # Create a test pod
    kubectl run chaos-pod --image=alpine --labels=chaos-experiment=true --restart=Never -- sleep 60
    sleep 10
    kubectl delete pod chaos-pod --ignore-not-found=true
    log "Kubernetes chaos pod created and deleted."
  else
    log "kubectl not found, skipping Kubernetes chaos."
  fi
}

# Generate report
generate_report() {
  log "Generating chaos experiment report..."
  
  cat > "$REPORT_DIR/chaos_report.json" << EOF
{
  "timestamp": "$(date -Iseconds)",
  "scenarios": [
    "network",
    "resource",
    "service",
    "time",
    "kubernetes"
  ],
  "status": "completed",
  "log_file": "$LOG_FILE"
}
EOF
  
  log "Report generated at $REPORT_DIR/chaos_report.json"
}

# Main execution
main() {
  log "Starting chaos experiments..."
  
  # Parse arguments
  SCENARIOS="all"
  while [[ $# -gt 0 ]]; do
    case $1 in
      --scenarios)
        SCENARIOS="$2"
        shift 2
        ;;
      --cleanup)
        cleanup
        exit 0
        ;;
      *)
        log "Unknown option: $1"
        exit 1
        ;;
    esac
  done
  
  # Execute scenarios
  if [[ "$SCENARIOS" == "all" ]] || [[ ",${SCENARIOS}," == *,network,* ]]; then
    chaos_network
  fi
  
  if [[ "$SCENARIOS" == "all" ]] || [[ ",${SCENARIOS}," == *,resource,* ]]; then
    chaos_resource
  fi
  
  if [[ "$SCENARIOS" == "all" ]] || [[ ",${SCENARIOS}," == *,service,* ]]; then
    chaos_service
  fi
  
  if [[ "$SCENARIOS" == "all" ]] || [[ ",${SCENARIOS}," == *,time,* ]]; then
    chaos_time
  fi
  
  if [[ "$SCENARIOS" == "all" ]] || [[ ",${SCENARIOS}," == *,kubernetes,* ]]; then
    chaos_kubernetes
  fi
  
  # Generate report
  generate_report
  
  log "Chaos experiments completed successfully!"
}

# Entry point
main "$@"
