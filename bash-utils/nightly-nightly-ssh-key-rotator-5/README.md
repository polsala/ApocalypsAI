# nightly-ssh-key-rotator

**Purpose**: Rotate SSH host keys on a server in a safe, automated way while keeping timestamped backups of the previous keys. Perfect for post‑apocalypse server hardening or just regular key hygiene.

## Features
- Generates a new RSA (or other type) host key using `ssh-keygen`.
- Backs up existing keys with a timestamped suffix.
- Works on any directory containing the host keys (default: `/etc/ssh`).
- Fully scriptable – can be run from cron or CI pipelines.

## Installation
```bash
# Clone the repository (or copy the files into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/bash-utils/nightly-ssh-key-rotator
chmod +x src/main.sh
chmod +x tests/test_main.sh
```

## Usage
```bash
# Rotate the default RSA host key (reads from /etc/ssh)
sudo ./src/main.sh rsa

# Rotate an ED25519 key located in a custom directory
sudo KEY_DIR=/custom/ssh ./src/main.sh ed25519
```

- The first argument is the key type (`rsa`, `ed25519`, `ecdsa`, …). If omitted, `rsa` is used.
- The environment variable `KEY_DIR` can be set to point to a different directory containing the host keys.
- The environment variable `SSH_KEYGEN_CMD` can be overridden for testing or custom key generation tools.

## Safety notes
- The script **must** be run with sufficient privileges to read/write the key files (usually root).
- Backups are stored alongside the original files with a timestamp suffix, e.g. `ssh_host_rsa_key.bak_20231130123045`.
- Always verify the new keys are correctly referenced in your SSH daemon configuration before restarting the service.

## Testing
Run the bundled test suite (requires Bash only):
```bash
cd tests
bash test_main.sh
```
All tests should pass, confirming that the rotation logic works and that backups are created.

## License
MIT – feel free to adapt, improve, or weaponize for your own post‑apocalyptic infrastructure.
