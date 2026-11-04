#!/usr/bin/env bash
# Simple test harness for nightly-disk-usage-emoji-alert
# No external test framework; uses basic bash assertions.

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
SCRIPT="$SCRIPT_DIR/src/disk_alert.sh"

# Mock df output (header + two lines)
read -r -d '' MOCK_DF <<'EOF'
Filesystem Size Used Avail Use% Mounted on
/dev/sda1 45G 20G 23G 47% /
/dev/sdb2 100G 85G 10G 90% /var
EOF

# Run script with mock input and a threshold of 80
output=$(echo "$MOCK_DF" | "$SCRIPT" 80)

# Expected lines (emoji, filesystem, size, used, percent, mount)
expected_line1="🟢 /dev/sda1 45G 20G 47% /"
expected_line2="🔴 /dev/sdb2 100G 85G 90% /var"

# Helper to trim leading/trailing whitespace
trim() { echo "$1" | xargs; }

# Assertions
if [[ "$(trim "$output" | grep -F "$expected_line1")" == "" ]]; then
  echo "FAIL: Expected green line not found"
  echo "Output was:"
  echo "$output"
  exit 1
fi

if [[ "$(trim "$output" | grep -F "$expected_line2")" == "" ]]; then
  echo "FAIL: Expected red line not found"
  echo "Output was:"
  echo "$output"
  exit 1
fi

echo "PASS: All checks passed"
