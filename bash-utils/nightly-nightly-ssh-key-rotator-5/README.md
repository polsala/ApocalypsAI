# nightly-ssh-key-rotator

**Purpose**: Rotate the SSH host keys on a machine (currently only Ed25519) while backing up the previous keys and printing the new fingerprint. Great for post‑apocalypse security drills or regular hardening.

## Features

- Detects existing `ssh_host_ed25519_key` and `ssh_host_ed25519_key.pub`.
- Moves old keys to a user‑specified backup directory with a timestamp.
- Generates a fresh Ed25519 host key using `ssh-keygen`.
- Outputs the new key's SHA256 fingerprint for easy verification.

## Installation

```bash
# Clone the repository (or copy the files into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/bash-utils/nightly-ssh-key-rotator
chmod +x src/rotate_ssh_keys.sh
```

## Usage

```bash
./src/rotate_ssh_keys.sh -d /etc/ssh -b /var/backups/ssh_keys
```

- `-d <dir>`: Directory where the host keys live (default: `/etc/ssh`).
- `-b <dir>`: Optional backup directory. If omitted, a temporary backup directory is created under `/tmp/ssh_key_backup_<timestamp>`.

The script prints the location of the backup and the new fingerprint, e.g.:

```
Backup created at /var/backups/ssh_keys/backup_20241012_150423
New host key fingerprint (SHA256): AAAAB3NzaC1yc2EAAAADAQABAAABAQC...
```

## Safety notes

- The script **must be run as root** (or a user with write permission to the key directory).
- It only handles Ed25519 keys; other key types are ignored.
- Always verify the new fingerprint with your clients after rotation.

## Testing

Run the bundled test suite (offline, no real `ssh-keygen` required):

```bash
cd tests
bash test_rotate_ssh_keys.sh
```

All tests should pass, confirming that backup, generation, and fingerprint reporting work as expected.
