# Nightly Ansible SSH Key Rotator

This utility provides an Ansible playbook that rotates an SSH host key, backs up the existing key, and stores the new key in a configurable location. It is designed to run on any host reachable by Ansible (default is the local machine).

## Features

- Generates a new RSA key pair (4096âbit)
- Backs up any existing key with a timestamped filename
- Allows custom key and backup locations via extra variables
- Works with the `local` connection (no remote hosts required)

## Prerequisites

- Ansible installed (`pip install ansible` or your package manager)
- `ssh-keygen` available in the PATH (standard on most Unixâlike systems)

## Usage

```bash
ansible-playbook -i inventory.ini rotate_ssh_key.yml -e "key_path=~/.ssh/rotated_ssh_host_rsa_key backup_dir=~/.ssh/backup_keys target=localhost"
```

- `key_path` â Destination for the new SSH key (default: `~/.ssh/rotated_ssh_host_rsa_key`)
- `backup_dir` â Directory where the old key will be archived (default: `~/.ssh/backup_keys`)
- `target` â Host or group to run against (default: `localhost`)

## Files

- `rotate_ssh_key.yml` â The Ansible playbook
- `inventory.ini` â Simple inventory targeting the local host
- `tests/test_key_rotator.sh` â Automated test script (runs offline)

## Testing

The test script creates a temporary directory, generates a dummy key, runs the playbook, and verifies that:

1. A new key file exists at the specified location
2. A backup of the old key was created

Run the test with:

```bash
chmod +x tests/test_key_rotator.sh
./tests/test_key_rotator.sh
```

## License

MIT â see the repository LICENSE file.
