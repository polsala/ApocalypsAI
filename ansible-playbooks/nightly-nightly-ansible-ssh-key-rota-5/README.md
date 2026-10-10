# Nightly Ansible SSH Key Rotator

Utility rotates SSH host keys on inventory hosts, backs up old keys, and updates the control node's known_hosts file. Useful for periodic key rotation in insecure environments.

## Requirements

- Ansible 2.9+
- Access to target hosts via existing SSH keys

## Variables

- `ssh_key_type` (default: rsa) – type of key to generate.
- `ssh_key_bits` (default: 4096) – key size.
- `backup_dir` (default: /etc/ssh/old_keys) – where to store old keys.

## Usage

```bash
ansible-playbook -i inventory.ini src/rotate_ssh_keys.yml
```

## How it works

1. Backup existing host keys.
2. Generate new host keys.
3. Restart sshd.
4. Remove old entries from control node's known_hosts and add new ones.
