# Nightly Ansible Chaos Orchestrator

A whimsical-yet-useful Ansible playbook for controlled chaos engineering in development environments. Simulate realistic failure scenarios to test your application's resilience without breaking production!

## Features

- **Network Chaos**: Simulate latency, packet loss, and bandwidth throttling
- **Resource Chaos**: CPU stress, memory pressure, and disk I/O throttling
- **Service Chaos**: Random service restarts and port blocking
- **Time Chaos**: NTP manipulation and timezone changes
- **Safe Mode**: Automatic rollback and safety checks

## Requirements

- Ansible 2.14+
- Linux target hosts with sudo access
- `tc` (traffic control) package for network chaos
- `stress` package for resource chaos

## Quick Start

```bash
# Clone and run
ansible-playbook -i inventory chaos_orchestrator.yml --extra-vars "chaos_type=network chaos_duration=60"

# Or use the convenience script
./run_chaos.sh network 60
```

## Chaos Scenarios

### Network Chaos
- Latency injection (10ms - 2000ms)
- Packet loss (1% - 50%)
- Bandwidth limiting (1mbit - 100mbit)

### Resource Chaos
- CPU stress (1 - 100%)
- Memory pressure (10MB - 8GB)
- Disk I/O throttling

### Service Chaos
- Random service restarts
- Port blocking/unblocking
- Process killing

### Time Chaos
- NTP server manipulation
- System clock adjustments
- Timezone changes

## Safety Features

- Automatic rollback after chaos duration
- Pre-flight checks for critical services
- Dry-run mode for testing
- Logging and reporting

## Contributing

Add new chaos scenarios by creating new task files in `tasks/chaos/` and updating `defaults/main.yml`.

## License

MIT - Use responsibly and only in development environments!
