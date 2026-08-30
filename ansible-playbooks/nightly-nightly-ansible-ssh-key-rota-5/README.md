# nightly-ansible-ssh-key-rotator

## Overview

`nightly-ansible-ssh-key-rotator` is a whimsical yet practical Ansible playbook that rotates the SSH host keys on all target machines.  It:

1. **Backs up** the existing host key to a timestamped file.
2. **Generates** a fresh ECDSA host key.
3. **Restarts** the SSH daemon so the new key takes effect.

Think of it as a post‑apocalyptic safe‑house routine – every night the doors (keys) get a fresh lock, and the old one is tucked away for later reference.

## Files

- `src/rotate_ssh_keys.yml` – The main playbook.
- `src/inventory.ini` – Minimal inventory (defaults to `localhost`).
- `tests/test_rotate_ssh_keys.yml` – Simple integration test that runs the playbook in check mode.

## Usage

```bash
# Install Ansible if you haven't already
pip install ansible

# Run the playbook against your inventory
ansible-playbook -i src/inventory.ini src/rotate_ssh_keys.yml
```

You can also run the bundled test to ensure the playbook parses correctly:

```bash
ansible-playbook -i src/inventory.ini tests/test_rotate_ssh_keys.yml
```

## Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ssh_key_path` | Path to the host key that will be rotated. | `/etc/ssh/ssh_host_ecdsa_key` |
| `backup_dir` | Directory where old keys are stored. | `/etc/ssh/backup_keys` |

## Safety notes

- The playbook **does not** delete old keys; they are stored with a timestamp.
- It runs with `become: true`, so you need sudo privileges on the target hosts.
- On macOS (Darwin) the service restart step is skipped because the service name differs.

---

*Created by the ApocalypsAI Nightly Integrator.*
