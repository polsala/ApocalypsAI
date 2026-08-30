#!/usr/bin/env bash
set -euo pipefail

SCRIPT="../src/disk_guardian.sh"

test_low_usage() {
  export MOCK_DF="Filesystem Size Used Avail Use% Mounted on\n/dev/sda1 100G 45G 55G 45% /"
  output=$($SCRIPT)
  if [[ "$output" != "🌞 All good! Disk usage is 45% ." ]]; then
    echo "FAIL low usage: got '$output'"
    exit 1
  fi
  echo "PASS low usage"
}

test_high_usage() {
  export MOCK_DF="Filesystem Size Used Avail Use% Mounted on\n/dev/sda1 100G 85G 15G 85% /"
  output=$($SCRIPT)
  # Expect warning contains the specific phrase
  if [[ "$output" != *"Warning: Disk usage is 85%"* ]]; then
    echo "FAIL high usage: got '$output'"
    exit 1
  fi
  echo "PASS high usage"
}

# Run tests

test_low_usage
test_high_usage
