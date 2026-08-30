#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)
SCRIPT="$SCRIPT_DIR/disk_guardian.sh"

# Helper to execute the script with a mock df file and verify outcome
run_test() {
  local df_file=$1
  local expected_exit=$2
  local expected_pattern=$3

  DISK_DF_FILE="$df_file" bash "$SCRIPT" >output.txt 2>&1 || true
  local exit_code=$?

  if [[ $exit_code -ne $expected_exit ]]; then
    echo "FAIL: Expected exit $expected_exit, got $exit_code"
    cat output.txt
    exit 1
  fi

  if ! grep -q "$expected_pattern" output.txt; then
    echo "FAIL: Expected output containing '$expected_pattern'"
    cat output.txt
    exit 1
  fi

  echo "PASS"
}

# Mock df output with low usage (42%)
cat > low.txt <<'EOF'
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   20G   28G  42% /
EOF

# Mock df output with high usage (90%)
cat > high.txt <<'EOF'
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   45G    5G  90% /
EOF

echo "Testing low usage (should be OK)"
run_test low.txt 0 "✅ Disk usage is 42%, below threshold"

echo "Testing high usage (should warn)"
run_test high.txt 1 "⚠️"
