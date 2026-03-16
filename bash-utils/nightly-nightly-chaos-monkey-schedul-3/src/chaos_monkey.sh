#!/bin/bash

set -euo pipefail

CHAOS_PID_FILE="/tmp/chaos_monkey.pid"
DEFAULT_INTERVAL="30s"
DRY_RUN=false
ACTION=""

log() { echo "[CHAOS MONKEY] $*"; }

show_help() {
cat << EOF
Usage: $0 [start|stop] [--interval=DURATION] [--dry-run]

Schedule random chaos events to test system resilience.

Arguments:
  start         Start scheduling chaos events
  stop          Stop all scheduled chaos events

Options:
  --interval=DURATION   Time between disruptions (e.g., 10s, 1m). Default: 30s
  --dry-run             Preview disruptions without applying them
  --help                Display this help and exit
EOF
}

parse_args() {
  for arg in "$@"; do
    case "$arg" in
      start|stop) ACTION="$arg" ;;
      --interval=*) INTERVAL="${arg#*=}" ;;
      --dry-run) DRY_RUN=true ;;
      --help|-h) show_help; exit 0 ;;
      *) log "Unknown argument: $arg"; show_help; exit 1 ;;
    esac
  done
}

disrupt_service() {
  local services=("nginx" "apache2" "docker")
  local svc=${services[RANDOM % ${#services[@]}]}
  if [[ "$DRY_RUN" == true ]]; then
    log "[DRY RUN] Would restart service: $svc"
  else
    log "Restarting service: $svc"
    if command -v systemctl >/dev/null; then
      sudo systemctl restart "$svc" || true
    fi
  fi
}

disrupt_network() {
  if [[ "$DRY_RUN" == true ]]; then
    log "[DRY RUN] Would add temporary network latency"
  else
    log "Adding temporary network latency"
    if command -v tc >/dev/null; then
      sudo tc qdisc add dev lo root netem delay 100ms 10ms 25% || true
      sleep 2
      sudo tc qdisc del dev lo root || true
    fi
  fi
}

disrupt_disk_io() {
  if [[ "$DRY_RUN" == true ]]; then
    log "[DRY RUN] Would simulate high disk I/O"
  else
    log "Simulating high disk I/O"
    dd if=/dev/zero of=/tmp/chaos.tmp bs=1M count=100 oflag=direct 2>/dev/null || true
    rm -f /tmp/chaos.tmp
  fi
}

run_chaos_loop() {
  log "Starting Chaos Monkey with interval: $INTERVAL"
  while true; do
    local disruptions=(disrupt_service disrupt_network disrupt_disk_io)
    local func=${disruptions[RANDOM % ${#disruptions[@]}]}
    "$func"
    sleep "$(echo "$INTERVAL" | sed 's/s$//' | sed 's/m$/ * 60 /' | bc)"
  done
}

start_chaos() {
  if [[ -f "$CHAOS_PID_FILE" ]]; then
    log "Chaos Monkey already running. PID: $(cat $CHAOS_PID_FILE)"
    return 1
  fi
  run_chaos_loop &
  echo $! > "$CHAOS_PID_FILE"
  log "Started Chaos Monkey. PID: $(cat $CHAOS_PID_FILE)"
}

stop_chaos() {
  if [[ ! -f "$CHAOS_PID_FILE" ]]; then
    log "No Chaos Monkey instance found."
    return 1
  fi
  local pid=$(cat "$CHAOS_PID_FILE")
  kill "$pid" 2>/dev/null || true
  rm -f "$CHAOS_PID_FILE"
  log "Stopped Chaos Monkey (PID: $pid)."
}

main() {
  parse_args "$@"
  if [[ -z "$ACTION" ]]; then
    log "Error: Action required (start or stop)."
    show_help
    exit 1
  fi

  case "$ACTION" in
    start)
      start_chaos
      ;;
    stop)
      stop_chaos
      ;;
  esac
}

main "$@"
