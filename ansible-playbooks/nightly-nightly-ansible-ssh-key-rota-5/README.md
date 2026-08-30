# Nightly Ansible SSH Key Rotator

Utility that rotates SSH host keys on target machines in a whimsical post‑apocalyptic fashion. It backs up existing keys, generates new RSA keys, and updates `authorized_keys` for a specified user.

## Usage

```bash
ansible-playbook -i src/inventory.ini src/rotate_ssh_keys.yml -e target_user=deployer
```

## Variables

- `target_user` (default: `root`) – user whose `authorized_keys` will be updated.

## What it does

1. Creates a backup of existing SSH host keys.
2. Generates a new RSA key pair.
3. Deploys the new public key to the target user's `authorized_keys`.
4. Optionally removes the old key after confirmation.

## Testing

Run the included test playbook:

```bash
ansible-playbook -i src/inventory.ini tests/test_rotate_ssh_keys.yml
```
