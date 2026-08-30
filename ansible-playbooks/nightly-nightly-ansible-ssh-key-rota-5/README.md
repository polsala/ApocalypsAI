# SSH Key Rotator

Utility to rotate SSH host keys on a set of servers via Ansible. It backs up existing keys, generates new ones, and updates the local known_hosts file. Perfect for post‑apocalypse security drills.

## Usage

```bash
ansible-playbook -i src/inventory.ini src/rotate_ssh_keys.yml
```

## Variables

- `ssh_key_type` (default: `rsa`) – type of key to generate.
- `ssh_key_bits` (default: `4096`) – key size.
- `backup_dir` (default: `/etc/ssh/backup`) – directory where old keys are stored.

## What it does

1. Copies existing `/etc/ssh/ssh_host_*_key*` to the backup directory with a timestamp.
2. Generates new host keys with `ssh-keygen`.
3. Restarts the SSH daemon.
4. Updates the control node's `~/.ssh/known_hosts` for the target hosts.
