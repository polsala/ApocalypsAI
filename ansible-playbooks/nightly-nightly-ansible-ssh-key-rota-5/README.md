# nightly-ansible-ssh-key-rotator

## Overview

`nightly-ansible-ssh-key-rotator` is a lightweight **Ansible** playbook that:

1. **Backs up** existing SSH host keys.
2. **Generates fresh** RSA, ECDSA, and Ed25519 host keys.
3. **Restarts** the SSH service so the new keys take effect.
4. **Collects** the new RSA fingerprint.
5. **Updates** the control node's `~/.ssh/known_hosts` file for each target host.

Rotating host keys periodically reduces the risk of long‑term key compromise – a whimsical yet practical security hygiene task for any fleet of servers.

## Files

- `src/rotate_ssh_keys.yml` – The core task file (no play header, intended to be imported).
- `src/inventory.ini` – Sample inventory with a placeholder host.
- `tests/test_rotate_ssh_keys.yml` – Deterministic test playbook that runs the rotation against a temporary directory on `localhost`.

## Usage

```bash
# Install Ansible if you haven't already
pip install ansible

# Run the rotation against your inventory
ansible-playbook -i src/inventory.ini src/rotate_ssh_keys.yml
```

### Running the test suite

The repository’s CI executes the test playbook directly:

```bash
ansible-playbook -i src/inventory.ini tests/test_rotate_ssh_keys.yml
```

The test creates a temporary directory under `/tmp/ssh_test`, performs the rotation there (so your real `/etc/ssh` is untouched), and asserts that the `ssh_key_rotated` fact is set to `true`.

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ssh_key_dir` | `/etc/ssh` | Directory where host keys live. Override in tests or custom runs to point at a sandbox location. |

## License

MIT – see the repository LICENSE file.
