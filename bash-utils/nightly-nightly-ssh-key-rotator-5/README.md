# nightly-ssh-key-rotator

Utility to rotate a user's SSH ed25519 key pair, backup old keys, and update authorized_keys. Useful for periodic key rotation in a post‑apocalyptic bunker.

## Usage

```sh
./src/rotate_ssh_keys.sh -u USERNAME [-d KEY_DIR]
```

- `-u USERNAME` : the account name (for logging only).
- `-d KEY_DIR` : directory containing the keys (default: `$HOME/.ssh`).

The script will:

1. Move existing `id_ed25519` and `id_ed25519.pub` to `KEY_DIR/backup/` with a timestamp.
2. Generate a new ed25519 key pair (or mock keys in test mode).
3. Append the new public key to `authorized_keys` if not already present.
4. Print a summary.

## Testing

Run the test suite:

```sh
bash tests/test_rotate_ssh_keys.sh
```

The tests use a temporary HOME directory and mock `ssh-keygen` via the `MOCK_SSH_KEYGEN` env var.
