#!/usr/bin/env bash

# nightly-ssh-key-rotator
# Rotates SSH host keys, backing up old ones and creating new placeholders.
# ---------------------------------------------------------------

set -euo pipefail

# Default values
KEY_DIR="/etc/ssh"
BACKUP_DIR=""
DRY_RUN=false

print_help() {
  cat <<'EOF'
Usage: rotate_ssh_keys.sh [options]

Options:
  --key-dir PATH     Directory containing ssh_host_* key files (default: /etc/ssh)
  --backup-dir PATH  Directory to store backups (default: <key-dir>/backup)
  --dry-run          Show actions without making changes
  -h, --help         Show this help message
EOF
}

# Parse arguments
while (( "$#" )); do
  case "$1" in
    --key-dir)
      KEY_DIR="$2"; shift 2;;
    --backup-dir)
      BACKUP_DIR="$2"; shift 2;;
    --dry-run)
      DRY_RUN=true; shift;;
    -h|--help)
      print_help; exit 0;;
    *)
      echo "Error: Unknown argument: $1" >&2; print_help; exit 1;;
  esac
done

# Validate key directory
if [[ ! -d "$KEY_DIR" ]]; then
  echo "Error: Key directory '$KEY_DIR' does not exist." >&2
  exit 1
fi

# Determine backup directory if not supplied
if [[ -z "$BACKUP_DIR" ]]; then
  BACKUP_DIR="$KEY_DIR/backup"
fi

timestamp=$(date +"%Y%m%d%H%M%S")

# Function to perform an action (or echo in dry‑run mode)
run() {
  if $DRY_RUN; then
    echo "[dry‑run] $*"
  else
    eval "$@"
  fi
}

# Ensure backup directory exists
run "mkdir -p \"$BACKUP_DIR\""

# List of typical host key files (private and public)
key_files=(
  ssh_host_rsa_key
  ssh_host_rsa_key.pub
  ssh_host_ecdsa_key
  ssh_host_ecdsa_key.pub
  ssh_host_ed25519_key
  ssh_host_ed25519_key.pub
)

# Rotate each key if it exists
for key in "${key_files[@]}"; do
  src="$KEY_DIR/$key"
  if [[ -e "$src" ]]; then
    backup_name="${key}.${timestamp}.bak"
    run "mv \"$src\" \"$BACKUP_DIR/$backup_name\""
    # Create a new placeholder (empty) key file
    run "touch \"$src\""
    echo "Rotated $key -> $BACKUP_DIR/$backup_name (new placeholder created)"
  else
    echo "Skipping $key (not found)"
  fi
done

# Optional: restart sshd (only if not dry‑run and running as root)
if ! $DRY_RUN && [[ $EUID -eq 0 ]]; then
  if command -v systemctl >/dev/null 2>&1; then
    echo "Restarting sshd via systemctl..."
    run "systemctl restart sshd"
  elif command -v service >/dev/null 2>&1; then
    echo "Restarting sshd via service..."
    run "service ssh restart"
  else
    echo "Warning: Could not determine how to restart sshd. Please restart manually."
  fi
fi

exit 0
