# nightly-ssh-key-rotator

Utility to rotate a user's SSH authorized keys. It generates a new RSA key pair, backs up the existing `authorized_keys`, and installs the new public key.

## Prerequisites
- `ssh-keygen` must be available in the PATH (the script works with the real `ssh-keygen` or a mock for testing).

## Usage
```bash
./rotate_ssh_key.sh <username> [key_comment]
```
- `<username>`: The system username whose SSH keys will be rotated. The script expects the user's home directory at `/home/<username>`.
- `[key_comment]` (optional): Comment to embed in the new public key. Defaults to `rotated-key`.

The script will:
1. Verify that `/home/<username>/.ssh` exists.
2. Back up the current `authorized_keys` to `authorized_keys.bak` (if it exists).
3. Generate a new RSA key pair (`id_rsa_rotated_<timestamp>`).
4. Replace `authorized_keys` with the newly generated public key.

## Example
```bash
# Rotate keys for user "alice" with a custom comment
./rotate_ssh_key.sh alice "alice@$(hostname)"
```

## Safety
- The original `authorized_keys` is preserved as `authorized_keys.bak` in the same directory.
- The generated private key is left in the `.ssh` folder; you may want to secure or delete it after copying the public key to other machines.

## Testing
See `tests/test_rotate_ssh_key.sh` for a deterministic, offline test suite that uses a mock `ssh-keygen`.
