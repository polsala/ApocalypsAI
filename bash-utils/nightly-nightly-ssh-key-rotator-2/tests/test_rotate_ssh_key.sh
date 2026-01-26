#!/usr/bin/env bash
set -euo pipefail

# Create a temporary directory to act as a fake .ssh folder
TMPDIR=$(mktemp -d)
cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

# Prepare mock existing keys
echo "old private" > "$TMPDIR/id_test"
chmod 600 "$TMPDIR/id_test"
echo "old public" > "$TMPDIR/id_test.pub"
chmod 644 "$TMPDIR/id_test.pub"

# Run the rotator in mock mode
MOCK_SSH_KEYGEN=1 "${BASH_SOURCE%/*}/../src/rotate_ssh_key.sh" -d "$TMPDIR" -f "id_test"

# Verify that backup files were created
BACKUP_PRIV=$(ls "$TMPDIR"/id_test.bak.* 2>/dev/null || true)
if [[ -z "$BACKUP_PRIV" ]]; then
  echo "FAIL: Private key backup not found"
  exit 1
fi
BACKUP_PUB=$(ls "$TMPDIR"/id_test.pub.bak.* 2>/dev/null || true)
if [[ -z "$BACKUP_PUB" ]]; then
  echo "FAIL: Public key backup not found"
  exit 1
fi

# Verify new key contents
if ! grep -q "mock private key" "$TMPDIR/id_test"; then
  echo "FAIL: New private key content incorrect"
  exit 1
fi
if ! grep -q "mock public key" "$TMPDIR/id_test.pub"; then
  echo "FAIL: New public key content incorrect"
  exit 1
fi

echo "PASS"
