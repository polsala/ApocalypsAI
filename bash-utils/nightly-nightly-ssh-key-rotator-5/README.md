# nightly-ssh-key-rotator

**Purpose**: Rotate the SSH host keys on a Unix-like system in a safe, automated way. The script backs up existing keys, generates fresh RSA, ECDSA, and Ed25519 host keys, and can run in a *dry‑run* mode to show what would happen without touching the filesystem.

## Features
- Backs up existing host keys with a timestamped ``.bak`` suffix.
- Generates new RSA (4096‑bit), ECDSA, and Ed25519 keys.
- Supports a custom SSH directory (default ``/etc/ssh``).
- Dry‑run mode (`-n`) for previewing actions.
- Fully self‑contained Bash script – no external dependencies beyond the standard ``ssh-keygen`` utility.

## Installation
```bash
# Clone the repository (or copy the files) and make the script executable
chmod +x utils/bash-utils/nightly-ssh-key-rotator/src/rotate_ssh_keys.sh
```

## Usage
```bash
# Rotate keys in the default location (/etc/ssh)
./src/rotate_ssh_keys.sh

# Specify a custom directory (useful for testing)
./src/rotate_ssh_keys.sh -d /tmp/ssh-test-dir

# Dry‑run to see what would happen without making changes
./src/rotate_ssh_keys.sh -n
```

## Options
- ``-d DIR`` – Path to the SSH directory containing the host keys. Defaults to ``/etc/ssh``.
- ``-n`` – Dry‑run mode. The script prints the actions it *would* take but does not modify any files.

## Safety notes
- The script **must** be run with sufficient privileges to write to the target directory (usually root).
- Existing keys are never overwritten; they are renamed with a ``.bak.<timestamp>`` suffix.
- After rotating keys, you may need to restart the SSH daemon (e.g., ``systemctl restart sshd``) for the new keys to take effect.

## Testing
Run the bundled test suite:
```bash
cd tests
bash test_rotate_ssh_keys.sh
```
All tests should pass, confirming that the script correctly handles dry‑run mode, creates new keys, and backs up old ones.
