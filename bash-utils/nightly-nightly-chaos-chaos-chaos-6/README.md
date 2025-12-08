# Nightly Chaos Chaos Chaos

A whimsical-yet-useful Bash utility that orchestrates chaos experiments across multiple systems using Ansible, Docker, and Kubernetes. Perfect for testing resilience in distributed systems!

## Features

- **Multi-Platform Chaos**: Execute chaos experiments on Ansible-managed hosts, Docker containers, and Kubernetes clusters.
- **Scenario Management**: Define and run various chaos scenarios (network latency, resource exhaustion, service failures, time manipulation).
- **Report Generation**: Generate detailed reports of chaos experiments.
- **Cleanup Automation**: Automatically clean up after experiments.

## Installation

1. Clone this repository.
2. Ensure you have the required dependencies installed:
   - Ansible
   - Docker
   - kubectl (configured)
   - jq

## Usage

```bash
# Run all chaos scenarios
./src/main.sh

# Run specific scenarios
./src/main.sh --scenarios network,resource

# Cleanup after experiments
./src/main.sh --cleanup
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT
