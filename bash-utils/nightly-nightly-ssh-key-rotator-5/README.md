# nightly-ssh-key-rotator

**Utility:** Rotate SSH keys for a given user across a fleet of hosts.

### What it does
1. Generates a fresh **ed25519** key pair.
2. Backs up the existing `~/.ssh/authorized_keys` on each target host.
3. Deploys the new public key to `~/.ssh/authorized_keys`.
4. Optionally removes the old key entries.

### Why?
Regular key rotation is a best‑practice for security hygiene, but doing it manually on dozens or hundreds of machines is tedious and error‑prone. This script automates the whole process in a safe, auditable way.

### Prerequisites
- Bash 4+ (available on virtually all Linux/macOS systems)
- `ssh-keygen` (part of OpenSSH)
- Password‑less SSH access (e.g., existing key) for the **target user** on all hosts.

### Usage
```bash
./rotate_ssh_keys.sh -u <remote_user> -h <hosts_file> [-d <dest_dir>]
```
- `-u` – Remote username whose keys will be rotated.
- `-h` – Path to a plain‑text file listing hostnames/IPs, one per line.
- `-d` – Optional directory where the newly generated key pair will be stored. Defaults to a temporary directory that is cleaned up after execution.

### Example
```bash
cat > hosts.txt <<EOF
host1.example.com
host2.example.com
host3.example.com
EOF

./rotate_ssh_keys.sh -u deploy -h hosts.txt
```
The script will:
- Create a temporary key pair (`id_ed25519` & `id_ed25519.pub`).
- For each host, backup `~/.ssh/authorized_keys` to `authorized_keys.bak`.
- Replace the authorized keys with the newly generated public key.
- Print a short summary of actions taken.

### Safety notes
- The script **never deletes** the old `authorized_keys` file; it is renamed to `authorized_keys.bak` on each host.
- All SSH commands are executed via the `$SSH_CMD` variable (default `ssh`). This can be overridden for testing or to use a wrapper like `ssh -o StrictHostKeyChecking=no`.

### Testing
A deterministic test suite lives in `tests/`. It replaces the real `ssh` binary with a mock that records the commands that would have been run, allowing the script to be exercised offline.

### License
MIT – feel free to adapt and improve!
