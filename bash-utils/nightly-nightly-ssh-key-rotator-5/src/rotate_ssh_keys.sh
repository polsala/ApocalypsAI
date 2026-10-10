#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: $(basename "$0") -u USERNAME -h HOSTFILE [-d KEYDIR]

  -u USERNAME   Remote username for ssh-copy-id
  -h HOSTFILE   File containing hostnames (one per line)
  -d KEYDIR     Directory where the key pair lives (default: ~/.ssh)
EOF
  exit 1
}

# Default values
KEYDIR="$HOME/.ssh"

while getopts ":u:h:d:" opt; do
  case $opt in
    u) USERNAME="$OPTARG";;
    h) HOSTFILE="$OPTARG";;
    d) KEYDIR="$OPTARG";;
    \?) echo "Invalid option: -$OPTARG" >&2; usage;;
    :) echo "Option -$OPTARG requires an argument." >&2; usage;;
  esac
done

# Verify required arguments
if [[ -z "${USERNAME:-}" || -z "${HOSTFILE:-}" ]]; then
  echo "Both -u and -h are required." >&2
  usage
fi

if [[ ! -f "$HOSTFILE" ]]; then
  echo "Host file '$HOSTFILE' does not exist." >&2
  exit 1
fi

# Ensure KEYDIR exists
mkdir -p "$KEYDIR"

OLD_KEY="$KEYDIR/id_ed25519"
NEW_KEY="$KEYDIR/id_ed25519_new"
NEW_PUB="$NEW_KEY.pub"

# Backup old key if it exists
if [[ -f "$OLD_KEY" ]]; then
  TIMESTAMP=$(date +%s)
  BACKUP="$KEYDIR/id_ed25519_old_$TIMESTAMP"
  mv "$OLD_KEY" "$BACKUP"
  mv "$OLD_KEY.pub" "$BACKUP.pub"
  echo "Backed up existing key to $BACKUP"
fi

# Generate new key pair (no passphrase)
ssh-keygen -t ed25519 -f "$NEW_KEY" -N "" -q

# Replace old key with new one
mv "$NEW_KEY" "$OLD_KEY"
mv "$NEW_PUB" "$OLD_KEY.pub"

echo "Generated new key pair at $OLD_KEY"

# Distribute the new public key to each host
while IFS= read -r host || [[ -n "$host" ]]; do
  # Skip empty lines and comments
  [[ -z "$host" || "$host" =~ ^# ]] && continue
  echo "Copying key to $host..."
  ssh-copy-id -i "$OLD_KEY.pub" "$USERNAME@$host"
done < "$HOSTFILE"

echo "Key rotation complete."
