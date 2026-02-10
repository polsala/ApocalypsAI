#!/usr/bin/env bash
set -euo pipefail

# Create a temporary HOME to avoid touching the real user environment
TMPDIR=$(mktemp -d)
export HOME="$TMPDIR"
SSH_DIR="$HOME/.ssh"
mkdir -p "$SSH_DIR"

# Seed an existing authorized_keys file
echo "oldkey ssh-ed25519 AAAAold" > "$SSH_DIR/authorized_keys"

# Enable mock mode so the script does not call ssh-keygen
export SSH_KEYGEN_MOCK=1

# Run the utility (script is located relative to this test file)
bash ../../src/rotate_ssh_keys.sh -u testuser -d "$SSH_DIR" -b 0

# Verify a new key pair was created
if [[ ! -f "$SSH_DIR"/id_ed25519_* ]]; then
  echo "FAIL: SSH private key not created"
  exit 1
fi

# Verify authorized_keys now contains both old and new entries
if ! grep -q "oldkey" "$SSH_DIR/authorized_keys"; then
  echo "FAIL: original authorized_keys entry missing"
  exit 1
fi
if ! grep -q "mock public key" "$SSH_DIR/authorized_keys"; then
  echo "FAIL: new public key not appended"
  exit 1
fi

# Verify a backup of the original authorized_keys was saved
BACKUP=$(ls "$SSH_DIR"/authorized_keys.backup.* 2>/dev/null | head -n1 || true)
if [[ -z "$BACKUP" ]]; then
  echo "FAIL: backup of authorized_keys not found"
  exit 1
fi

# Clean up temporary directory
rm -rf "$TMPDIR"

echo "PASS"
