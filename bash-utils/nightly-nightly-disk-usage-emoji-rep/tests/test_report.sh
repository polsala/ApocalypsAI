#!/usr/bin/env bash
# Test suite for nightly‑disk‑usage‑emoji‑report

set -euo pipefail

# Locate the script under test
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
REPORT_SH="$SCRIPT_DIR/report.sh"

# Helper to run the script with a mocked df output
run_with_mock() {
  local mock_output="$1"
  DF_MOCK="$mock_output" bash "$REPORT_SH" "$2"
}

# Mock df output with three filesystems covering the three emoji thresholds
read -r -d '' MOCK_DF <<'EOF'
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   10G   40G  20% /
/dev/sda2       100G   70G   30G  70% /home
/dev/sda3       200G  180G   20G  90% /var
EOF

# Execute the script
OUTPUT=$(run_with_mock "$MOCK_DF" "/")

# Extract the emoji column (last field) from each data line
EMOJIS=$(echo "$OUTPUT" | tail -n +2 | awk '{print $NF}')

# Expected emojis: 🟢 for 20% used (80% free), 🟡 for 70% used (30% free), 🔴 for 90% used (10% free)
EXPECTED="🟢
🟡
🔴"

if [[ "$EMOJIS" != "$EXPECTED" ]]; then
  echo "Test FAILED"
  echo "Expected emojis:"; echo -e "$EXPECTED"
  echo "Got emojis:"; echo -e "$EMOJIS"
  exit 1
else
  echo "All tests passed."
fi
