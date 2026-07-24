#!/usr/bin/env bash

set -euo pipefail

# Directory for mock binaries
MOCK_BIN_DIR="$(mktemp -d)"
export PATH="$MOCK_BIN_DIR:$PATH"

# Log file to capture mock calls
CALL_LOG="$(mktemp)"

# Create mock ssh
cat > "$MOCK_BIN_DIR/ssh" <<'EOF'
#!/usr/bin/env bash
# Mock ssh: record arguments to CALL_LOG
echo "ssh $@" >> "${CALL_LOG}"
# Simulate successful remote command execution
exit 0
EOF
chmod +x "$MOCK_BIN_DIR/ssh"

# Create mock scp
cat > "$MOCK_BIN_DIR/scp" <<'EOF'
#!/usr/bin/env bash
# Mock scp: record arguments to CALL_LOG
echo "scp $@" >> "${CALL_LOG}"
exit 0
EOF
chmod +x "$MOCK_BIN_DIR/scp"

# Prepare a temporary hosts file
HOSTS_FILE="$(mktemp)"
echo "host1.example.com" > "$HOSTS_FILE"
echo "host2.example.com" >> "$HOSTS_FILE"

# Run the utility (using the relative path from repo root)
bash ./src/rotate_ssh_keys.sh "$HOSTS_FILE" testuser

# Verify that ssh and scp were called the expected number of times
EXPECTED_CALLS=6  # 2 hosts * (backup ssh + scp + install ssh) = 6
ACTUAL_CALLS=$(wc -l < "$CALL_LOG")
if [[ "$ACTUAL_CALLS" -ne "$EXPECTED_CALLS" ]]; then
  echo "FAIL: Expected $EXPECTED_CALLS mock calls, got $ACTUAL_CALLS"
  cat "$CALL_LOG"
  exit 1
fi

# Simple content checks
if ! grep -q "ssh testuser@host1.example.com" "$CALL_LOG"; then
  echo "FAIL: Missing ssh call for host1"
  exit 1
fi
if ! grep -q "scp" "$CALL_LOG"; then
  echo "FAIL: Missing scp calls"
  exit 1
fi

echo "All tests passed."
