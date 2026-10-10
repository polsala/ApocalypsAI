#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 -u USERNAME [-d KEY_DIR]"
  exit 1
}

while getopts "u:d:" opt; do
  case $opt in
    u) USERNAME=$OPTARG ;;
    d) KEY_DIR=$OPTARG ;;
    *) usage ;;
  esac
done

: "${USERNAME:?Missing -u USERNAME}" 
KEY_DIR=${KEY_DIR:-"$HOME/.ssh"}

mkdir -p "$KEY_DIR"
TIMESTAMP=$(date +%Y%m%d%H%M%S)
OLD_PRIV="$KEY_DIR/id_ed25519"
OLD_PUB="${OLD_PRIV}.pub"
BACKUP_DIR="$KEY_DIR/backup"
mkdir -p "$BACKUP_DIR"

if [[ -f "$OLD_PRIV" ]]; then
  mv "$OLD_PRIV" "$BACKUP_DIR/id_ed25519_$TIMESTAMP"
  mv "$OLD_PUB" "$BACKUP_DIR/id_ed25519_$TIMESTAMP.pub"
fi

NEW_PRIV="$KEY_DIR/id_ed25519"
NEW_PUB="${NEW_PRIV}.pub"

if [[ -n "${MOCK_SSH_KEYGEN:-}" ]]; then
  echo "MOCK PRIVATE KEY" > "$NEW_PRIV"
  echo "MOCK PUBLIC KEY" > "$NEW_PUB"
else
  ssh-keygen -t ed25519 -f "$NEW_PRIV" -N "" -q
fi

AUTH_KEYS="$KEY_DIR/authorized_keys"
mkdir -p "$(dirname "$AUTH_KEYS")"
: > "$AUTH_KEYS"
if ! grep -qxF "$(cat "$NEW_PUB")" "$AUTH_KEYS"; then
  cat "$NEW_PUB" >> "$AUTH_KEYS"
fi

echo "New SSH key generated for $USERNAME at $NEW_PRIV"
echo "Public key added to $AUTH_KEYS"
echo "Old keys backed up in $BACKUP_DIR"
