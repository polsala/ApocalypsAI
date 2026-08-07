# nightly-ssh-key-rotator

**Purpose**: Rotate the SSH host keys on a machine in a reproducible, safe way while keeping a timestamped backup of the previous keys. Perfect for post‑apocalypse security drills or regular hardening.

## Features

- Generates a new RSA host key (`ssh_host_rsa_key` and `.pub`).
- Moves the existing host keys to a backup directory named `ssh-key-backup-<timestamp>`.
- Optionally updates the `authorized_keys` file for a specified user so they can still log in with the new host key fingerprint.
- All actions are logged to stdout for easy piping into CI or cron.

## Requirements

- Bash 4+ (standard on most Linux distributions)
- `ssh-keygen` (part of OpenSSH)
- `sudo` if the script needs to write to `/etc/ssh/` or another privileged location.

## Usage

```bash
# Rotate keys for the default "root" user, backing up to /var/backups/ssh
sudo ./src/rotate_ssh_keys.sh

# Rotate keys for a non‑root user and specify a custom backup directory
sudo USERNAME=alice BACKUP_ROOT=/tmp/ssh-backups ./src/rotate_ssh_keys.sh
```

### Environment Variables

| Variable      | Description                                               | Default               |
|---------------|-----------------------------------------------------------|-----------------------|
| `USERNAME`    | System user whose `authorized_keys` will be updated.     | `root`                |
| `KEY_TYPE`    | Type of key to generate (`rsa`, `ed25519`, etc.).         | `rsa`                 |
| `KEY_BITS`    | Bit length for RSA keys (ignored for other types).        | `4096`                |
| `BACKUP_ROOT` | Directory where backups will be stored.                  | `/var/backups`        |
| `DATE_NOW`    | Timestamp used for naming the backup folder (for testing).| `$(date +%s)`         |

## Safety Notes

- The script **never deletes** old keys; they are moved to a timestamped backup folder.
- If something goes wrong, you can restore the previous keys by copying them back from the backup directory.

## Testing

Run the bundled tests with:

```bash
bash tests/test_rotate_ssh_keys.sh
```

The tests use a temporary directory and mock `date` via the `DATE_NOW` variable, so they are fully deterministic and offline.
