# Nightly SSH Key Rotator

Utility that rotates SSH host keys on target machines using Ansible. Useful for keeping secure communications fresh in a post‑apocalyptic environment.

## Files

- `src/rotate_keys.yml` – Main playbook.
- `inventory.ini` – Sample inventory.
- `vars/main.yml` – Default variables.
- `tests/test_rotate_keys.yml` – Simple test playbook.

## Usage

```bash
ansible-playbook -i inventory.ini src/rotate_keys.yml -e @vars/main.yml
```

The playbook backs up existing host keys, generates new ones, and restarts the SSH service.

## Variables

- `ssh_key_type` (default: `ed25519`) – Type of key to generate.
- `ssh_key_bits` (default: `4096`) – Bits for RSA keys (ignored for ed25519).

## Safety

The playbook creates backups in `/etc/ssh/backup_keys/` before overwriting.
