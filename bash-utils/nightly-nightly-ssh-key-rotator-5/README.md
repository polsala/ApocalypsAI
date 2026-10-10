# nightly-ssh-key-rotator

**Purpose**: Rotate a specified user’s SSH key pair, archive the old keys, and ensure the new public key is added to the user’s `authorized_keys` file.  Perfect for keeping your keys fresh without manual hassle – the apocalypse may be coming, but your SSH security stays up‑to‑date!

## Features

- Generates a new RSA key pair (2048‑bit by default).
- Moves the previous private key to a backup directory with a timestamp.
- Appends the new public key to `~/.ssh/authorized_keys` if it isn’t already present.
- Works entirely with standard Unix tools (`ssh-keygen`, `mv`, `cat`).
- Fully testable with a mock filesystem – no real keys are touched during CI.

## Installation

```bash
# Clone the repository (or copy the script) into your utilities folder
mkdir -p ~/utils/ssh-key-rotator && cd ~/utils/ssh-key-rotator
# Save the script
curl -O https://raw.githubusercontent.com/your-repo/main/bash-utils/nightly-ssh-key-rotator/src/rotate_ssh_keys.sh
chmod +x rotate_ssh_keys.sh
```

## Usage

```bash
./rotate_ssh_keys.sh \
    --user <username> \
    --key-dir <path-to-ssh-dir> \
    --backup-dir <path-to-backup-dir>
```

- `--user` (required): The system user whose keys should be rotated.
- `--key-dir` (optional, default: `~/.ssh`): Directory containing the current `id_rsa` and `id_rsa.pub`.
- `--backup-dir` (optional, default: `~/.ssh/key_backups`): Where the old private key will be stored.

## Example

```bash
# Rotate keys for the current user, using defaults
./rotate_ssh_keys.sh --user $(whoami)
```

## Testing

The utility includes a deterministic test suite that creates a temporary home directory, runs the script, and verifies:

1. A new key pair is created.
2. The old private key is moved to the backup location.
3. `authorized_keys` now contains the new public key.

Run the tests with:

```bash
cd tests && bash test_rotate_ssh_keys.sh
```

## Safety Notes

- The script **never deletes** old keys; they are archived with a timestamp.
- Ensure the backup directory is secured (proper permissions) to avoid leaking old private keys.
- This utility is intended for Unix‑like systems with `ssh-keygen` available.

---

*Created by the ApocalypsAI Nightly Integrator – because even in the end times, good security practices matter.*
