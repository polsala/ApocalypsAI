#!/usr/bin/env bash

# nightly-ssh-key-rotator
# Rotates SSH host keys with backup and optional dry‑run.
# -------------------------------------------------------

set -euo pipefail

# Default values
KEY_DIR="/etc/ssh"
BACKUP_DIR="/var/backups/ssh_keys"
DRY_RUN=false

print_help() {
  cat <<'EOF'
Usage: rotate_ssh_keys.sh [options]

Options:
  --key-dir <path>      Directory containing host keys (default: /etc/ssh)
  --backup-dir <path>   Directory to store backups (default: /var/backups/ssh_keys)
  --dry-run             Show actions without performing them
  -h, --help            Show this help message
EOF
}

# Simple argument parser
while [[ $# -gt 0 ]]; do
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
      echo "Unknown option: $1" >&2; print_help; exit 1;;
  esac
done

# Helper to run a command (or echo it in dry‑run mode)
run_cmd() {
  if $DRY_RUN; then
    echo "[dry‑run] $*"
  else
    echo "[exec] $*"
    "$@"
  fi
}

# Ensure backup directory exists
run_cmd mkdir -p "${BACKUP_DIR}"

# Timestamp for backup naming (overrideable for tests)
TIMESTAMP="${APOCALYPSE_TIMESTAMP:-$(date +%Y%m%d%H%M%S)}"
BACKUP_ARCHIVE="${BACKUP_DIR}/ssh_host_keys_${TIMESTAMP}.bak"

# Backup existing keys
run_cmd mkdir -p "${BACKUP_ARCHIVE}"
run_cmd cp -a "${KEY_DIR}/ssh_host_*" "${BACKUP_ARCHIVE}/"

echo "Backed up existing keys to ${BACKUP_ARCHIVE}"

# Generate new keys
generate_key() {
  local type="$1"
  local file="$2"
  run_cmd ssh-keygen -t "$type" -f "$file" -N "" -q
}

# RSA (2048 bits)
generate_key rsa "${KEY_DIR}/ssh_host_rsa_key"
# ECDSA (256 bits)
generate_key ecdsa "${KEY_DIR}/ssh_host_ecdsa_key"
# Ed25519
generate_key ed25519 "${KEY_DIR}/ssh_host_ed25519_key"

echo "Generated new SSH host keys."

# Restart sshd using systemctl or service
if command -v systemctl >/dev/null 2>&1; then
  run_cmd systemctl restart sshd
elif command -v service >/dev/null 2>&1; then
  run_cmd service ssh restart
else
  echo "Warning: Could not find systemctl or service to restart sshd." >&2
fi

echo "SSH host key rotation complete."
