# nightly-ssh-key-rotator

Utility to safely rotate SSH keys for a user. It backs up existing keys, generates a new ed25519 key pair, and replaces the authorized_keys file with the new public key.

## Usage

```sh
./rotate_ssh_keys.sh [-u username] [-d ssh_dir]
```

- `-u` : user whose keys are being rotated (default: current user)
- `-d` : directory containing the .ssh files (default: $HOME/.ssh)

The script creates a `backup/` subdirectory inside the ssh directory and moves any existing `id_*` private/public keys there before generating a fresh `id_ed25519` pair.

## Example

```sh
./rotate_ssh_keys.sh -u alice -d /home/alice/.ssh
```

## Safety

The script never deletes old keys; they are moved to `backup/` for manual review.
