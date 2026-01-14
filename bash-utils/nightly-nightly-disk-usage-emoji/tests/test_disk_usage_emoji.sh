#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
SCRIPT="${SCRIPT_DIR}/src/disk_usage_emoji.sh"

# Mock du output: size (KB) TAB path
export DISK_USAGE_MOCK_DATA=$'1200\t./dirA\n800\t./dirB\n50\t./dirC'

expected=$'./dirA 📦📦📦📦📦📦\n./dirB 📦📦📦📦\n./dirC'

output=$("$SCRIPT" .)

if [[ "$output" != "$expected" ]]; then
  echo "Test failed"
  echo "Expected:"
  echo "$expected"
  echo "Got:"
  echo "$output"
  exit 1
fi
echo "Test passed"
