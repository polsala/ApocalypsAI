Nightly SSH Key Rotator

Overview:
This utility rotates an SSH RSA key pair for a given user. It backs up any existing private and public keys with a timestamped filename before generating a fresh 4096-bit RSA key pair. The script supports a dry-run mode and a mock generation mode (useful for automated tests).

Usage:
./rotate_ssh_key.sh [-d SSH_DIR] [-f KEY_NAME] [-n]

Options:
- -d SSH_DIR   Directory containing the keys (default: $HOME/.ssh).
- -f KEY_NAME  Base name of the key files without the .pub extension (default: id_rsa).
- -n           Dry-run mode – prints actions without making changes.

Environment:
- MOCK_SSH_KEYGEN=1 – When set, the script creates placeholder key files instead of invoking ssh-keygen. This is used by the test suite.

The script exits with status 0 on success or a non-zero code on error.
