# Nightly Ephemeral SSH Rotator

A whimsical-yet-useful Bash utility that generates ephemeral SSH key pairs with automatic rotation, cleanup, and audit logging. Perfect for security-conscious teams who want to rotate SSH keys regularly without manual intervention.

## Features

- Generates unique SSH key pairs with timestamps
- Automatic cleanup of expired keys (configurable TTL)
- Audit logging for compliance and security tracking
- Simple CLI interface with help documentation
- Cross-platform compatibility (Linux/macOS)

## Usage

```bash
# Generate a new ephemeral SSH key pair
./src/ephemeral_ssh_rotator.sh generate

# Rotate keys (generates new + cleans old)
./src/ephemeral_ssh_rotator.sh rotate

# Clean up expired keys
./src/ephemeral_ssh_rotator.sh cleanup

# Show help
./src/ephemeral_ssh_rotator.sh --help

# View audit log
./src/ephemeral_ssh_rotator.sh log
```

## Installation

1. Clone or download this utility
2. Make the script executable: `chmod +x src/ephemeral_ssh_rotator.sh`
3. Run from the utils directory

## Configuration

Edit the script to modify:
- `KEY_TTL_HOURS`: Time-to-live for generated keys (default: 24 hours)
- `KEY_DIR`: Directory to store ephemeral keys (default: ~/.ephemeral_ssh)
- `LOG_FILE`: Audit log location (default: ~/.ephemeral_ssh/audit.log)

## Security Notes

- Keys are automatically removed after TTL expires
- All operations are logged with timestamps and operation details
- Keys are generated with 4096-bit RSA for strong security
- Script validates permissions and exits safely on errors

## Requirements

- Bash 4.0+
- ssh-keygen (standard with OpenSSH)
- date command with GNU extensions

## License

MIT - feel free to use in your post-apocalyptic security setup!
