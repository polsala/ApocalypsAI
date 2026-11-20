# Nightly SSH Key Rotator

Utility to rotate SSH keys across all hosts in an inventory. It generates a new RSA key pair on the control node, backs up existing authorized_keys, distributes the new public key, and leaves a hook for optional old‑key cleanup.

## Features

- Generates a 4096‑bit RSA key pair if it does not already exist.
- Backs up the current `authorized_keys` with a timestamped copy.
- Deploys the newly generated public key to each host's `authorized_keys`.
- Fully idempotent – re‑running the playbook will not recreate keys.

## Requirements

- Ansible 2.9+ installed on the control node.
- `openssh-client` package available on target hosts (the playbook ensures this).

## Usage

```bash
ansible-playbook -i inventory.ini src/rotate_ssh_keys.yml \
  --extra-vars "key_name=nightly_key"
```

- `key_name` (optional) – Base name for the key files. Defaults to `nightly_key`.
- The keys are stored under `/etc/ssh/{{ key_name }}` on the control node.

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `key_name` | `nightly_key` | Base filename for the generated key pair. |
| `key_path` | `/etc/ssh/{{ key_name }}` | Full path (without extension) where the key pair will be stored. |

## Cleanup

The playbook leaves the old `authorized_keys` file backed up as
`~/.ssh/authorized_keys.bak_<timestamp>`. You can manually prune these backups when desired.

## Testing

Run the bundled test with:

```bash
ansible-playbook -i localhost, tests/test_rotate_ssh_keys.yml
```

The test runs the playbook in `--check` mode against localhost and asserts successful execution.
