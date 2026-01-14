#!/bin/bash

# nightly-chaos-monkey-scheduler
# Introduces controlled chaos to test system resilience

set -euo pipefail

# Configuration with defaults
CHAOS_PROBABILITY=${CHAOS_PROBABILITY:-10}  # 10% chance of chaos by default
DRY_RUN=${DRY_RUN:-0}
LOG_FILE=${LOG_FILE:-"/var/log/chaos-monkey.log"}

# Log function
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check if we should cause chaos
should_cause_chaos() {
  local random_value=$((RANDOM % 100 + 1))
  if [[ $random_value -le $CHAOS_PROBABILITY ]]; then
    return 0
  else
    return 1
  fi
}

# CPU stress
cause_cpu_stress() {
  local duration=$((RANDOM % 30 + 5))  # 5-35 seconds
  log "Causing CPU stress for ${duration}s"
  if [[ $DRY_RUN -eq 0 ]]; then
    timeout $duration stress-ng --cpu 4 --timeout ${duration}s >/dev/null 2>&1 &
  fi
}

# Network interface chaos
cause_network_chaos() {
  local interfaces=$(ip -o link show | awk -F': ' '{print $2}' | grep -v lo)
  if [[ -z "$interfaces" ]]; then
    log "No network interfaces found for chaos"
    return
  fi
  
  local interface=$(echo "$interfaces" | shuf | head -n1)
  local down_time=$((RANDOM % 10 + 2))  # 2-12 seconds
  
  log "Taking down network interface $interface for ${down_time}s"
  if [[ $DRY_RUN -eq 0 ]]; then
    ip link set "$interface" down
    sleep "$down_time"
    ip link set "$interface" up
  fi
}

# Service restart chaos
cause_service_chaos() {
  local services=$(systemctl list-units --type=service --state=running | awk 'NR>1 {print $1}' | grep -vE "(systemd|dbus|ssh|network)" | shuf | head -n3)
  if [[ -z "$services" ]]; then
    log "No suitable services found for chaos"
    return
  fi
  
  local service=$(echo "$services" | shuf | head -n1)
  log "Restarting service: $service"
  if [[ $DRY_RUN -eq 0 ]]; then
    systemctl restart "$service" 2>/dev/null || log "Failed to restart $service"
  fi
}

# Memory stress
cause_memory_stress() {
  local duration=$((RANDOM % 20 + 5))  # 5-25 seconds
  log "Causing memory stress for ${duration}s"
  if [[ $DRY_RUN -eq 0 ]]; then
    timeout $duration stress-ng --vm 1 --vm-bytes 512M --timeout ${duration}s >/dev/null 2>&1 &
  fi
}

# Disk I/O stress
cause_disk_stress() {
  local duration=$((RANDOM % 25 + 5))  # 5-30 seconds
  log "Causing disk I/O stress for ${duration}s"
  if [[ $DRY_RUN -eq 0 ]]; then
    timeout $duration stress-ng --hdd 2 --hdd-bytes 1G --timeout ${duration}s >/dev/null 2>&1 &
  fi
}

# Main execution
main() {
  log "Chaos Monkey started (Probability: ${CHAOS_PROBABILITY}%)"
  
  if should_cause_chaos; then
    local chaos_type=$((RANDOM % 5))
    case $chaos_type in
      0) cause_cpu_stress ;;
      1) cause_network_chaos ;;
      2) cause_service_chaos ;;
      3) cause_memory_stress ;;
      4) cause_disk_stress ;;
    esac
  else
    log "No chaos today - system is safe"
  fi
  
  log "Chaos Monkey finished"
}

# Run main function
main
