# Nightly Chaos Chaos Chaos 7

A whimsical Bash utility that orchestrates multiple chaos agents (network, resource, time, service) in a single run, with a mockable test suite for reproducible chaos engineering.

## Features

- **Network Chaos**: Simulates latency, packet loss, and bandwidth throttling.
- **Resource Chaos**: Spawns CPU and memory stressors.
- **Time Chaos**: Adjusts system time forward or backward.
- **Service Chaos**: Stops and starts services.
- **Cleanup**: Removes all chaos effects.
- **Mockable Tests**: Deterministic, offline test suite with mocks.

## Usage

```bash
./src/main.sh --scenario network
./src/main.sh --scenario resource
./src/main.sh --scenario time
./src/main.sh --scenario service
./src/main.sh --cleanup
```

## Requirements

- `tc` (for network chaos)
- `stress` (for resource chaos)
- `systemctl` (for service chaos)
- `date` (for time chaos)

## License

MIT
