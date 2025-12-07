# Nightly Chaos Chaos Chaos

A whimsical chaos engineering tool that randomly induces failures in network, services, resources, and time to test system resilience.

## Features

- **Network Chaos**: Introduce latency, packet loss, and bandwidth limits
- **Service Chaos**: Randomly restart or stop services
- **Resource Chaos**: Consume CPU, memory, and disk I/O
- **Time Chaos**: Manipulate system time
- **Random Chaos**: Unpredictable failures for maximum chaos

## Installation

1. Clone or copy the `src/main.sh` script
2. Make it executable: `chmod +x src/main.sh`
3. Ensure required tools are installed:
   - `tc` (traffic control)
   - `systemctl` (system services)
   - `stress` (resource stress testing)

## Usage

```bash
# Run all chaos scenarios
./src/main.sh --all

# Run specific chaos type
./src/main.sh --network
./src/main.sh --services
./src/main.sh --resources
./src/main.sh --time
./src/main.sh --random

# Cleanup chaos effects
./src/main.sh --cleanup

# View help
./src/main.sh --help
```

## Examples

```bash
# Induce network latency of 100ms on eth0
./src/main.sh --network --interface eth0 --latency 100

# Stress CPU for 60 seconds
./src/main.sh --resources --cpu 4 --timeout 60

# Randomly restart nginx service
./src/main.sh --services --restart nginx
```

## Safety Notes

- Use only in testing/staging environments
- Always run cleanup after chaos experiments
- Monitor system health during chaos injection

## License

MIT
