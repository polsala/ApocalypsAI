# Nightly Ansible SSH Key Rotator

Utility that rotates SSH host keys across a fleet of servers using Ansible. Generates a new RSA key pair, distributes the public key, and removes the old key from `authorized_keys`. Ideal for post‑apocalypse security drills.

## Usage

```bash
ansible-playbook -i inventory.ini rotate_ssh_keys.yml
```

## Variables

- `new_key_path` (default: `~/.ssh/id_rsa_rotated`) – path where the new private key will be stored on the control node.
- `target_user` (default: `root`) – user whose `authorized_keys` will be updated.

## Safety

Run with `--check` first to preview changes.
