#!/usr/bin/env bash

# nightly-ssh-key-rotator
# Rotates SSH keys for a user across multiple hosts.
# ---------------------------------------------------

set -euo pipefail

# Default to the system ssh binary; can be overridden for testing.
SSH_CMD="${SSH_CMD:-ssh}"

usage() {
  cat <<'EOF'
Usage: ./rotate_ssh_keys.sh -u <remote_user> -h <hosts_file> [-d <dest_dir>]

  -u   Remote username whose keys will be rotated (required)
  -h   File containing hostnames/IPs, one per line (required)
  -d   Destination directory for the generated key pair (optional, defaults to a temporary dir)
EOF
  exit 1
}

# Parse arguments
while getopts ":u:h:d:" opt; do
  case $opt in
    u) REMOTE_USER="$OPTARG" ;;
    h) HOSTS_FILE="$OPTARG" ;;
    d) DEST_DIR="$OPTARG" ;;
    *) usage ;;
  esac
done

# Validate required arguments
if [[ -z "${REMOTE_USER:-}" || -z "${HOSTS_FILE:-}" ]]; then
  usage
fi

if [[ ! -f "$HOSTS_FILE" ]]; then
  echo "Error: hosts file '$HOSTS_FILE' does not exist." >&2
  exit 1
fi

# Create a temporary directory for the key pair if not supplied
if [[ -z "${DEST_DIR:-}" ]]; then
  DEST_DIR="$(mktemp -d)"
  CLEANUP_DEST=true
else
  mkdir -p "$DEST_DIR"
  CLEANUP_DEST=false
fi

KEY_PRIV="$DEST_DIR/id_ed25519"
KEY_PUB="$DEST_DIR/id_ed25519.pub"

generate_key() {
  echo "Generating new ed25519 key pair..."
  ssh-keygen -t ed25519 -f "$KEY_PRIV" -N "" -q
}

backup_remote_authorized_keys() {
  local host="$1"
  echo "Backing up authorized_keys on $host..."
  $SSH_CMD "$REMOTE_USER@$host" "mkdir -p ~/.ssh && cp -p ~/.ssh/authorized_keys ~/.ssh/authorized_keys.bak || true"
}

deploy_new_key() {
  local host="$1"
  echo "Deploying new public key to $host..."
  $SSH_CMD "$REMOTE_USER@$host" "mkdir -p ~/.ssh && cat > ~/.ssh/authorized_keys" < "$KEY_PUB"
}

rotate_host() {
  local host="$1"
  backup_remote_authorized_keys "$host"
  deploy_new_key "$host"
}

# Main execution
generate_key

while IFS= read -r host || [[ -n "$host" ]]; do
  # Skip empty lines or comments
  [[ -z "$host" || "$host" =~ ^# ]] && continue
  rotate_host "$host"
  echo "Rotated keys on $host"
 done < "$HOSTS_FILE"

echo "All hosts processed. New key pair stored in $DEST_DIR"

# Cleanup temporary directory unless user asked to keep it
if [[ "$CLEANUP_DEST" == true ]]; then
  rm -rf "$DEST_DIR"
fi

exit 0
