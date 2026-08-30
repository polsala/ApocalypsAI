# nightly-ssh-key-rotator

## Overview

`nightly-ssh-key-rotator` is a tiny Bash utility that safely rotates a user's SSH key pair. It backs up the existing `id_rsa` and `id_rsa.pub` files with a timestamped `.bak` suffix, generates a new RSA key pair, and optionally restarts the SSH daemon.

## Features

- **Backup** existing keys with a timestamped `.bak` suffix.
- **Generate** a new 2048‑bit RSA key pair (no passphrase).
- **Idempotent** – running it multiple times will always keep the latest backup.
- **Customizable** SSH directory via the `SSH_DIR` environment variable.
- **No external dependencies** beyond the standard `ssh-keygen` utility.

## Usage

```sh
# Rotate keys in the default $HOME/.ssh directory
./src/rotate_ssh_keys.sh

# Specify a custom .ssh directory
SSH_DIR=/tmp/myssh ./src/rotate_ssh_keys.sh
```

The script prints a short summary of actions performed.

## License

MIT © ApocalypsAI
