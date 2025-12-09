#!/bin/bash

# Nightly Bash Chaos Chaos Chaos 2
# A whimsical chaos generator for testing system resilience

set -euo pipefail

# Configuration
CHAOS_LEVEL=${1:-1}
LOG_FILE="/tmp/chaos_report_$(date +%s).log"

# Functions
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

chaos_cpu() {
  log "CHAOS: Spiking CPU usage"
  timeout 10s yes > /dev/null &
  timeout 10s yes > /dev/null &
  timeout 10s yes > /dev/null &
  wait
  log "CHAOS: CPU spike complete"
}

chaos_memory() {
  log "CHAOS: Consuming memory"
  # Allocate memory in a controlled way
  dd if=/dev/zero of=/tmp/chaos_memory bs=1M count=100 2>/dev/null || true
  rm -f /tmp/chaos_memory
  log "CHAOS: Memory consumption complete"
}

chaos_network() {
  log "CHAOS: Disrupting network"
  # Add network delay
  tc qdisc add dev lo root netem delay 100ms 2>/dev/null || true
  sleep 2
  tc qdisc del dev lo root 2>/dev/null || true
  log "CHAOS: Network disruption complete"
}

chaos_time() {
  log "CHAOS: Distorting time"
  # Just log a time distortion message
  log "CHAOS: Time distortion detected - this is just for fun!"
}

chaos_random() {
  log "CHAOS: Random chaos event"
  case $((RANDOM % 4)) in
    0) chaos_cpu ;;
    1) chaos_memory ;;
    2) chaos_network ;;
    3) chaos_time ;;
  esac
}

# Main execution
log "Starting chaos level $CHAOS_LEVEL"

for i in $(seq 1 $CHAOS_LEVEL); do
  log "CHAOS: Executing chaos event $i"
  chaos_random
  sleep 1
done

log "Chaos execution complete. Report saved to $LOG_FILE"
echo "Chaos report:"
cat "$LOG_FILE"
