#!/usr/bin/env bash
# Nightly Ephemeral GitHub Runner
# Spin up, monitor, and clean up short-lived self-hosted runners.
# Usage: ./src/ephemeral_runner.sh [options]

set -euo pipefail
IFS=$'\n\t'

# Configuration
RUNNER_VERSION="2.320.2"
RUNNER_OS="linux"
RUNNER_ARCH="x64"
if [[ "$(uname -s)" == "Darwin" ]]; then
  RUNNER_OS="osx"
  case "$(uname -m)" in
    arm64) RUNNER_ARCH="arm64" ;;
    *) RUNNER_ARCH="x64" ;;
  esac
fi
RUNNER_BASE_URL="https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}"
RUNNER_TAR="actions-runner-${RUNNER_OS}-${RUNNER_ARCH}-${RUNNER_VERSION}.tar.gz"
RUNNER_URL="${RUNNER_BASE_URL}/${RUNNER_TAR}"
RUNNER_CACHE_DIR="./cache/runner"
RUNNER_LOGS_DIR="./logs"
RUNNER_STATE_FILE="./runners/state.json"
DEFAULT_TIMEOUT=3600

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
  echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $*"
}
warn() {
  echo -e "${YELLOW}[WARN]${NC} $*" >&2
}
err() {
  echo -e "${RED}[ERROR]${NC} $*" >&2
  exit 1
}

usage() {
  cat <<EOF
Usage: $0 [options]

Options:
  --repo <url>          Repository URL (required unless --org)
  --org <url>           Organization URL (required unless --repo)
  --token <token>       GitHub PAT with repo or admin:org scope (required)
  --labels <csv>        Comma-separated labels (optional)
  --runner-dir <path>   Directory to install runner (default: ./runners/<name>)
  --timeout <seconds>   Runner idle timeout (default: ${DEFAULT_TIMEOUT})
  --status              Show status of active runners
  --cleanup             Stop and remove orphaned runners
  --help                Show this help

Examples:
  $0 --repo https://github.com/owner/repo --token YOUR_TOKEN --labels test,ephemeral
  $0 --org https://github.com/owner --token YOUR_TOKEN --labels test,ephemeral
  $0 --status
  $0 --cleanup
EOF
}

# Parse arguments
REPO_URL=""
ORG_URL=""
TOKEN=""
LABELS=""
RUNNER_DIR=""
TIMEOUT="${DEFAULT_TIMEOUT}"
SHOW_STATUS=false
DO_CLEANUP=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --repo)
      REPO_URL="$2"
      shift 2
      ;;
    --org)
      ORG_URL="$2"
      shift 2
      ;;
    --token)
      TOKEN="$2"
      shift 2
      ;;
    --labels)
      LABELS="$2"
      shift 2
      ;;
    --runner-dir)
      RUNNER_DIR="$2"
      shift 2
      ;;
    --timeout)
      TIMEOUT="$2"
      shift 2
      ;;
    --status)
      SHOW_STATUS=true
      shift
      ;;
    --cleanup)
      DO_CLEANUP=true
      shift
      ;;
    --help)
      usage
      exit 0
      ;;
    *)
      err "Unknown option: $1"
      ;;
  esac
done

if $SHOW_STATUS; then
  show_status
  exit 0
fi

if $DO_CLEANUP; then
  cleanup_orphans
  exit 0
fi

if [[ -z "$TOKEN" ]]; then
  err "--token is required."
fi

if [[ -z "$REPO_URL" && -z "$ORG_URL" ]]; then
  err "Either --repo or --org is required."
fi

if [[ -n "$REPO_URL" && -n "$ORG_URL" ]]; then
  err "Specify only one of --repo or --org."
fi

# Derived values
if [[ -n "$REPO_URL" ]]; then
  TARGET_URL="$REPO_URL"
  TARGET_TYPE="repo"
else
  TARGET_URL="$ORG_URL"
  TARGET_TYPE="org"
fi

