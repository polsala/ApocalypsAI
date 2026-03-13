# nightly-ssh-key-rotator

Utility to rotate SSH keys across multiple hosts in a whimsical apocalypse‑ready fashion. Generates a fresh RSA key pair, distributes the public key to given host directories (simulating remote hosts), and removes the old key entry.

## Usage

```bash
./src/main.sh -u <user> -h <host_dir1,host_dir2,...>
```

- `-u` : username (for display only)
- `-h` : comma‑separated list of host directories. Each directory must contain a `.ssh/authorized_keys` file.

The script creates a new key pair at `~/.ssh/id_rsa_rotated` (and `.pub`). It appends the public key to each host's `authorized_keys` and removes any line containing the marker `OLDKEY`.

## Requirements

- Bash 4+
- `ssh-keygen` (standard OpenSSH)

## Testing

Run the bundled tests:

```bash
bash tests/test_main.sh
```
