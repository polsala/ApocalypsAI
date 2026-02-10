# nightly-ssh-key-rotator

Utility to generate a fresh SSH key pair for a given user, append the public key to `authorized_keys`, backup the previous `authorized_keys`, and prune old keys.

## Usage

```sh
./src/rotate_ssh_keys.sh -u USER [-d SSH_DIR] [-b BACKUP_DAYS]
```

- `-u USER` : Username for which the key is generated (required).
- `-d SSH_DIR` : Directory containing SSH files (default: `$HOME/.ssh`).
- `-b BACKUP_DAYS` : Number of days to keep old private keys (default: 30).

The script is safe to run repeatedly; it will backup the existing `authorized_keys` each time and only delete private keys older than the specified retention period.

## Testing

Run the test suite:

```sh
cd tests && bash test_rotate_ssh_keys.sh
```

The tests use a mock mode (`SSH_KEYGEN_MOCK=1`) to avoid invoking `ssh-keygen`.
