# Nightly Ansible Chaos Orchestrator

A whimsical-yet-useful Ansible playbook for chaos engineering experiments. This tool helps you build resilience by injecting controlled chaos into your infrastructure.

## Features

- **Network Chaos**: Introduce latency, packet loss, and bandwidth limits
- **Resource Chaos**: Consume CPU, memory, and disk I/O
- **Service Chaos**: Restart, stop, or kill services
- **Time Chaos**: Manipulate system time
- **Random Chaos**: Unpredictable chaos scenarios
- **Automated Cleanup**: Restores systems to original state
- **Comprehensive Reporting**: Generates detailed chaos experiment reports

## Requirements

- Ansible 2.10+
- Linux hosts with sudo access
- `stress` package for resource chaos
- `tc` (traffic control) for network chaos

## Usage

```bash
# Run all chaos scenarios
./run_chaos.sh

# Run specific scenario
ansible-playbook chaos_orchestrator.yml --tags "network"

# Run with custom parameters
ansible-playbook chaos_orchestrator.yml -e "chaos_duration=60 chaos_intensity=medium"
```

## Scenarios

### Network Chaos
- Latency injection (50ms - 500ms)
- Packet loss (1% - 20%)
- Bandwidth limiting (1Mbps - 100Mbps)

### Resource Chaos
- CPU stress (1 - 100%)
- Memory consumption (10% - 90%)
- Disk I/O stress

### Service Chaos
- Random service restarts
- Service kills
- Service stop/start cycles

### Time Chaos
- Clock skew (±1 hour)
- Time acceleration/deceleration

### Random Chaos
- Unpredictable chaos combinations
- Random timing and intensity

## Safety Features

- **Automatic Cleanup**: All changes are reverted after chaos
- **Rollback Mechanisms**: Emergency recovery procedures
- **Safety Checks**: Validates system state before and after
- **Dry Run Mode**: Test scenarios without actual execution

## Reports

After each chaos run, a detailed report is generated showing:
- Chaos scenarios executed
- System metrics during chaos
- Recovery status
- Recommendations for improvement

## Contributing

1. Add new chaos scenarios to `vars/chaos_scenarios.yml`
2. Create corresponding task files in `tasks/chaos/`
3. Update the test suite in `tests/`
4. Submit a PR!

## License

MIT License - Use responsibly and at your own risk!
