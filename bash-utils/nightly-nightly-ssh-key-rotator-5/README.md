Nightly SSH Key Rotator
========================

Automates the creation of a fresh SSH key pair and distributes the public key to a list of remote hosts. Ideal for periodic key rotation in a fleet of servers.

## Prerequisites
- `ssh-keygen` and `ssh-copy-id` must be installed (standard on most Unix systems).
- Passwordless SSH access (or appropriate authentication) to each target host.

## Usage
```bash
./rotate_ssh_keys.sh <hosts_file> [key_path]
```
- **hosts_file**: Plain text file with one hostname per line.
- **key_path** (optional): Destination for the new private key. Defaults to `~/.ssh/id_rsa_rotated`.

The script will:
1. Generate a new RSA‑4096 key pair (overwrites if the file already exists).
2. Append the public key to `authorized_keys` on each host via `ssh-copy-id`.
3. Report completion and the location of the private key.

## Example
```bash
cat > hosts.txt <<EOF
host1.example.com
host2.example.com
EOF

./rotate_ssh_keys.sh hosts.txt
```

## Testing
Run the test suite with:
```bash
bash tests/test_rotate_ssh_keys.sh
```
The tests use mock versions of `ssh-keygen` and `ssh-copy-id` to verify behaviour without touching real hosts.
