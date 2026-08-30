# Nightly SSH Key Rotator

Utility to rotate an SSH host key safely. It backs up the existing key (and its public counterpart) to a timestamp‑stamped backup directory, generates a new key pair using `ssh-keygen`, and prints the locations of the new key and backup.

## Usage
```bash
./rotate_ssh_keys.sh /path/to/ssh_host_key
```
- `<ssh_host_key>` is the **base** path of the key (e.g., `/etc/ssh/ssh_host_rsa_key`).
- The script requires write permission to the directory containing the key.

## What It Does
1. Creates a backup directory named `backup_<YYYYMMDDHHMMSS>` next to the key.
2. Copies any existing private and public key files into that backup.
3. Calls `ssh-keygen -q -N "" -f <key>` to generate a fresh key pair.
4. Prints the paths of the new key and the backup directory.

## Safety
- Existing keys are never overwritten; they are moved to the backup directory first.
- The script exits with a usage message if the required argument is missing.

## Testing
See `tests/test_rotate_ssh_keys.sh` for a deterministic, offline test suite that mocks `ssh-keygen`.
