# Nightly Ephemeral SSH Key Rotator

This utility automates the rotation of SSH keys for ephemeral servers, ensuring secure and efficient key management. It generates new key pairs, distributes them to specified hosts, and cleans up old keys.

## Features
- Generate new SSH key pairs
- Distribute public keys to multiple hosts
- Clean up old keys from hosts
- Log all operations for audit trails

## Usage

### Prerequisites
- `ssh` and `ssh-keygen` installed
- Passwordless SSH access to target hosts

### Installation
1. Clone this repository
2. Make the script executable: `chmod +x src/rotate_ssh_keys.sh`

### Running the Utility
```bash
./src/rotate_ssh_keys.sh --hosts-file hosts.txt --key-name my-key
```

### Arguments
- `--hosts-file`: Path to a file containing hostnames/IPs (one per line)
- `--key-name`: Name for the new SSH key pair

## Testing
Run the test suite:
```bash
./tests/test_rotate_ssh_keys.sh
```

## License
MIT
