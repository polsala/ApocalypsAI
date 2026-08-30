#!/usr/bin/env bash

# Test suite for nightly-ssh-key-rotator
# ---------------------------------------------------

set -euo pipefail

# Load the script under test in a subshell to avoid polluting the test environment.
SCRIPT_PATH="$(dirname "${BASH_SOURCE[0]}")/../src/rotate_ssh_keys.sh"

# Create a temporary working directory
WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

# Mock SSH command that records its invocations
MOCK_SSH_LOG="$WORKDIR/mock_ssh.log"
mock_ssh() {
  echo "MOCK_SSH: $*" >> "$MOCK_SSH_LOG"
  # Simulate a successful remote command without doing anything.
  return 0
}
export -f mock_ssh
export SSH_CMD="mock_ssh"

# Prepare a hosts file with two dummy hosts
HOSTS_FILE="$WORKDIR/hosts.txt"
cat > "$HOSTS_FILE" <<EOF
host-a.example.com
host-b.example.com
EOF

# Run the script (it will generate a key pair in a temporary dir)
bash "$SCRIPT_PATH" -u testuser -h "$HOSTS_FILE"

# ---- Assertions ----
# 1. The mock SSH log should contain backup and deploy commands for each host.
EXPECTED_COUNT=4  # 2 hosts * (backup + deploy)
ACTUAL_COUNT=$(grep -c "MOCK_SSH:" "$MOCK_SSH_LOG" || true)
if [[ "$ACTUAL_COUNT" -ne "$EXPECTED_COUNT" ]]; then
  echo "FAIL: Expected $EXPECTED_COUNT SSH invocations, got $ACTUAL_COUNT"
  echo "Log contents:"
  cat "$MOCK_SSH_LOG"
  exit 1
fi

# 2. Verify that each host appears twice (backup then deploy)
for host in host-a.example.com host-b.example.com; do
  OCCURS=$(grep -c "$host" "$MOCK_SSH_LOG" || true)
  if [[ "$OCCURS" -ne 2 ]]; then
    echo "FAIL: Host $host should appear twice in mock SSH log, found $OCCURS"
    exit 1
  fi
done

echo "PASS: All tests succeeded."
