#!/usr/bin/env bash
# Tests for Nightly Ephemeral GitHub Runner
# Mock rationale: Avoid real GitHub API calls and runner binaries.

set -euo pipefail
IFS=$'\n\t'

# Test helpers
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*" >&2; }
err() { echo -e "${RED}[ERROR]${NC} $*" >&2; exit 1; }

# Mock functions
mock_curl() {
  case "$1" in
    *registration-token*)
      echo '{"token":"mock-registration-token"}'
      ;;
    *remove-token*)
      echo '{"token":"mock-remove-token"}'
      ;;
    *runners*)
      echo '{}'
      ;;
    *)
      echo '{}'
      ;;
  esac
}

mock_jq() {
  case "$1" in
    -r)
      echo "mock-token"
      ;;
    *)
      echo '{}'
      ;;
  esac
}

# Setup test environment
TEST_DIR="$(mktemp -d)"
export RUNNER_CACHE_DIR="$TEST_DIR/cache/runner"
export RUNNER_LOGS_DIR="$TEST_DIR/logs"
export RUNNER_STATE_FILE="$TEST_DIR/state.json"
export PATH="$TEST_DIR/bin:$PATH"

mkdir -p "$RUNNER_CACHE_DIR" "$RUNNER_LOGS_DIR" "$TEST_DIR/bin"

# Mock binaries
mock_binary() {
  cat > "$TEST_DIR/bin/$1" <<'EOF'
#!/usr/bin/env bash
# Mock binary
exit 0
EOF
  chmod +x "$TEST_DIR/bin/$1"
}

mock_binary curl
mock_binary jq
mock_binary tar

# Mock runner files
mkdir -p "$TEST_DIR/runners/test-runner"
cat > "$TEST_DIR/runners/test-runner/config.sh" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
cat > "$TEST_DIR/runners/test-runner/run.sh" <<'EOF'
#!/usr/bin/env bash
sleep 1
exit 0
EOF
chmod +x "$TEST_DIR/runners/test-runner/config.sh"
chmod +x "$TEST_DIR/runners/test-runner/run.sh"

cat > "$TEST_DIR/runners/test-runner/actions-runner.tar.gz" <<'EOF'
# Mock tarball
EOF

# Source the script (with mocks)
export -f mock_curl mock_jq
alias curl='mock_curl'
alias jq='mock_jq'

# Test state management
log "Testing state management..."
source ./src/ephemeral_runner.sh <<'EOF'
state_add "test-runner" "$TEST_DIR/runners/test-runner" "1234" "https://github.com/test/repo" "repo" "test,ephemeral"
state_list
EOF

if [[ ! -f "$RUNNER_STATE_FILE" ]]; then
  err "State file not created."
fi
log "State management OK."

# Test runner start/stop
log "Testing runner start/stop..."
export RUNNER_DIR="$TEST_DIR/runners/test-runner"
export RUNNER_NAME="test-runner"
export TOKEN="mock-token"
export TARGET_URL="https://github.com/test/repo"
export TARGET_TYPE="repo"
export LABELS="test,ephemeral"
export TIMEOUT="10"

# Mock download
export RUNNER_TAR="actions-runner-linux-x64-2.320.2.tar.gz"
export RUNNER_URL="https://example.com/${RUNNER_TAR}"
export RUNNER_CACHE_DIR="$TEST_DIR/cache/runner"

cp "$TEST_DIR/runners/test-runner/actions-runner.tar.gz" "$RUNNER_CACHE_DIR/${RUNNER_TAR}"

tar -xzf "$RUNNER_CACHE_DIR/${RUNNER_TAR}" -C "$RUNNER_DIR" --strip-components=1 2>/dev/null || true

# Mock config and run
./src/ephemeral_runner.sh --repo "$TARGET_URL" --token "$TOKEN" --labels "$LABELS" --runner-dir "$RUNNER_DIR" --timeout 5

if ! grep -q "test-runner" "$RUNNER_STATE_FILE"; then
  err "Runner not registered in state."
fi
log "Runner start/stop OK."

# Cleanup
rm -rf "$TEST_DIR"
log "All tests passed."
