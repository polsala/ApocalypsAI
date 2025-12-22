#!/usr/bin/env bash
# nightly-ssh-tunnel-elf – persistent SSH tunnel helper with ASCII elf status

# Default SSH command – can be overridden for testing
: "${SSH_TUNNEL_ELF_SSH_CMD:=ssh}"

LOCK_FILE="/tmp/ssh-tunnel-elf.lock"
PID_FILE="/tmp/ssh-tunnel-elf.pid"

print_elf() {
  cat <<'EOF'
      /\
     /  \
    /____\
   (|    |)
    |____|
    /____\
   (______)  
   /      \
  /        \
EOF
}

is_running() {
  if [[ -f "$PID_FILE" ]]; then
    local pid
    pid=$(cat "$PID_FILE")
    if kill -0 "$pid" 2>/dev/null; then
      return 0
    else
      rm -f "$PID_FILE" "$LOCK_FILE"
      return 1
    fi
  else
    return 1
  fi
}

start_tunnel() {
  if [[ $# -ne 2 ]]; then
    echo "Usage: $0 start <user@host> <local_port>"
    return 1
  fi
  local target="$1"
  local local_port="$2"

  if is_running; then
    echo "Tunnel already running (PID $(cat $PID_FILE))."
    return 0
  fi

  # Ensure lock file to avoid race conditions
  exec 200>"$LOCK_FILE" || { echo "Cannot create lock file"; return 1; }
  flock -n 200 || { echo "Another instance is starting the tunnel"; return 1; }

  # Start SSH tunnel in background
  "$SSH_TUNNEL_ELF_SSH_CMD" -N -D "${local_port}" "$target" &
  local pid=$!
  echo "$pid" > "$PID_FILE"
  echo "Tunnel started (PID $pid) to $target on local port $local_port."
  return 0
}

stop_tunnel() {
  if ! is_running; then
    echo "No active tunnel to stop."
    return 0
  fi
  local pid
  pid=$(cat "$PID_FILE")
  kill "$pid" && rm -f "$PID_FILE" "$LOCK_FILE"
  echo "Tunnel (PID $pid) stopped."
}

status_tunnel() {
  if is_running; then
    echo "Tunnel is active (PID $(cat $PID_FILE))."
  else
    echo "No active tunnel."
  fi
  print_elf
}

# Main entry point
cmd="$1"
shift || true
case "$cmd" in
  start)
    start_tunnel "$@"
    ;;
  stop)
    stop_tunnel
    ;;
  status)
    status_tunnel
    ;;
  *)
    echo "Usage: $0 {start|stop|status}"
    exit 1
    ;;
esac
