#!/usr/bin/env bash
set -euo pipefail

# Configuration
SERVICES=("ssh" "nginx" "apache2" "docker" "redis-server")
LOG_FILE="chaos_log.txt"
MAX_DELAY_MS=200
MAX_LOSS_PERCENT=10
MAX_CPU_CORES=2
MAX_CPU_SECONDS=30

# Helpers
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

random_choice() {
  local arr=($@)
  echo "${arr[$((RANDOM % ${#arr[@]}))]}"
}

# Chaos actions
chaos_kill_service() {
  local svc="$1"
  log "CHAOS: Attempting to kill service $svc"
  if systemctl is-active --quiet "$svc" 2>/dev/null; then
    log "CHAOS: Killing $svc"
    if $EXECUTE; then
      sudo systemctl stop "$svc" || log "CHAOS: Failed to stop $svc"
    else
      log "CHAOS: Dry-run: would stop $svc"
    fi
  else
    log "CHAOS: $svc not running, skipping"
  fi
}

chaos_restart_service() {
  local svc="$1"
  log "CHAOS: Attempting to restart service $svc"
  if $EXECUTE; then
    sudo systemctl restart "$svc" || log "CHAOS: Failed to restart $svc"
  else
    log "CHAOS: Dry-run: would restart $svc"
  fi
}

chaos_network_latency() {
  local dev="$(ip route | grep default | awk '{print $5}' | head -n1)"
  local delay=$((RANDOM % MAX_DELAY_MS + 1))
  log "CHAOS: Adding network latency $delay ms on $dev"
  if $EXECUTE; then
    sudo tc qdisc add dev "$dev" root netem delay ${delay}ms 2>/dev/null || sudo tc qdisc change dev "$dev" root netem delay ${delay}ms
  else
    log "CHAOS: Dry-run: would add latency $delay ms on $dev"
  fi
}

chaos_network_loss() {
  local dev="$(ip route | grep default | awk '{print $5}' | head -n1)"
  local loss=$((RANDOM % MAX_LOSS_PERCENT + 1))
  log "CHAOS: Adding network packet loss $loss% on $dev"
  if $EXECUTE; then
    sudo tc qdisc add dev "$dev" root netem loss ${loss}% 2>/dev/null || sudo tc qdisc change dev "$dev" root netem loss ${loss}%
  else
    log "CHAOS: Dry-run: would add loss $loss% on $dev"
  fi
}

chaos_cpu_load() {
  local cores=$((RANDOM % MAX_CPU_CORES + 1))
  local seconds=$((RANDOM % MAX_CPU_SECONDS + 5))
  log "CHAOS: Spiking CPU load for $cores cores for $seconds seconds"
  if $EXECUTE; then
    timeout "$seconds"s stress --cpu "$cores" || log "CHAOS: CPU stress completed or failed"
  else
    log "CHAOS: Dry-run: would spike CPU for $cores cores for $seconds seconds"
  fi
}

chaos_execute() {
  local action=$(random_choice "kill" "restart" "latency" "loss" "cpu")
  case "$action" in
    kill)
      local svc=$(random_choice "${SERVICES[@]}")
      chaos_kill_service "$svc"
      ;;
    restart)
      local svc=$(random_choice "${SERVICES[@]}")
      chaos_restart_service "$svc"
      ;;
    latency)
      chaos_network_latency
      ;;
    loss)
      chaos_network_loss
      ;;
    cpu)
      chaos_cpu_load
      ;;
  esac
}

chaos_reset() {
  log "CHAOS: Resetting network and CPU state"
  if $EXECUTE; then
    sudo tc qdisc del dev "$(ip route | grep default | awk '{print $5}' | head -n1)" root 2>/dev/null || true
    pkill -f stress || true
  else
    log "CHAOS: Dry-run: would reset network and CPU"
  fi
}

# CLI
EXECUTE=false
SHOW_LOG=false
RESET=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --execute)
      EXECUTE=true
      shift
      ;;
    --dry-run)
      EXECUTE=false
      shift
      ;;
    --log)
      SHOW_LOG=true
      shift
      ;;
    --reset)
      RESET=true
      shift
      ;;
    *)
      echo "Usage: $0 [--execute|--dry-run] [--log] [--reset]"
      exit 1
      ;;
  esac
done

if $RESET; then
  chaos_reset
  exit 0
fi

if $SHOW_LOG; then
  if [[ -f "$LOG_FILE" ]]; then
    cat "$LOG_FILE"
  else
    echo "No log file found. Run chaos first."
  fi
  exit 0
fi

log "CHAOS: Starting chaos run (execute=$EXECUTE)"
chaos_execute
log "CHAOS: Chaos run complete"
