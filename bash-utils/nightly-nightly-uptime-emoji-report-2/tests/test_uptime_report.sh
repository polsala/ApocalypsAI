#!/usr/bin/env bash

# Tests for nightly-uptime-emoji-report
# These tests are deterministic and do not depend on the real system uptime.
# They create temporary mock files that mimic /proc/uptime.

set -euo pipefail

SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)/uptime_report.sh"

# Helper to run the script with a given mock file and capture output
run_with_mock() {
  local mock_file="$1"
  UPTIME_FILE="$mock_file" bash "$SCRIPT_PATH"
}

# Test case 1: uptime >= 1 day (green)
cat > /tmp/mock_uptime_1d.txt <<'EOF'
90000 0.00
EOF
output=$(run_with_mock /tmp/mock_uptime_1d.txt)
if [[ "$output" != *"🟢"* ]]; then
  echo "FAIL: Expected green emoji for 1 day uptime, got: $output" >&2
  exit 1
fi

# Test case 2: uptime between 6h and 1d (yellow)
cat > /tmp/mock_uptime_8h.txt <<'EOF'
30000 0.00
EOF
output=$(run_with_mock /tmp/mock_uptime_8h.txt)
if [[ "$output" != *"🟡"* ]]; then
  echo "FAIL: Expected yellow emoji for 8h uptime, got: $output" >&2
  exit 1
fi

# Test case 3: uptime < 6h (red)
cat > /tmp/mock_uptime_5m.txt <<'EOF'
500 0.00
EOF
output=$(run_with_mock /tmp/mock_uptime_5m.txt)
if [[ "$output" != *"🔴"* ]]; then
  echo "FAIL: Expected red emoji for 5 minute uptime, got: $output" >&2
  exit 1
fi

# Clean up temporary files
rm -f /tmp/mock_uptime_1d.txt /tmp/mock_uptime_8h.txt /tmp/mock_uptime_5m.txt

echo "All tests passed for nightly-uptime-emoji-report"
