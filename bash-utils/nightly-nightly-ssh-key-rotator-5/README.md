# nightly-ssh-key-rotator

Utility to rotate SSH host keys on a Unix system. It backs up existing keys, generates new ones with `ssh-keygen`, and (optionally) restarts the `sshd` service. Useful for periodic key rotation policies.

## Usage

```sh
./rotate_ssh_keys.sh [-t rsa|ed25519] [-d /etc/ssh] [-r]
```

- `-t` key type (default `ed25519`)
- `-d` directory containing host keys (default `/etc/ssh`)
- `-r` actually restart `sshd`; without it, the script only prepares keys.

## How it works

1. Detect existing host key files (`ssh_host_*_key` and `*_key.pub`).
2. Move them to a backup directory with a timestamp.
3. Generate new keys with `ssh-keygen`.
4. If `-r` is given, run `systemctl restart sshd` (or `service ssh restart`).

## Safety

- Requires root privileges.
- Backup directory is `${KEY_DIR}/backup-$(date +%s)`.

## Testing

Run the test suite with:

```sh
sh tests/test_rotate_ssh_keys.sh
```

The test creates a temporary key directory, invokes the script, and verifies that new keys are present while old keys are backed up.
