#!/bin/bash

set -euo pipefail

# Mock rationale: Avoid actual system changes during testing by replacing real commands with echo.

# Save original PATH
ORIG_PATH="$PATH"

# Create mock bin directory
MOCK_BIN=$(mktemp -d)
cp src/chaos-monkey-scheduler.sh "$MOCK_BIN/"

# Mock systemctl and tc
mkdir -p "$MOCK_BIN"
cat > "$MOCK_BIN/systemctl" <<'EOF'
#!/bin/bash
echo "[MOCK systemctl] $*"
EOF

cat > "$MOCK_BIN/tc" <<'EOF'
#!/bin/bash
echo "[MOCK tc] $*"
EOF

chmod +x "$MOCK_BIN/systemctl" "$MOCK_BIN/tc"

# Prepend mock bin to PATH
export PATH="$MOCK_BIN:$ORIG_PATH"

# Test 1: Network delay dry run
output=$("$MOCK_BIN/chaos-monkey-scheduler.sh" --type network --delay 500 --interval '@daily' --dry-run)
if [[ "$output" != *"[DRY RUN] Would schedule: tc qdisc add dev lo root netem delay 500ms at '@daily'"* ]]; then
  echo "FAIL: Test 1 failed"
  exit 1
fi
echo "PASS: Test 1 passed"

# Test 2: Service restart dry run
output=$("$MOCK_BIN/chaos-monkey-scheduler.sh" --type service --service nginx --interval '0 2 * * *' --dry-run)
if [[ "$output" != *"[DRY RUN] Would schedule: systemctl restart nginx at '0 2 * * *'"* ]]; then
  echo "FAIL: Test 2 failed"
  exit 1
fi
echo "PASS: Test 2 passed"

# Test 3: Missing required args
set +e
output=$("$MOCK_BIN/chaos-monkey-scheduler.sh" --type network 2>&1)
exit_code=$?
set -e
if [[ $exit_code -ne 1 || "$output" != *"--interval are required"* ]]; then
  echo "FAIL: Test 3 failed"
  exit 1
fi
echo "PASS: Test 3 passed"

# Cleanup
rm -rf "$MOCK_BIN"
