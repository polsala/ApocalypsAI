# nightly-ssh-key-rotator

**Purpose**: Quickly rotate SSH host keys on a server (or in a test directory) while preserving the old keys in a backup location.  This is handy for security drills, CI environments, or just for fun.

## Features
- Backs up existing `ssh_host_*` key files with a timestamp.
- Creates new empty placeholder key files (you can replace the placeholder generation with `ssh-keygen` if desired).
- Supports custom key directory and backup directory.
- Dry‑run mode to see what would happen without touching the filesystem.

## Installation
```bash
# Clone the repository (or copy the utility folder) and make the script executable
chmod +x src/rotate_ssh_keys.sh
```

## Usage
```bash
# Rotate keys in the default /etc/ssh directory (requires sudo)
sudo src/rotate_ssh_keys.sh

# Rotate keys in a custom directory (useful for testing)
src/rotate_ssh_keys.sh --key-dir /tmp/ssh_test --backup-dir /tmp/ssh_backup

# Dry‑run – show actions without making changes
src/rotate_ssh_keys.sh --dry-run
```

## Options
- `--key-dir PATH`   : Directory containing the `ssh_host_*` key files (default: `/etc/ssh`).
- `--backup-dir PATH`: Directory where old keys will be stored (default: `<key-dir>/backup`).
- `--dry-run`        : Print actions without performing them.
- `-h, --help`       : Show help message.

## Testing
Run the bundled test suite:
```bash
bash tests/test_rotate_ssh_keys.sh
```
The test creates a temporary key directory, runs the rotator, and verifies that:
1. Old keys are moved to the backup location.
2. New placeholder key files exist.
3. No errors are reported.

## License
MIT © ApocalypsAI community
