# nightly-ssh-key-rotator

Utility to rotate SSH keys for a given user. It generates a new ed25519 key pair, backs up the existing `authorized_keys`, appends the new public key, and leaves the old private key untouched (you can delete it manually if desired).

## Features
- Generates a fresh ed25519 key pair without a passphrase (suitable for automated environments).
- Backs up the current `authorized_keys` with a timestamped filename.
- Appends the new public key to `authorized_keys` so existing access remains.
- Deterministic timestamp via optional `DATE_NOW` env var (useful for testing).

## Requirements
- Bash (>=4)
- `ssh-keygen` (part of OpenSSH)

## Installation
```bash
# Clone the repository (or copy the files) and make the script executable
chmod +x src/rotate_ssh_keys.sh
```

## Usage
```bash
./src/rotate_ssh_keys.sh -u USERNAME [-d SSH_DIRECTORY]
```
- `-u USERNAME` – **required**. The user whose SSH directory will be processed.
- `-d SSH_DIRECTORY` – Optional. Path to the `.ssh` directory. Defaults to `/home/USERNAME/.ssh`.

### Example
```bash
# Rotate keys for user "alice" using the default home directory
./src/rotate_ssh_keys.sh -u alice
```

## Testing
Run the bundled test script:
```bash
bash tests/test_rotate_ssh_keys.sh
```
All tests should pass on a standard Linux environment.

## License
MIT © ApocalypsAI
