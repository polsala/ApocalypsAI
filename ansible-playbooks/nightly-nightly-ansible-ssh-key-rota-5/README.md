# SSH Key Rotator

Utility to rotate SSH host keys across an inventory. It backs up existing keys, generates new RSA keys, places them, and restarts sshd. Useful for post‑apocalypse security hygiene.

## Requirements

- Ansible 2.9+
- OpenSSL available on target hosts

## Usage

```bash
ansible-playbook -i inventory.ini src/rotate_ssh_keys.yml -e "ssh_key_dir=/etc/ssh"
```

## Variables

- `ssh_key_dir` (default: `/etc/ssh`) – directory where host keys reside.
- `ssh_key_type` (default: `rsa`) – type of key to generate.
- `ssh_key_bits` (default: `4096`) – key size.

## What it does

1. Backs up existing host keys to `<ssh_key_dir>/backup_<timestamp>/`.
2. Generates new host keys.
3. Restarts the SSH service.