RUNNER_NAME="ephemeral-$(date +%s)-$$"
if [[ -z "$RUNNER_DIR" ]]; then
  RUNNER_DIR="./runners/${RUNNER_NAME}"
fi

# Ensure directories
mkdir -p "$RUNNER_CACHE_DIR" "$RUNNER_LOGS_DIR" "$(dirname "$RUNNER_DIR")"

# State management
state_add() {
  local name="$1"
  local dir="$2"
  local pid="$3"
  local target_url="$4"
  local target_type="$5"
  local labels="$6"
  local ts="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
  local entry="{\"name\": \"$name\", \"dir\": \"$dir\", \"pid\": \"$pid\", \"target_url\": \"$target_url\", \"target_type\": \"$target_type\", \"labels\": \"$labels\", \"created\": \"$ts\"}"
  if [[ -f "$RUNNER_STATE_FILE" ]]; then
    jq --argjson entry "$entry" '.runners += [$entry]' "$RUNNER_STATE_FILE" > /tmp/state.tmp && mv /tmp/state.tmp "$RUNNER_STATE_FILE"
  else
    echo '{"runners": []}' | jq --argjson entry "$entry" '.runners += [$entry]' > "$RUNNER_STATE_FILE"
  fi
}

state_remove() {
  local name="$1"
  if [[ -f "$RUNNER_STATE_FILE" ]]; then
    jq 'del(.runners[] | select(.name == env.name))' "$RUNNER_STATE_FILE" > /tmp/state.tmp && mv /tmp/state.tmp "$RUNNER_STATE_FILE"
  fi
}

state_list() {
  if [[ -f "$RUNNER_STATE_FILE" ]]; then
    jq -r '.runners[] | [.name, .dir, .pid, .target_url, .target_type, .labels, .created] | @tsv' "$RUNNER_STATE_FILE" 2>/dev/null || true
  fi
}

# Cleanup on exit
cleanup_runner() {
  local name="$1"
  local dir="$2"
  local pid="$3"
  log "Cleaning up runner $name (pid $pid)"
  if kill -0 "$pid" 2>/dev/null; then
    kill "$pid" || true
  fi
  if [[ -d "$dir" ]]; then
    # Stop service if installed
    if [[ -f "$dir/runsvc.sh" ]]; then
      "$dir/runsvc.sh" stop || true
    fi
    # Remove runner from target
    if command -v jq >/dev/null 2>&1; then
      local target_url target_type
      read -r _ _ _ target_url target_type _ _ < <(state_list | grep -F "${name}" | head -n1 || true)
      if [[ -n "$target_url" && -n "$target_type" ]]; then
        remove_runner_from_target "$target_url" "$target_type" "$TOKEN" "$name"
      fi
    fi
    rm -rf "$dir"
  fi
  state_remove "$name"
}

trap_exit() {
  # Best-effort cleanup
  for line in $(state_list); do
    set -- $line
    local name="$1" dir="$2" pid="$3"
    cleanup_runner "$name" "$dir" "$pid"
  done
}
trap trap_exit EXIT

# Download runner binary (cached)
download_runner() {
  local cache_file="$RUNNER_CACHE_DIR/${RUNNER_TAR}"
  if [[ ! -f "$cache_file" ]]; then
    log "Downloading runner ${RUNNER_VERSION} for ${RUNNER_OS}-${RUNNER_ARCH}"
    curl -fsSL "$RUNNER_URL" -o "$cache_file" || err "Failed to download runner."
  else
    log "Using cached runner ${RUNNER_VERSION}"
  fi
  tar -xzf "$cache_file" -C "$RUNNER_DIR" --strip-components=1
}

# Configure runner
configure_runner() {
  local dir="$1"
  local name="$2"
  local token="$3"
  local target_url="$4"
  local target_type="$5"
  local labels="$6"
  log "Configuring runner $name"
  cd "$dir"
  # Configure without interactive prompts
  ./config.sh \
    --unattended \
    --url "$target_url" \
    --token "$token" \
    --name "$name" \
    --labels "$labels" \
    --replace \
    --runnergroup "Default" \
    --ephemeral || err "Failed to configure runner."
}

