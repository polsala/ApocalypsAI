# SSH Key Rotator

This Ansible playbook creates a new SSH key pair, copies the public key to the `authorized_keys` of each target host, and removes the previous key. It is ideal for rotating keys across a fleet of servers in a whimsical, post‑apocalypse setting.

## Requirements

- Ansible 2.9+
- Python 3.8+ on control node

## Usage

```bash
ansible-playbook -i src/inventory.ini src/rotate_ssh_keys.yml -e "key_name=postapoc_key"
```

The playbook will:

1. Generate a new RSA key pair (if not existing) under `~/.ssh/{{ key_name }}`.
2. Distribute the public key to each host's `~/.ssh/authorized_keys`.
3. Optionally delete the old key (set `remove_old=true`).

## Variables

- `key_name` (default: `postapoc_key`) – base name for the key files.
- `remove_old` (default: `true`) – whether to delete the previous key from hosts.

## License

MIT
