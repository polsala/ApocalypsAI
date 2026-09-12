# nightly-ssh-key-rotator

**Purpose**: Rotate your SSH host keys with a single command while keeping a timestamped backup of the previous keys. Perfect for post‑apocalypse security drills or regular hardening routines.

## Features
- Detects existing `ssh_host_*` keys in a target directory (default `~/.ssh`).
- Moves old keys to a backup folder with a timestamp.
- Generates fresh 4096‑bit RSA host keys using `ssh-keygen` (non‑interactive).
- Fully self‑contained Bash script – no external dependencies beyond standard Unix tools.

## Installation
```bash
# Clone the repository (or copy the script) into your preferred location
mkdir -p ~/bin && cp src/rotate_ssh_keys.sh ~/bin/rotate_ssh_keys
chmod +x ~/bin/rotate_ssh_keys
```

## Usage
```bash
# Rotate keys in the default ~/.ssh directory, backup to ~/.ssh/backup
rotate_ssh_keys.sh

# Specify a custom directory and backup location
rotate_ssh_keys.sh -d /etc/ssh -b /var/backups/ssh_keys
```

### Options
- `-d <dir>` – Directory containing the host keys (default: `$HOME/.ssh`).
- `-b <dir>` – Backup directory where old keys will be stored (default: `<target>/backup`).
- `-h` – Show help message.

## How It Works
1. **Detect existing keys** – Looks for files matching `ssh_host_*_key`.
2. **Backup** – Creates a sub‑directory `<backup>/<YYYYmmdd_HHMMSS>` and moves any found keys there.
3. **Generate** – Calls `ssh-keygen -t rsa -b 4096 -f <target>/ssh_host_rsa_key -N "" -q` (you can extend the script for other key types).
4. **Report** – Prints a concise summary of actions taken.

## Testing
Run the bundled test suite to verify behavior in an isolated temporary environment:
```bash
cd tests && bash test_rotate_ssh_keys.sh
```
The test uses a mock `ssh-keygen` to avoid generating real keys.

## License
MIT – feel free to adapt, improve, or weaponize it for your own post‑apocalyptic infrastructure.
