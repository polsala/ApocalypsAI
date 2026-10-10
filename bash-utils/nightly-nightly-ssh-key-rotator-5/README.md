# nightly-ssh-key-rotator

**Purpose**: Rotate the SSH host keys on a Unix‑like system in a safe, repeatable way. The script backs up existing keys, generates fresh RSA, ECDSA and Ed25519 host keys, and restarts the SSH daemon. A `--dry-run` flag lets you preview actions without touching the filesystem.

## Features
- Automatic backup of current host keys (timestamped archive).
- Generation of RSA, ECDSA and Ed25519 keys using `ssh-keygen`.
- Detects whether to use `systemctl` or `service` to restart `sshd`.
- Fully configurable key directory and backup location.
- Dry‑run mode for safe preview.

## Installation
```bash
# Clone the repository (or copy the files) and make the script executable
chmod +x src/rotate_ssh_keys.sh
```

## Usage
```bash
./src/rotate_ssh_keys.sh [options]
```

### Options
| Flag | Description |
|------|-------------|
| `--key-dir <path>` | Directory containing the host keys (default: `/etc/ssh`). |
| `--backup-dir <path>` | Directory where backups will be stored (default: `/var/backups/ssh_keys`). |
| `--dry-run` | Show what would be done without making changes. |
| `-h`, `--help` | Show help message. |

### Example
```bash
# Rotate keys, backing up to /tmp/ssh_backup
./src/rotate_ssh_keys.sh --key-dir /tmp/ssh_test --backup-dir /tmp/ssh_backup
```

## Testing
The utility includes a deterministic Bash test suite located in `tests/`. Run it with:
```bash
bash tests/test_rotate_ssh_keys.sh
```
All tests should pass on any POSIX‑compatible shell.

## License
MIT © ApocalypsAI
