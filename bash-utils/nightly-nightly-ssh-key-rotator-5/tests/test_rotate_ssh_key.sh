#!/usr/bin/env bash

# Test suite for nightly-ssh-key-rotator (mock mode)
# ---------------------------------------------------
# This script creates a temporary .ssh directory, populates it with a dummy
# authorized_keys file, runs the rotator with --mock-keygen, and verifies that:
#   * A new private key file exists
#   * A new public key file exists
#   * authorized_keys.bak contains the original key
#   * authorized_keys now contains the mock public key

set -euo pipefail

# Create temporary workspace
TMPDIR=$(mktemp -d)
SSHDIR="$TMPDIR/.ssh"
mkdir -p "$SSHDIR"

echo "old-public-key" > "$SSHDIR/authorized_keys"

# Run the rotator in mock mode
bash ../../src/rotate_ssh_key.sh -u testuser -d "$SSHDIR" --mock-keygen

# Assertions
if [[ ! -f "$SSHDIR/id_rsa_new" ]]; then
  echo "FAIL: Private key (id_rsa_new) not created"
  exit 1
fi
if [[ ! -f "$SSHDIR/id_rsa_new.pub" ]]; then
  echo "FAIL: Public key (id_rsa_new.pub) not created"
  exit 1
fi
if [[ ! -f "$SSHDIR/authorized_keys.bak" ]]; then
  echo "FAIL: Backup authorized_keys (authorized_keys.bak) not created"
  exit 1
fi

# Verify contents
if ! grep -q "mock-public-key" "$SSHDIR/authorized_keys"; then
  echo "FAIL: New authorized_keys does not contain mock public key"
  exit 1
fi
if ! grep -q "old-public-key" "$SSHDIR/authorized_keys.bak"; then
  echo "FAIL: Backup authorized_keys does not contain original key"
  exit 1
fi

echo "All tests passed"
