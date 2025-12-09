#!/bin/bash

# Nightly Chaos Chaos Chaos 3
# A whimsical chaos generator for testing resilience

set -euo pipefail

# Configuration
CHAOS_DURATION=60
REPORT_FILE="/tmp/chaos_report_$(date +%s).txt"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
  echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
  echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

error() {
  echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

# Initialize report
init_report() {
  echo "Chaos Report - $(date)" > "$REPORT_FILE"
  echo "========================" >> "$REPORT_FILE"
}

# Add entry to report
add_to_report() {
  echo "- $1" >> "$REPORT_FILE"
}

# Check if command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Chaos function: Network disruption
chaos_network() {
  log "Initiating network chaos..."
  
  if command_exists tc; then
    # Add random latency and packet loss
    LATENCY=$((RANDOM % 200 + 50))
    PACKET_LOSS=$((RANDOM % 10 + 1))
    
    warn "Adding ${LATENCY}ms latency and ${PACKET_LOSS}% packet loss"
    sudo tc qdisc add dev lo root netem delay ${LATENCY}ms loss ${PACKET_LOSS}% 2>/dev/null || true
    add_to_report "Network: Added ${LATENCY}ms latency and ${PACKET_LOSS}% packet loss"
    
    # Schedule cleanup
    (sleep $CHAOS_DURATION && sudo tc qdisc del dev lo root 2>/dev/null || true) &
  else
    warn "tc not found, skipping network chaos"
    add_to_report "Network: tc not found, skipping"
  fi
}

# Chaos function: Resource stress
chaos_resources() {
  log "Initiating resource chaos..."
  
  if command_exists stress; then
    # Stress CPU and memory
    CPU_LOAD=$((RANDOM % 4 + 1))
    MEMORY_GB=$((RANDOM % 2 + 1))
    
    warn "Stressing ${CPU_LOAD} CPU cores and ${MEMORY_GB}GB memory for ${CHAOS_DURATION}s"
    stress --cpu $CPU_LOAD --vm $MEMORY_GB --timeout ${CHAOS_DURATION}s &
    add_to_report "Resources: Stressed ${CPU_LOAD} CPU cores and ${MEMORY_GB}GB memory"
  else
    warn "stress not found, skipping resource chaos"
    add_to_report "Resources: stress not found, skipping"
  fi
}

# Chaos function: Service disruption
chaos_services() {
  log "Initiating service chaos..."
  
  if command_exists systemctl; then
    # Get a list of active services
    SERVICES=$(systemctl list-units --type=service --state=active --no-pager --no-legend | head -5 | awk '{print $1}')
    
    for service in $SERVICES; do
      if [ $((RANDOM % 2)) -eq 0 ]; then
        warn "Stopping service: $service"
        sudo systemctl stop "$service" 2>/dev/null || true
        add_to_report "Service: Stopped $service"
        
        # Schedule restart
        (sleep $((CHAOS_DURATION / 2)) && sudo systemctl start "$service" 2>/dev/null || true) &
      fi
    done
  else
    warn "systemctl not found, skipping service chaos"
    add_to_report "Service: systemctl not found, skipping"
  fi
}

# Chaos function: Random file operations
chaos_files() {
  log "Initiating file chaos..."
  
  # Create temporary files in /tmp
  TEMP_FILES=3
  for i in $(seq 1 $TEMP_FILES); do
    FILE_PATH="/tmp/chaos_temp_$i"
    FILE_SIZE=$((RANDOM % 1024 + 100))
    
    warn "Creating temporary file: $FILE_PATH (${FILE_SIZE}KB)"
    dd if=/dev/zero of="$FILE_PATH" bs=1024 count=$FILE_SIZE 2>/dev/null || true
    add_to_report "Files: Created $FILE_PATH (${FILE_SIZE}KB)"
  done
  
  # Schedule cleanup
  (sleep $CHAOS_DURATION && rm -f /tmp/chaos_temp_* 2>/dev/null || true) &
}

# Main chaos execution
execute_chaos() {
  log "Starting chaos execution for ${CHAOS_DURATION} seconds..."
  
  # Randomly select chaos functions to execute
  CHAOS_FUNCTIONS=(chaos_network chaosos_resources chaos_services chaos_files)
  
  # Execute 2-3 random chaos functions
  NUM_FUNCTIONS=$((RANDOM % 2 + 2))
  
  for i in $(seq 1 $NUM_FUNCTIONS); do
    FUNC_INDEX=$((RANDOM % ${#CHAOS_FUNCTIONS[@]}))
    ${CHAOS_FUNCTIONS[$FUNC_INDEX]} &
  done
  
  # Wait for chaos duration
  sleep $CHAOS_DURATION
  
  log "Chaos execution completed!"
}

# Display final report
show_report() {
  log "Generating chaos report..."
  echo ""
  echo "Chaos Report:" | tee -a "$REPORT_FILE"
  cat "$REPORT_FILE" | tail -n +3
  echo ""
  echo "Report saved to: $REPORT_FILE"
}

# Cleanup function
cleanup() {
  log "Performing cleanup..."
  
  # Remove any remaining tc rules
  sudo tc qdisc del dev lo root 2>/dev/null || true
  
  # Kill any remaining stress processes
  pkill -f stress 2>/dev/null || true
  
  # Remove temporary files
  rm -f /tmp/chaos_temp_* 2>/dev/null || true
  
  log "Cleanup completed!"
}

# Main execution
main() {
  log "Nightly Chaos Chaos Chaos 3 - Starting chaos simulation"
  
  # Check if running as root for some operations
  if [[ $EUID -eq 0 ]]; then
    warn "Running as root - full chaos capabilities enabled"
  else
    warn "Not running as root - some chaos operations may be limited"
  fi
  
  init_report
  execute_chaos
  cleanup
  show_report
}

# Trap cleanup on exit
trap cleanup EXIT

# Run main function
main
