#!/usr/bin/env bash
set -euo pipefail

# Test default emoji
output=$(./src/main.sh)
if [[ "$output" != "Logging: 😃" ]]; then
  echo "FAIL: default emoji mismatch: $output"
  exit 1
fi

# Test custom emoji
export EMOJI="🚀"
output=$(./src/main.sh)
if [[ "$output" != "Logging: 🚀" ]]; then
  echo "FAIL: custom emoji mismatch: $output"
  exit 1
fi

echo "PASS"
