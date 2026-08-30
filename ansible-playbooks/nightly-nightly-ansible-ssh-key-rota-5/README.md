# Nightly Ansible SSH Key Rotator

Utility to rotate SSH keys for a given user across target hosts. Generates a fresh RSA key pair, distributes the public key to `authorized_keys`, and removes the previous key entry. Safe to run in check mode for dry‑run.

## Usage

```bash
ansible-playbook -i src/inventory.ini src/rotate_ssh_keys.yml -e "target_user=deploy"
```

Add `--check` for a dry‑run.

## Variables

- `target_user` (required): system user whose SSH keys will be rotated.
- `key_path` (optional): path to store generated private key on the control node (default: `{{ playbook_dir }}/{{ target_user }}_id_rsa`).

## How it works

1. Generate a new RSA key pair using `openssh_keypair`.
2. Ensure the public key is present in the user's `~/.ssh/authorized_keys`.
3. Remove any previous key entries matching the comment `rotated-key-{{ target_user }}`.

## Testing

Run the provided test suite:

```bash
python -m unittest discover -s tests
```
