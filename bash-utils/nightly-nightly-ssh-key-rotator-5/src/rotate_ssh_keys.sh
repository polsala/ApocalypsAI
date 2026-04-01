#!/usr/bin/env bash
set -euo pipefail

# Optional override for deterministic timestamps (used by tests)
now="${DATE_OVERRIDE:-$(date +%Y%m%d%H%M%S)}"

ssh_dir="${HOME}/.ssh"
backup_dir="${ssh_dir}/backup_${now}"

mkdir -p "${backup_dir}"

# If an existing key pair is present, back it up
if [[ -f "${ssh_dir}/id_rsa" && -f "${ssh_dir}/id_rsa.pub" ]]; then
  cp "${ssh_dir}/id_rsa" "${backup_dir}/id_rsa"
  cp "${ssh_dir}/id_rsa.pub" "${backup_dir}/id_rsa.pub"
fi

# Generate a fresh RSA key pair (2048 bits, no passphrase)
ssh-keygen -t rsa -b 2048 -f "${ssh_dir}/id_rsa" -N "" -q

# Whimsical post‑apocalyptic quotes
quotes=(
  "The night is dark, but your keys are bright."
  "Rotating keys, like rotating the earth—endless."
  "Even the wasteland respects a fresh key pair."
  "Secure today, survive tomorrow."
)

# Pick a random quote
printf "%s\n" "${quotes[RANDOM % ${#quotes[@]}]}"
