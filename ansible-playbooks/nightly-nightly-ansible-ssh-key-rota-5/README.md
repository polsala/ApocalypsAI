# nightly-ansible-ssh-key-rotator

Utility to rotate SSH host keys on remote servers using Ansible. Generates a fresh RSA key pair, updates `authorized_keys`, and removes the old key. Useful for post‑apocalypse security drills.

## Usage

```bash
ansible-playbook -i src/inventory.ini src/rotate_ssh_keys.yml -e "target=yourhost"
```

## Variables

- `target` – host to rotate keys on (default: `localhost`)
- `ssh_key_path` – path to store the new key (default: `~/.ssh/id_rsa_rotated`)

## How it works

1. Generate a new RSA key pair.
2. Append the new public key to `~/.ssh/authorized_keys`.
3. Remove the previous public key entry.
4. Optionally backup the old key.

## Testing

Run the test playbook:

```bash
ansible-playbook -i src/inventory.ini tests/test_rotate_ssh_keys.yml
```
