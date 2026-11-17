#!/usr/bin/env bash
set -euo pipefail

# Mock ssh-copy-id to capture calls
MOCK_DIR="$(mktemp -d)"
export PATH="$MOCK_DIR:$PATH"

cat > "$MOCK_DIR/ssh-copy-id" <<'EOF'
#!/usr/bin/env bash
# Mock implementation: log arguments to a file
echo "$@" >> "${HOME}/ssh_copy_id_calls.log"
exit 0
EOF
chmod +x "$MOCK_DIR/ssh-copy-id"

# Prepare temporary environment
TMPDIR="$(mktemp -d)"
HOSTS_FILE="$TMPDIR/hosts.txt"
cat > "$HOSTS_FILE" <<EOF
host1.example.com
host2.example.com
EOF

# Run the utility
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
"$SCRIPT_DIR/rotate_ssh_keys.sh" -u testuser -f "$HOSTS_FILE" -d "$TMPDIR/keys"

# Verify key files exist
if [[ ! -f "$TMPDIR/keys/id_ed25519" || ! -f "$TMPDIR/keys/id_ed25519.pub" ]]; then
  echo "Key files not created"
  exit 1
fi

# Verify ssh-copy-id was called correctly
EXPECTED_LOG="${HOME}/ssh_copy_id_calls.log"
if [[ ! -f "$EXPECTED_LOG" ]]; then
  echo "Mock ssh-copy-id was not invoked"
  exit 1
fi

# Check contents
if ! grep -q "testuser@host1.example.com" "$EXPECTED_LOG"; then
  echo "Missing call for host1"
  exit 1
fi
if ! grep -q "testuser@host2.example.com" "$EXPECTED_LOG"; then
  echo "Missing call for host2"
  exit 1
fi

echo "All tests passed."
