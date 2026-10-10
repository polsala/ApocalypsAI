#!/usr/bin/env bash

# Test suite for nightly-ssh-key-rotator
# ---------------------------------------------------------------

set -euo pipefail

# Helper: create a temporary directory and clean up on exit
TMP_ROOT=$(mktemp -d)
cleanup() { rm -rf "$TMP_ROOT"; }
trap cleanup EXIT

KEY_DIR="$TMP_ROOT/ssh_keys"
BACKUP_DIR="$TMP_ROOT/backup"

mkdir -p "$KEY_DIR"

# Create dummy key files (content is irrelevant)
for key in ssh_host_rsa_key ssh_host_rsa_key.pub ssh_host_ecdsa_key ssh_host_ecdsa_key.pub; do
  echo "old-$key" > "$KEY_DIR/$key"
done

# Path to the script under test
SCRIPT_PATH="$(dirname "${BASH_SOURCE[0]}")/../src/rotate_ssh_keys.sh"

# Run the rotator (non‑dry‑run) with custom directories
bash "$SCRIPT_PATH" --key-dir "$KEY_DIR" --backup-dir "$BACKUP_DIR"

# ---- Assertions ----
# 1. Backup directory should exist and contain renamed files
if [[ ! -d "$BACKUP_DIR" ]]; then
  echo "FAIL: Backup directory was not created" >&2
  exit 1
fi

backup_count=$(ls -1 "$BACKUP_DIR" | wc -l)
if (( backup_count != 4 )); then
  echo "FAIL: Expected 4 backup files, found $backup_count" >&2
  exit 1
fi

# 2. New placeholder files should exist and be empty
for key in ssh_host_rsa_key ssh_host_rsa_key.pub ssh_host_ecdsa_key ssh_host_ecdsa_key.pub; do
  if [[ ! -f "$KEY_DIR/$key" ]]; then
    echo "FAIL: New placeholder $key missing" >&2
    exit 1
  fi
  if [[ -s "$KEY_DIR/$key" ]]; then
    echo "FAIL: Placeholder $key is not empty" >&2
    exit 1
  fi
done

# 3. Files that were not present originally should be untouched (e.g., ed25519)
if [[ -e "$KEY_DIR/ssh_host_ed25519_key" ]]; then
  echo "FAIL: Unexpected ed25519 key file created" >&2
  exit 1
fi

echo "All tests passed."
exit 0
