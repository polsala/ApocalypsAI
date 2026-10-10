# SSH Key Rotator

Utility to rotate SSH host keys on target machines via Ansible. Generates new RSA/ECDSA keys, restarts sshd, and updates the control node's known_hosts.

## Usage

```sh
ansible-playbook -i inventory.ini src/rotate_ssh_keys.yml
```

## Variables

- `ssh_key_type` (default: rsa)
- `ssh_key_bits` (default: 4096)

## How it works

1. Remove existing host keys.
2. Generate new keys.
3. Restart sshd.
4. Fetch the new public key and add to known_hosts.
