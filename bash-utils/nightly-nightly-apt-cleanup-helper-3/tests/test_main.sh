#!/usr/bin/env bash
set -euo pipefail

# Path to the script under test
SCRIPT_PATH="../src/main.sh"

# Enable mock mode so no real apt commands are executed
export APT_MOCK=1

# Execute the script in dry‑run mode and capture output
output=$($SCRIPT_PATH --dry-run)

# Expected output (exact string, newline‑separated)
expected=$'Packages that would be removed:\nlibfoo1\nlibbar2'

if [[ "$output" != "$expected" ]]; then
  echo "Test failed: dry‑run output did not match expected."
  echo "--- Got ---"
  echo "$output"
  echo "--- Expected ---"
  echo "$expected"
  exit 1
fi

echo "All tests passed."
