#!/usr/bin/env bash
# Tests for nightly-disk-usage-whisperer

set -euo pipefail

SCRIPT="../src/main.sh"

# Mock df output
cat > sample_df.txt <<'EOF'
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   45G    5G  90% /
/dev/sda2        20G   10G   10G  50% /home
tmpfs           2.0G     0  2.0G   0% /run
EOF

# Test with default threshold (80%) – expect warning on /dev/sda1
output=$(bash "$SCRIPT" 80 "$PWD/sample_df.txt")
if ! echo "$output" | grep -q "/dev/sda1.*⚠️"; then
    echo "Test failed: expected warning for /dev/sda1 at 80% threshold"
    exit 1
fi

# Test with higher threshold (95%) – no warnings expected
output=$(bash "$SCRIPT" 95 "$PWD/sample_df.txt")
if echo "$output" | grep -q "⚠️"; then
    echo "Test failed: did not expect any warnings at 95% threshold"
    exit 1
fi

echo "All tests passed."
