# Nightly SSH Key Rotator

## Overview
`nightly-ssh-key-rotator` is a whimsical yet practical Ansible playbook that automates the rotation of SSH host keys across a fleet of servers.  In a post‑apocalyptic setting, keeping your bunker’s SSH keys fresh prevents stale credentials from becoming a security liability.

## Features
- Generates new RSA host keys (`ssh_host_rsa_key` and `ssh_host_ed25519_key`).
- Backs up existing host keys with a timestamped copy.
- Restarts the SSH daemon to apply the new keys.
- Runs in **check mode** by default for safe dry‑runs.

## Requirements
- Ansible 2.9+ installed on the control node.
- Password‑less sudo or appropriate privilege escalation on target hosts.

## Inventory
Create an inventory file (`inventory.ini`) listing the hosts you want to rotate keys on.  See the provided example in `src/inventory.ini`.

## Usage
```bash
# Dry‑run (check mode)
ansible-playbook -i src/inventory.ini src/rotate_ssh_keys.yml --check

# Actual rotation
ansible-playbook -i src/inventory.ini src/rotate_ssh_keys.yml
```

## Testing
Run the bundled test playbook to ensure the rotation playbook executes without errors:
```bash
ansible-playbook -i src/inventory.ini tests/test_rotate_ssh_keys.yml
```
The test runs the rotation playbook in check mode and asserts a zero exit code.

## License
MIT © ApocalypsAI
