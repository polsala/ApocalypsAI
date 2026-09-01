# Nightly Ansible SSH Key Rotator

Utility to rotate SSH keys on remote hosts using Ansible. Generates a new key pair, distributes the public key, and removes the previous key from `authorized_keys`.

## Usage

```bash
ansible-playbook -i src/inventory.ini src/rotate_ssh_keys.yml -e "new_key_path=~/.ssh/id_rsa_new old_key_fingerprint=SHA256:oldfingerprint"
```

## Variables

- `new_key_path` (required): Path where the new private key will be stored locally.
- `old_key_fingerprint` (optional): Fingerprint of the old key to be removed from `authorized_keys`.

## How it works

1. Ensures `ssh-keygen` is available.
2. Generates a new RSA key pair if it does not already exist.
3. Copies the public key to each host's `~/.ssh/authorized_keys`.
4. Optionally removes any line in `authorized_keys` that contains the provided fingerprint.

## Testing

Run the test suite with:

```bash
pytest tests/test_rotate.py
```
