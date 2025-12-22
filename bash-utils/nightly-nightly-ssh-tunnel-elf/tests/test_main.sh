#!/usr/bin/env bash
# Tests for nightly-ssh-tunnel-elf (offline, using mocks)

set -e

# Load the script under test
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.. && pwd)"
source "$SCRIPT_DIR/src/main.sh"

# Mock SSH command – records invocations to a temporary file
MOCK_SSH_LOG=$(mktemp)
mock_ssh() {
  echo "mock_ssh called with: $*" >> "$MOCK_SSH_LOG"
  # Simulate a long‑running background process by sleeping in background
  sleep 60 &
  echo $!   # output a fake PID
}
export SSH_TUNNEL_ELF_SSH_CMD=mock_ssh

# Helper to clean state before each test
reset_state() {
  rm -f /tmp/ssh-tunnel-elf.lock /tmp/ssh-tunnel-elf.pid "$MOCK_SSH_LOG"
}

# Test 1: start creates a tunnel and writes PID file
reset_state
start_tunnel "user@example.com" "1080"
if [[ ! -f /tmp/ssh-tunnel-elf.pid ]]; then
  echo "FAIL: PID file not created"
  exit 1
fi
PID=$(cat /tmp/ssh-tunnel-elf.pid)
if ! kill -0 "$PID" 2>/dev/null; then
  echo "FAIL: Recorded PID is not a running process (mocked)"
  exit 1
fi
if ! grep -q "mock_ssh called with" "$MOCK_SSH_LOG"; then
  echo "FAIL: mock ssh was not invoked"
  exit 1
fi
echo "PASS: start creates tunnel"

# Test 2: status reports active tunnel
STATUS_OUTPUT=$(status_tunnel)
if [[ "$STATUS_OUTPUT" != *"Tunnel is active"* ]]; then
  echo "FAIL: status did not report active tunnel"
  exit 1
fi
echo "PASS: status reports active tunnel"

# Test 3: stop terminates tunnel and cleans files
stop_tunnel
if [[ -f /tmp/ssh-tunnel-elf.pid ]]; then
  echo "FAIL: PID file still exists after stop"
  exit 1
fi
if kill -0 "$PID" 2>/dev/null; then
  echo "FAIL: Process still running after stop"
  exit 1
fi
echo "PASS: stop terminates tunnel"

# Test 4: status after stop reports no tunnel
STATUS_OUTPUT=$(status_tunnel)
if [[ "$STATUS_OUTPUT" != *"No active tunnel"* ]]; then
  echo "FAIL: status still reports active after stop"
  exit 1
fi
echo "PASS: status reports no tunnel after stop"

# Clean up
reset_state
rm -f "$MOCK_SSH_LOG"

echo "All tests passed."
