# nightly-ssh-key-rotator

Utility to rotate SSH keys for a user across many remote hosts.

## Overview

Generates a fresh RSA key pair, backs up the existing `~/.ssh/id_rsa` and `id_rsa.pub` on each host, installs the new public key into `~/.ssh/authorized_keys`, and optionally removes the old private key.

## Usage

```sh
./src/rotate_ssh_keys.sh hosts.txt username
```

- `hosts.txt` – newline‑separated list of hostnames or IPs.
- `username` – remote user whose keys will be rotated.

The script will:

1. Create a temporary key pair in `/tmp/ssh_key_rotator_<pid>`.
2. For each host:
   * Backup existing keys to `~/.ssh/backup_<timestamp>`.
   * Append the new public key to `~/.ssh/authorized_keys`.
3. Print a summary.

## Prerequisites

- `ssh` and `scp` available.
- Passwordless SSH (or SSH agent) for the target user, or you will be prompted.
- Local machine must have write permission to `/tmp`.

## Safety

The script never deletes existing keys; it only backs them up. Review the backup directory on each host if you need to revert.

## Testing

Run the bundled tests with:

```sh
bash tests/test_rotate_ssh_keys.sh
```

They use mocked `ssh`/`scp` commands and do not touch real hosts.
