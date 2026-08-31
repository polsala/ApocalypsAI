# SSH Key Rotator Ansible Playbook

Utility to rotate SSH keys on target hosts. Generates a new RSA key pair, distributes the public key to `authorized_keys`, and removes the old key fingerprint.

## Usage

```bash
ansible-playbook -i src/inventory.ini src/rotate_ssh_keys.yml -e "old_fingerprint=AA:BB:CC:DD:EE:FF:..."
```

## Variables

- `old_fingerprint` (required): fingerprint of the key to remove.
- `key_path` (optional, default: `~/.ssh/id_rsa`): path where new key will be stored.

## How it works

1. Generate a new RSA key pair using `openssh_keypair`.
2. Append the public key to `~/.ssh/authorized_keys` on each host.
3. Remove any line in `authorized_keys` matching the old fingerprint.

## Testing

Run the test playbook in check mode:

```bash
ansible-playbook -i src/inventory.ini tests/test_rotate_ssh_keys.yml
```

Now rotate keys (dry‑run):

```bash
ansible-playbook -i src/inventory.ini src/rotate_ssh_keys.yml -e "old_fingerprint=..." --check
```
