#!/usr/bin/env bash
set -euo pipefail

# Test 1: usage below threshold
cat > /tmp/mock_low <<'EOF'
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   20G   28G  42% /
EOF

result=$(THRESHOLD=80 DF_MOCK_FILE=/tmp/mock_low ./src/disk_watcher.sh; echo $?)
if [[ $result -ne 0 ]]; then
  echo "Test 1 failed: expected exit 0, got $result"
  exit 1
fi

# Test 2: usage above threshold
cat > /tmp/mock_high <<'EOF'
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   45G    5G  90% /
EOF

result=$(THRESHOLD=80 DF_MOCK_FILE=/tmp/mock_high ./src/disk_watcher.sh; echo $?)
if [[ $result -ne 1 ]]; then
  echo "Test 2 failed: expected exit 1, got $result"
  exit 1
fi

echo "All tests passed."
