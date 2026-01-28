#!/usr/bin/env bash
set -euo pipefail

# Test for nightly-ssh-key-rotator
# Uses a temporary directory to avoid side effects.

TMPDIR=$(mktemp -d)
SSH_DIR="$TMPDIR/.ssh"
mkdir -p "$SSH_DIR"

# Create dummy existing keys
echo "old_private_key" > "$SSH_DIR/id_rsa"
chmod 600 "$SSH_DIR/id_rsa"

echo "old_public_key" > "$SSH_DIR/id_rsa.pub"
chmod 644 "$SSH_DIR/id_rsa.pub"

# Run the rotator script
bash ../../src/rotate_ssh_keys.sh "$SSH_DIR"

# Assertions
if [[ ! -f "$SSH_DIR/id_rsa" ]]; then
  echo "ERROR: New private key missing"
  exit 1
fi
if [[ ! -f "$SSH_DIR/id_rsa.pub" ]]; then
  echo "ERROR: New public key missing"
  exit 1
fi
if [[ ! -f "$SSH_DIR/id_rsa.old" ]]; then
  echo "ERROR: Old private key backup missing"
  exit 1
fi
if [[ ! -f "$SSH_DIR/id_rsa.pub.old" ]]; then
  echo "ERROR: Old public key backup missing"
  exit 1
fi

# Verify contents
if ! grep -q "new_private_key" "$SSH_DIR/id_rsa"; then
  echo "ERROR: New private key content incorrect"
  exit 1
fi
if ! grep -q "new_public_key" "$SSH_DIR/id_rsa.pub"; then
  echo "ERROR: New public key content incorrect"
  exit 1
fi

# Clean up
rm -rf "$TMPDIR"

echo "All tests passed"
