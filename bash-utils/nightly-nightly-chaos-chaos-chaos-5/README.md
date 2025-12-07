# Nightly Chaos Chaos Chaos 5

A whimsical chaos engineering tool that injects controlled failures into systems for resilience testing.

## Features

- Network latency injection
- Service disruption simulation
- Resource exhaustion testing
- Random chaos events
- Time manipulation
- Cleanup automation

## Usage

```bash
./src/main.sh --scenario network-latency --duration 60
./src/main.sh --scenario service-disruption --service nginx
./src/main.sh --scenario resource-exhaustion --cpu 80 --memory 50
./src/main.sh --scenario random --duration 30
./src/main.sh --scenario time-manipulation --offset -300
./src/main.sh --cleanup
```

## Installation

1. Clone or copy the script
2. Make it executable: `chmod +x src/main.sh`
3. Run with appropriate permissions (some scenarios require sudo)

## Scenarios

- `network-latency`: Adds network delay using tc
- `service-disruption`: Stops/starts services using systemctl
- `resource-exhaustion`: Consumes CPU/memory using stress
- `random`: Randomly selects a chaos scenario
- `time-manipulation`: Adjusts system time
- `cleanup`: Removes all chaos effects

## Requirements

- Linux system with bash
- sudo privileges for chaos scenarios
- tc (for network scenarios)
- stress (for resource scenarios)
- systemctl (for service scenarios)

## Safety

This tool is designed for testing environments. Use with caution in production!

## License

MIT
