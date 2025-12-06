# Nightly Nightly Chaos Chaos Chaos

A whimsical chaos engineering tool that injects controlled mayhem into systems for resilience testing.

## Features

- **Network Chaos**: Introduce latency, packet loss, and bandwidth limits
- **Service Chaos**: Randomly restart or stop services
- **Resource Chaos**: Consume CPU, memory, and disk I/O
- **Time Chaos**: Manipulate system time
- **Cleanup**: Restore systems to their original state

## Installation

1. Clone or copy the `src/main.sh` script to your system
2. Ensure you have the required dependencies:
   - `tc` (Traffic Control) for network chaos
   - `stress` for resource chaos
   - `systemctl` for service chaos
   - `date` for time chaos
3. Make the script executable: `chmod +x src/main.sh`

## Usage

```bash
# Run all chaos scenarios
./src/main.sh --chaos all

# Run specific chaos type
./src/main.sh --chaos network
./src/main.sh --chaos service
./src/main.sh --chaos resource
./src/main.sh --chaos time

# Cleanup after chaos
./src/main.sh --cleanup

# View help
./src/main.sh --help
```

## Examples

```bash
# Network chaos with 100ms latency and 5% packet loss
./src/main.sh --chaos network --latency 100 --packet-loss 5

# Resource chaos consuming 50% CPU and 1GB memory
./src/main.sh --chaos resource --cpu 50 --memory 1024

# Service chaos targeting nginx and ssh
./src/main.sh --chaos service --services nginx,ssh

# Time chaos shifting system time by 1 hour forward
./src/main.sh --chaos time --time-shift 3600
```

## Safety Notes

- This tool requires root privileges for many operations
- Always test in development environments first
- Use the cleanup command to restore systems after testing
- Monitor your systems closely during chaos experiments

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

MIT License - see LICENSE file for details.
