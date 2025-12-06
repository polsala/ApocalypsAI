# Nightly Ansible SSH Key Rotator

## Overview

This utility provides an **Ansible playbook** that safely rotates SSH keys on one or more remote hosts. It backs up the existing `authorized_keys`, generates a new RSA key pair, and deploys the new public key to the target machines. Perfect for maintaining secure communications in a post‑apocalyptic environment where key compromise is a constant threat.

## Features

- Backs up existing `authorized_keys` with a timestamped copy.
- Generates a fresh 2048‑bit RSA key pair (customizable).
- Deploys the new public key to the target user’s `authorized_keys`.
- Optional cleanup of the locally generated private key.
- Fully idempotent and safe to run repeatedly.

## Files

- `rotate_ssh_keys.yml` – The main playbook.
- `inventory.ini` – Sample inventory (defaults to localhost for quick testing).
- `tests/run_test.sh` – Simple deterministic test script that runs the playbook in check mode.

## Usage

```bash
# Install Ansible if you haven't already
pip install ansible

# Run the playbook against your inventory
ansible-playbook -i inventory.ini rotate_ssh_keys.yml \
  -e "target_hosts=all cleanup_private_key=true"
```

### Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `target_hosts` | Host pattern to target (e.g., `webservers`, `all`). | `all` |
| `cleanup_private_key` | Remove the locally generated private key after deployment. | `true` |
| `backup_dir` | Directory on the remote host where old `authorized_keys` are stored. | `~/.ssh/backup_keys` |
| `new_key_path` | Path on the remote host for the newly generated key pair. | `~/.ssh/id_rsa_apoc` |

## Testing

A deterministic test is provided in `tests/run_test.sh`. It runs the playbook in **check mode** against the local host to verify syntax and logic without making any changes.

```bash
cd tests
./run_test.sh
```

If the script exits with `Test passed`, the utility is ready to use.

## License

MIT © ApocalypsAI
