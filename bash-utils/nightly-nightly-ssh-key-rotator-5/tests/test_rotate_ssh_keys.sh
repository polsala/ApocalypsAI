#!/usr/bin/env bash
set -euo pipefail

# Create isolated temporary HOME
TMPDIR=$(mktemp -d)
export HOME="$TMPDIR"
export MOCK_SSH_KEYGEN=1

# Prepare a fake existing key pair
mkdir -p "$HOME/.ssh"
echo "OLD PRIVATE" > "$HOME/.ssh/id_ed25519"
echo "OLD PUBLIC" > "$HOME/.ssh/id_ed25519.pub"
echo "OLD PUBLIC" > "$HOME/.ssh/authorized_keys"

# Run the rotator script
bash ../src/rotate_ssh_keys.sh -u testuser

# Assertions
if [[ ! -f "$HOME/.ssh/id_ed25519" ]]; then
  echo "FAIL: New private key missing"
  exit 1
fi
if [[ ! -f "$HOME/.ssh/id_ed25519.pub" ]]; then
  echo "FAIL: New public key missing"
  exit 1
fi
if [[ ! -d "$HOME/.ssh/backup" ]]; then
  echo "FAIL: Backup directory missing"
  exit 1
fi
if [[ -z $(ls "$HOME/.ssh/backup"/id_ed25519_*) ]]; then
  echo "FAIL: Backup key file missing"
  exit 1
fi
if ! grep -qxF "MOCK PUBLIC KEY" "$HOME/.ssh/authorized_keys"; then
  echo "FAIL: authorized_keys not updated with new public key"
  exit 1
fi

echo "All tests passed"
