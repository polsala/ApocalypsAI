#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
# Mock curl
# ---------------------------------------------------------------------------
# This mock captures the arguments passed to curl and simulates API responses.
# Mock rationale: we avoid real network calls and provide deterministic output.
mock_curl() {
  local args=("$@")
  # Detect which endpoint is being called based on URL pattern
  if [[ "${args[*]}" == *"/commits/abc123"* && "${args[*]}" == *"-X POST"* ]]; then
    # Simulate a successful reaction creation response
    echo '{"id":1,"content":"🛠️","created_at":"2023-01-01T00:00:00Z"}'
  elif [[ "${args[*]}" == *"/commits/def456"* && "${args[*]}" == *"-X POST"* ]]; then
    echo '{"id":2,"content":"✨","created_at":"2023-01-01T00:00:00Z"}'
  else
    # Default mock response for any other request
    echo '{}'
  fi
}

# Export the mock so that the script under test uses it instead of real curl
export -f mock_curl
export PATH="$(dirname "$0"):$PATH"

# Alias curl to our mock within this test process
alias curl='mock_curl'

# ---------------------------------------------------------------------------
# Helper to run the action script with given inputs
# ---------------------------------------------------------------------------
run_action() {
  local sha="$1"
  local msg="$2"
  GITHUB_TOKEN="test-token" INPUT_COMMIT_SHA="$sha" INPUT_MESSAGE="$msg" GITHUB_REPOSITORY="owner/repo" INPUT_GITHUB_TOKEN="$GITHUB_TOKEN" bash ./src/annotate.sh
}

# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------
log() { echo "[test] $*"; }

log "Test 1: fix commit should yield 🛠️"
output=$(run_action "abc123" "fix: correct typo")
if echo "$output" | grep -q "🛠️"; then
  log "PASS"
else
  log "FAIL"
  exit 1
fi

log "Test 2: feature commit should yield ✨"
output=$(run_action "def456" "feat: add new login flow")
if echo "$output" | grep -q "✨"; then
  log "PASS"
else
  log "FAIL"
  exit 1
fi

log "All tests passed."
