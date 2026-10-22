# Nightly Ansible SSH Key Rotator

Utility to rotate SSH host keys across an inventory. Generates a new RSA key pair, distributes the public key to target hosts, backs up old authorized_keys, and optionally removes the old key.

## Usage

```bash
ansible-playbook -i inventory.ini src/rotate_ssh_keys.yml -e "key_path=~/.ssh/id_rsa_rotated"
```

- `key_path` (optional) path where the new private key will be stored on the control machine.
- `backup_dir` (optional) directory on remote hosts where old authorized_keys will be backed up (default: `~/.ssh/backup`).

## How it works

1. Generate a new RSA key pair locally (or use a provided key).
2. Copy the public key to each host's `~/.ssh/authorized_keys`.
3. Move the previous `authorized_keys` to a backup directory with a timestamp.
4. Optionally remove the old private key from the control machine.

## Requirements

- Ansible 2.9+
- Python 3.6+ (for key generation via `ssh-keygen`)

## Testing

Run the syntax‑check test:

```bash
ansible-playbook -i inventory.ini tests/test_syntax_check.yml
```
