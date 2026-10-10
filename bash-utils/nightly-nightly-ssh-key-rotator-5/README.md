# nightly-ssh-key-rotator

Utility to rotate a user's SSH private key, backing up the old key with a timestamp and generating a new RSA key pair. Useful for regular key rotation in a post‑apocalyptic secure environment.

## Usage

```sh
./src/rotate_ssh_keys.sh <key_path>
```

- `<key_path>`: Path to the existing private key (e.g., `~/.ssh/id_rsa`). The script will backup the existing key to `<key_path>.bak.<timestamp>` and generate a new key at the same location.

## How it works

1. Verify the key file exists.
2. Create a timestamped backup of the private key and its public counterpart.
3. Run `ssh-keygen` to generate a new RSA key pair (2048 bits) without a passphrase.
4. Print the location of the new keys.

## Requirements

- `ssh-keygen` (usually provided by OpenSSH)
- Bash 4+
