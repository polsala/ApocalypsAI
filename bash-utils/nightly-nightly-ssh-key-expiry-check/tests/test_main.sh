#!/usr/bin/env bash
set -euo pipefail

# Create temp authorized_keys
TMPFILE=$(mktemp)
cat > "$TMPFILE" <<'EOF'
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC... user@example.com (expires=2022-12-31)
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD... user2@example.com (expires=2025-01-01)
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQE... user3@example.com
EOF

# Test expired
CURRENT_DATE="2023-01-01" ./src/main.sh "$TMPFILE"
RET=$?
if [[ $RET -ne 1 ]]; then
  echo "Expected exit 1 for expired key"
  exit 1
fi

# Test all valid
CURRENT_DATE="2025-01-02" ./src/main.sh "$TMPFILE"
RET=$?
if [[ $RET -ne 0 ]]; then
  echo "Expected exit 0 for all valid keys"
  exit 1
fi

echo "All tests passed"
exit 0
