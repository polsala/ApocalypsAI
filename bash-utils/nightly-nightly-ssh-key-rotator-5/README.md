# nightly-ssh-key-rotator

Utility to safely rotate a user's SSH keys. Generates a new ed25519 key pair, backs up the existing authorized_keys, and installs the new public key. Ideal for post‑apocalyptic key hygiene.

## Usage

```sh
./rotate_ssh_keys.sh [-u username] [-d ssh_dir]
```

- `-u` : username whose `.ssh` directory to operate on (default: current user)
- `-d` : path to the `.ssh` directory (default: `$HOME/.ssh`)

The script will:

1. Generate a new ed25519 key pair (`id_ed25519_rotated` and `.pub`).
2. Backup existing `authorized_keys` to `authorized_keys.bak.<timestamp>`.
3. Replace `authorized_keys` with the new public key.

## Safety

- The script never deletes old keys; they are kept in the backup file.
- All operations are logged to stdout.

## Example

```sh
./rotate_ssh_keys.sh -u alice -d /home/alice/.ssh
```
