#!/usr/bin/env bash

# Test suite for nightly-ssh-key-rotator
# Uses a mock ssh-keygen to avoid real key generation.

set -euo pipefail

# Create a temporary directory for the fake .ssh folder
TMPDIR=$(mktemp -d)
SSH_DIR="$TMPDIR/.ssh"
mkdir -p "$SSH_DIR"

# Place dummy existing keys
echo "old private" > "$SSH_DIR/id_rsa"
chmod 600 "$SSH_DIR/id_rsa"
echo "old public" > "$SSH_DIR/id_rsa.pub"
chmod 644 "$SSH_DIR/id_rsa.pub"

# Create a mock ssh-keygen that just creates placeholder files
MOCK_BIN="$TMPDIR/mock_bin"
mkdir -p "$MOCK_BIN"
cat > "$MOCK_BIN/ssh-keygen" <<'EOF'
#!/usr/bin/env bash
# Mock ssh-keygen: create empty private and public key files
while [[ $# -gt 0 ]]; do
  case $1 in
    -f) shift; KEYFILE="$1";;
    *) ;;
  esac
  shift
done
# Create private key file
printf "mock private key" > "$KEYFILE"
chmod 600 "$KEYFILE"
# Create public key file
printf "mock public key" > "${KEYFILE}.pub"
chmod 644 "${KEYFILE}.pub"
EOF
chmod +x "$MOCK_BIN/ssh-keygen"

# Prepend mock bin to PATH
export PATH="$MOCK_BIN:$PATH"

# Run the script with the custom SSH_DIR
SSH_DIR="$SSH_DIR" ./src/rotate_ssh_keys.sh

# Verify that backup files exist
BACKUP_PRIV=$(ls "$SSH_DIR"/id_rsa.bak.* 2>/dev/null || true)
BACKUP_PUB=$(ls "$SSH_DIR"/id_rsa.pub.bak.* 2>/dev/null || true)
if [[ -z "$BACKUP_PRIV" || -z "$BACKUP_PUB" ]]; then
  echo "FAIL: Backup files were not created" >&2
  exit 1
fi

# Verify that new key files exist and contain mock data
if [[ ! -f "$SSH_DIR/id_rsa" || ! -f "$SSH_DIR/id_rsa.pub" ]]; then
  echo "FAIL: New key files missing" >&2
  exit 1
fi
if ! grep -q "mock private key" "$SSH_DIR/id_rsa"; then
  echo "FAIL: New private key does not contain mock data" >&2
  exit 1
fi
if ! grep -q "mock public key" "$SSH_DIR/id_rsa.pub"; then
  echo "FAIL: New public key does not contain mock data" >&2
  exit 1
fi

echo "PASS: SSH key rotation behaved as expected"

# Cleanup
rm -rf "$TMPDIR"

exit 0
