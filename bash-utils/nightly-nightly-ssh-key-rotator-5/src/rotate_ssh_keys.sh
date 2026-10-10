#!/usr/bin/env bash

# nightly-ssh-key-rotator
# Rotates SSH host keys, backs up old ones, and updates authorized_keys.
# ---------------------------------------------------------------

set -euo pipefail

# ---------- Configuration (can be overridden via env) ----------
USERNAME="${USERNAME:-root}"
KEY_TYPE="${KEY_TYPE:-rsa}"
KEY_BITS="${KEY_BITS:-4096}"
BACKUP_ROOT="${BACKUP_ROOT:-/var/backups}"
DATE_NOW="${DATE_NOW:-$(date +%s)}"

# Paths (assuming standard OpenSSH layout)
SSH_DIR="/etc/ssh"
HOST_KEY_PREFIX="ssh_host_${KEY_TYPE}_key"
HOST_KEY="${SSH_DIR}/${HOST_KEY_PREFIX}"
HOST_PUB_KEY="${HOST_KEY}.pub"

# ---------- Helper Functions ----------
log() {
  echo "[nightly-ssh-key-rotator] $*"
}

backup_keys() {
  local backup_dir="${BACKUP_ROOT}/ssh-key-backup-${DATE_NOW}"
  mkdir -p "${backup_dir}"
  log "Backing up existing keys to ${backup_dir}"
  for file in "${HOST_KEY}" "${HOST_PUB_KEY}"; do
    if [[ -f "${file}" ]]; then
      cp -a "${file}" "${backup_dir}/"
    fi
  done
}

generate_new_keys() {
  log "Generating new ${KEY_TYPE} host key (${KEY_BITS} bits)"
  if [[ "${KEY_TYPE}" == "rsa" ]]; then
    ssh-keygen -t rsa -b "${KEY_BITS}" -f "${HOST_KEY}" -N "" -q
  else
    ssh-keygen -t "${KEY_TYPE}" -f "${HOST_KEY}" -N "" -q
  fi
}

update_authorized_keys() {
  local auth_file="$(eval echo ~${USERNAME})/.ssh/authorized_keys"
  if [[ ! -f "${auth_file}" ]]; then
    log "No authorized_keys for ${USERNAME}, skipping update."
    return
  fi
  log "Appending new host public key to ${auth_file}"
  cat "${HOST_PUB_KEY}" >> "${auth_file}"
}

restart_sshd() {
  if command -v systemctl >/dev/null 2>&1; then
    log "Restarting sshd via systemctl"
    systemctl restart sshd
  else
    log "Attempting to restart sshd via service command"
    service ssh restart || true
  fi
}

# ---------- Main Execution Flow ----------
log "Starting SSH host key rotation for user '${USERNAME}'"
backup_keys
generate_new_keys
update_authorized_keys
restart_sshd
log "Rotation complete. New host key fingerprint:"
ssh-keygen -lf "${HOST_PUB_KEY}"