# Start runner (background)
start_runner() {
  local dir="$1"
  local log_file="$2"
  log "Starting runner"
  ./run.sh >"$log_file" 2>&1 &
  echo $!
}

# Remove runner from target (repo or org)
remove_runner_from_target() {
  local target_url="$1"
  local target_type="$2"
  local token="$3"
  local name="$4"
  log "Removing runner $name from $target_type"
  local api_url=""
  if [[ "$target_type" == "repo" ]]; then
    api_url="${target_url}/actions/runners/registration-token"
  else
    api_url="${target_url}/actions/runners/remove-token"
  fi
  # Get remove token
  local remove_token=""
  if command -v jq >/dev/null 2>&1; then
    remove_token=$(curl -fsSL -X POST -H "Authorization: token $token" -H "Accept: application/vnd.github.v3+json" "${api_url%registration-token}remove-token" | jq -r .token)
  else
    remove_token=$(curl -fsSL -X POST -H "Authorization: token $token" -H "Accept: application/vnd.github.v3+json" "${api_url%registration-token}remove-token" | grep -o '"token":"[^"]*' | cut -d: -f2- | tr -d '"')
  fi
  if [[ -z "$remove_token" ]]; then
    warn "Could not retrieve remove token; skipping removal."
    return 0
  fi
  # Remove runner
  curl -fsSL -X DELETE -H "Authorization: token $token" -H "Accept: application/vnd.github.v3+json" \
    -d "{\"runner_ids\":[\"$name\"], \"token\": \"$remove_token\"}" \
    "${api_url%registration-token}runners"
}

# Show status
show_status() {
  log "Active runners:"
  if [[ ! -f "$RUNNER_STATE_FILE" ]]; then
    log "No active runners."
    return 0
  fi
  while IFS=$'\t' read -r name dir pid target_url target_type labels created; do
    if kill -0 "$pid" 2>/dev/null; then
      echo "  Name: $name"
      echo "  Dir: $dir"
      echo "  PID: $pid"
      echo "  Target: $target_url ($target_type)"
      echo "  Labels: $labels"
      echo "  Created: $created"
      echo ""
    else
      warn "Runner $name (pid $pid) is not running; cleaning up."
      cleanup_runner "$name" "$dir" "$pid"
    fi
  done < <(state_list)
}

# Cleanup orphaned runners (by PID check)
cleanup_orphans() {
  log "Cleaning up orphaned runners..."
  while IFS=$'\t' read -r name dir pid target_url target_type labels created; do
    if ! kill -0 "$pid" 2>/dev/null; then
      warn "Orphaned runner $name (pid $pid); removing."
      cleanup_runner "$name" "$dir" "$pid"
    fi
  done < <(state_list)
  log "Cleanup complete."
}

# Main flow
main() {
  log "Spinning up ephemeral runner $RUNNER_NAME"
  mkdir -p "$RUNNER_DIR"
  download_runner
  configure_runner "$RUNNER_DIR" "$RUNNER_NAME" "$TOKEN" "$TARGET_URL" "$TARGET_TYPE" "$LABELS"
  local log_file="$RUNNER_LOGS_DIR/${RUNNER_NAME}.log"
  local pid=$(start_runner "$RUNNER_DIR" "$log_file")
  state_add "$RUNNER_NAME" "$RUNNER_DIR" "$pid" "$TARGET_URL" "$TARGET_TYPE" "$LABELS"
  log "Runner $RUNNER_NAME started (pid $pid, log $log_file)"
  # Wait with timeout
  local elapsed=0
  while kill -0 "$pid" 2>/dev/null; do
    sleep 5
    elapsed=$((elapsed + 5))
    if [[ $elapsed -ge $TIMEOUT ]]; then
      warn "Timeout reached ($TIMEOUT s); stopping runner."
      cleanup_runner "$RUNNER_NAME" "$RUNNER_DIR" "$pid"
      break
    fi
  done
  log "Runner $RUNNER_NAME stopped."
}

main
