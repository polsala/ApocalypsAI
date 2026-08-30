# nightly-ansible-ssh-key-rotator

Utility to rotate SSH keys on a set of hosts via Ansible. Generates a fresh RSA key pair, distributes the public key to target users, and removes the previous key from `authorized_keys`. Helpful for periodic key hygiene in a post‑apocalyptic bunker.

## Prerequisites

- Ansible 2.9+ installed on the control node.
- SSH access to target hosts with a user that can manage its own `~/.ssh/authorized_keys`.
- Python `cryptography` library (used by `openssh_keypair`).

## Usage

```bash
ansible-playbook -i src/inventory.ini src/rotate_ssh_keys.yml \
  -e "target_user=deployer old_key_fingerprint=SHA256:abc123"
```

- `target_user` – user whose `authorized_keys` will be updated.
- `old_key_fingerprint` – fingerprint of the key to be removed (optional; if omitted, only adds the new key).

The playbook runs in `check` mode by default; remove `--check` to apply changes.

## Files

- `src/rotate_ssh_keys.yml` – main playbook.
- `src/inventory.ini` – sample inventory.
- `tests/test_rotate_ssh_keys.yml` – deterministic test using mock hosts.
