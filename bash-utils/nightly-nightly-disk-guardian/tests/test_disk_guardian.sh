#!/usr/bin/env bash

set -euo pipefail

SCRIPT="../src/disk_guardian.sh"

# Create a mock df output with two mount points: one at 85% and one at 45%
cat > mock_df.txt <<'EOF'
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   42G   8G  85% /
/dev/sda2        100G  45G  55G  45% /data
EOF

# Test 1: threshold 80% should trigger a warning and exit with code 1
if $SCRIPT 80 mock_df.txt; then
  echo "Test 1 failed: expected non-zero exit code when usage exceeds threshold"
  exit 1
fi

# Test 2: higher threshold 90% should produce no warning and exit with code 0
if ! $SCRIPT 90 mock_df.txt; then
  echo "Test 2 failed: expected zero exit code when usage is below threshold"
  exit 1
fi

echo "All tests passed"
