#!/usr/bin/env bash

# nightly-ssh-key-rotator – rotate SSH keys safely
# -------------------------------------------------
# This script generates a new RSA key pair, backs up the existing
# authorized_keys file, and installs the new public key.
#
# Flags:
#   -u <username>   : Identifier for logging (optional, defaults to current user)
#   -d <ssh_dir>    : Path to the .ssh directory (required)
#   --mock-keygen   : Use mock key generation (for testing)
#
# Exit on any error
set -euo pipefail

# Default values
USERNAME="$(whoami)"
SSH_DIR=""
MOCK_MODE="false"

print_usage() {
  echo "Usage: $0 -u <username> -d <ssh_dir> [--mock-keygen]"
  exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -u)
      USERNAME="$2"
      shift 2
      ;;
    -d)
      SSH_DIR="$2"
      shift 2
      ;;
    --mock-keygen)
      MOCK_MODE="true"
      shift
      ;;
    -h|--help)
      print_usage
      ;;
    *)
      echo "Unknown argument: $1"
      print_usage
      ;;
  esac
done

if [[ -z "$SSH_DIR" ]]; then
  echo "Error: SSH directory must be provided with -d"
  print_usage
fi

# Ensure directory exists
if [[ ! -d "$SSH_DIR" ]]; then
  echo "Error: Directory $SSH_DIR does not exist"
  exit 1
fi

# Paths
AUTH_KEYS="$SSH_DIR/authorized_keys"
BACKUP_AUTH_KEYS="$SSH_DIR/authorized_keys.bak"
PRIVATE_KEY="$SSH_DIR/id_rsa_new"
PUBLIC_KEY="$SSH_DIR/id_rsa_new.pub"

# Backup existing authorized_keys if it exists
if [[ -f "$AUTH_KEYS" ]]; then
  cp "$AUTH_KEYS" "$BACKUP_AUTH_KEYS"
  echo "[$USERNAME] Backed up existing authorized_keys to authorized_keys.bak"
else
  echo "[$USERNAME] No existing authorized_keys found; proceeding without backup"
fi

# Generate new key pair
if [[ "$MOCK_MODE" == "true" ]]; then
  echo "mock-private-key" > "$PRIVATE_KEY"
  echo "mock-public-key" > "$PUBLIC_KEY"
  chmod 600 "$PRIVATE_KEY"
  chmod 644 "$PUBLIC_KEY"
  echo "[$USERNAME] Mock key pair generated (id_rsa_new, id_rsa_new.pub)"
else
  # Use ssh-keygen; -N '' for empty passphrase, -f for output file
  ssh-keygen -t rsa -b 2048 -N "" -f "$PRIVATE_KEY" -q
  echo "[$USERNAME] Real RSA key pair generated"
fi

# Install new public key as authorized_keys
cat "$PUBLIC_KEY" > "$AUTH_KEYS"
chmod 600 "$AUTH_KEYS"

echo "[$USERNAME] New public key installed to authorized_keys"

echo "[$USERNAME] Rotation complete. Private key: $PRIVATE_KEY"
