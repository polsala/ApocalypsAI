# Nightly Ansible Chaos Orchestrator

A whimsical-yet-useful Ansible playbook that orchestrates controlled chaos experiments across your infrastructure. Inspired by chaos engineering principles, this tool helps you build resilience by introducing randomized failures in a safe, controlled manner.

## Features

- **Chaos Scenarios**: Network latency, service failures, resource exhaustion, time manipulation
- **Safety Guards**: Automatic rollback, health checks, and cleanup
- **Whimsical Reporting**: Generate chaos reports with ASCII art and humorous failure descriptions
- **Configurable**: Easy to customize scenarios and thresholds

## Requirements

- Ansible 2.12+
- Python 3.8+
- Target hosts with appropriate permissions for chaos actions

## Quick Start

1. Clone this repository
2. Configure your inventory file
3. Run the chaos orchestrator:

```bash
./run_chaos.sh
```

## Inventory Example

```ini
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com
db2.example.com
```

## Scenarios

### Network Chaos
- Adds random latency and packet loss
- Tests connectivity resilience

### Service Chaos
- Randomly restarts services
- Simulates service failures

### Resource Chaos
- Consumes CPU/memory temporarily
- Tests resource exhaustion handling

### Time Chaos
- Manipulates system time
- Tests time-sensitive applications

## Safety Features

- **Health Checks**: Validates system health before and after chaos
- **Rollback**: Automatically restores systems to original state
- **Limits**: Configurable chaos duration and intensity

## License

MIT - Use responsibly and only in non-production environments!
