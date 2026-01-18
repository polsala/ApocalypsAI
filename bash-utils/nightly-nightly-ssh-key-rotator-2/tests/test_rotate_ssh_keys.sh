#!/usr/bin/env bash
set -euo pipefail

# Create temporary SSH directory
TMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

# Simulate existing keys
echo "old private key" > "$TMP_DIR/id_rsa"
echo "old public key" > "$TMP_DIR/id_rsa.pub"

# Run the rotator (script is located one level up in src/)
bash "../src/rotate_ssh_keys.sh" -d "$TMP_DIR"

# 1. Backup directory exists and contains old keys
if [[ ! -d "$TMP_DIR/backup" ]]; then
  echo "FAIL: backup directory missing"
  exit 1
fi
if [[ ! -f "$TMP_DIR/backup/id_rsa" ]] || [[ ! -f "$TMP_DIR/backup/id_rsa.pub" ]]; then
  echo "FAIL: old keys not moved to backup"
  exit 1
fi

# 2. New key files exist
if [[ ! -f "$TMP_DIR/id_ed25519" ]] || [[ ! -f "$TMP_DIR/id_ed25519.pub" ]]; then
  echo "FAIL: new key pair not created"
  exit 1
fi

# 3. authorized_keys contains the new public key
if ! diff -q "$TMP_DIR/id_ed25519.pub" "$TMP_DIR/authorized_keys" > /dev/null; then
  echo "FAIL: authorized_keys does not match new public key"
  exit 1
fi

echo "PASS"
