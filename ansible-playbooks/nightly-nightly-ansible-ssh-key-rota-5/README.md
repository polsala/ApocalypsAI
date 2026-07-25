# Nightly Ansible SSH Key Rotator

Utility that generates a fresh SSH key pair and distributes the public key to all hosts defined in the inventory, replacing old keys. Ideal for periodic key rotation in a post‑apocalyptic bunker.

## Usage

```sh
ansible-playbook -i src/inventory.ini src/rotate_ssh_keys.yml -e "ssh_key_path=~/.ssh/id_rsa_nightly"
```

## Variables

- `ssh_key_path` (string): Path where the new private key will be stored. Public key will be at `${ssh_key_path}.pub`. Defaults to `~/.ssh/id_rsa_nightly`.

## How it works

1. Generates a new RSA key pair if not present.
2. Backs up any existing authorized_keys on the remote host.
3. Replaces authorized_keys with the new public key.
4. Optionally removes the old private key locally.

## Testing

Run the provided test playbook:

```sh
ansible-playbook -i src/inventory.ini tests/test_rotate_ssh_keys.yml --check
```
