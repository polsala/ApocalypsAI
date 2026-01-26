#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 [-d SSH_DIR] [-f KEY_NAME] [-n]" >&2
  exit 1
}

SSH_DIR="${HOME}/.ssh"
KEY_NAME="id_rsa"
DRY_RUN=0

while getopts ":d:f:n" opt; do
  case $opt in
    d) SSH_DIR="$OPTARG" ;;
    f) KEY_NAME="$OPTARG" ;;
    n) DRY_RUN=1 ;;
    *) usage ;;
  esac
done

PRIVATE_KEY="${SSH_DIR}/${KEY_NAME}"
PUBLIC_KEY="${PRIVATE_KEY}.pub"
TIMESTAMP=$(date +%Y%m%d%H%M%S)

backup() {
  local src=$1 dest=$2
  if [[ -f "$src" ]]; then
    cp "$src" "$dest"
    echo "Backed up $src to $dest"
  fi
}

if [[ $DRY_RUN -eq 1 ]]; then
  echo "Dry-run mode: no changes will be made."
  exit 0
fi

mkdir -p "$SSH_DIR"

# Backup existing keys
backup "$PRIVATE_KEY" "${PRIVATE_KEY}.bak.${TIMESTAMP}"
backup "$PUBLIC_KEY" "${PUBLIC_KEY}.bak.${TIMESTAMP}"

# Generate new key
if [[ "${MOCK_SSH_KEYGEN:-0}" == "1" ]]; then
  echo "mock private key" > "$PRIVATE_KEY"
  chmod 600 "$PRIVATE_KEY"
  echo "mock public key" > "$PUBLIC_KEY"
  chmod 644 "$PUBLIC_KEY"
  echo "Mock key pair generated at $PRIVATE_KEY"
else
  ssh-keygen -t rsa -b 4096 -f "$PRIVATE_KEY" -N "" -q
  echo "New key pair generated at $PRIVATE_KEY"
fi
