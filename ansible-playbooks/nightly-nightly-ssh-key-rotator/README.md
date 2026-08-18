# Nightly SSH Key Rotator

## Overview
A whimsical yet practical Ansible playbook that backs up the current SSH host keys on target machines, generates brand‑new keys, restarts the SSH daemon, and sets a fact indicating a successful rotation. Ideal for rotating credentials in a post‑apocalyptic bunker or any environment that values fresh cryptographic material.

## Files
- `inventory.ini` – Simple inventory targeting the local host (can be expanded).
- `src/rotate_ssh_keys.yml` – The main playbook.
- `tests/test_rotate_ssh_keys.yml` – An offline test that imports the playbook and asserts the rotation flag.

## Usage
```bash
# Run the rotation against your inventory
ansible-playbook -i inventory.ini src/rotate_ssh_keys.yml
```

## Testing
The test playbook runs the rotation in a safe, idempotent way and then checks that the `ssh_key_rotated` fact is set to `true`.
```bash
ansible-playbook -i inventory.ini tests/test_rotate_ssh_keys.yml
```

## Notes
- The playbook uses `become: true` because key generation and service restart require root privileges.
- Existing keys are backed up with a `.bak` suffix before being replaced.
- The playbook is written to be idempotent; running it multiple times will not recreate keys that already exist.
