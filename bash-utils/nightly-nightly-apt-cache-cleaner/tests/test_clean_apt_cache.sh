#!/usr/bin/env bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT="$SCRIPT_DIR/clean_apt_cache.sh"

run_test() {
  local desc="$1"
  shift
  echo "Running test: $desc"
  "$@"
  echo "✓ $desc"
}

# Test dry‑run output
output=$(bash "$SCRIPT" -n)
if [[ "$output" != "Would run: sudo apt-get clean" ]]; then
  echo "Dry‑run test failed"
  exit 1
fi
run_test "dry‑run mode prints expected command"

# Test mock mode output
output=$(TEST_MODE=1 bash "$SCRIPT")
if [[ "$output" != "Mock cleaning APT cache (TEST_MODE enabled)." ]]; then
  echo "Mock mode test failed"
  exit 1
fi
run_test "mock mode prints expected message"

echo "All tests passed."
