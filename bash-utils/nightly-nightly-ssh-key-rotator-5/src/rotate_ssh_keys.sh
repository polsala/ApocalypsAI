#!/usr/bin/env bash
set -euo pipefail

# Default key directory
KEY_DIR="${HOME}/.ssh/rotated"

usage() {
  echo "Usage: $0 -u <username> -f <hosts_file> [-d <key_dir>]"
  exit 1
}

# Parse arguments
while getopts ":u:f:d:" opt; do
  case $opt in
    u) USERNAME="$OPTARG" ;;
    f) HOSTS_FILE="$OPTARG" ;;
    d) KEY_DIR="$OPTARG" ;;
    *) usage ;;
  esac
done

if [[ -z "${USERNAME:-}" || -z "${HOSTS_FILE:-}" ]]; then
  usage
fi

if [[ ! -f "$HOSTS_FILE" ]]; then
  echo "Hosts file not found: $HOSTS_FILE"
  exit 1
fi

mkdir -p "$KEY_DIR"
PRIVATE_KEY="$KEY_DIR/id_ed25519"
PUBLIC_KEY="${PRIVATE_KEY}.pub"

# Generate new key pair (overwrite if exists)
ssh-keygen -t ed25519 -f "$PRIVATE_KEY" -N "" -q

echo "Generated new key pair at $PRIVATE_KEY"

# Distribute public key
while IFS= read -r HOST; do
  [[ -z "$HOST" ]] && continue
  echo "Copying public key to $USERNAME@$HOST ..."
  ssh-copy-id -i "$PUBLIC_KEY" "${USERNAME}@${HOST}"
 done < "$HOSTS_FILE"

echo "Key rotation complete."
