# Nightly Ansible SSH Key Rotator

## Overview
This utility provides an Ansible playbook that rotates SSH key pairs on target hosts. It backs up existing keys, generates a fresh RSA key pair, and ensures the new public key is present in each host's `authorized_keys`. Ideal for post‑apocalyptic vaults that need fresh keys every night.

## Files
- `src/playbook.yml` – The main playbook.
- `src/inventory.ini` – Simple inventory (defaults to localhost).
- `tests/test_ssh_key_rotator.py` – Pytest that runs the playbook and checks key creation.

## Usage
```bash
cd ansible-playbooks/nightly-ansible-ssh-key-rotator
ansible-playbook -i src/inventory.ini src/playbook.yml
```

The generated keys are stored under `ssh_keys/` in the playbook directory.

## License
MIT
