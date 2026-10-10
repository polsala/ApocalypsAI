# nightly-ssh-key-rotator

Utility to rotate a user's SSH key pair across multiple remote hosts. Generates a fresh ed25519 key, backs up the old key, and distributes the new public key to the specified hosts using `ssh-copy-id`. Ideal for periodic key rotation in small fleets.

## Prerequisites

- Bash 4+
- `ssh-keygen` and `ssh-copy-id` available in `PATH`
- Passwordless SSH access (or SSH agent) for the target user to each host

## Usage

```bash
./src/rotate_ssh_keys.sh -u USERNAME -h hosts.txt -d ~/.ssh
```

- `-u USERNAME` – remote user name
- `-h hosts.txt` – file with one hostname per line
- `-d KEYDIR` – directory where the key pair resides (default: `~/.ssh`)

The script will:

1. Backup existing `id_ed25519` (if present) to `id_ed25519_old_<timestamp>`.
2. Generate a new `id_ed25519_new` key pair.
3. Replace the old key with the new one.
4. Distribute the new public key to each host.

## Safety

The script never deletes old keys; they are renamed with a timestamp for manual review.
