# Nightly Ansible Chaos Orchestrator

A whimsical-yet-useful Ansible playbook for orchestrating controlled chaos engineering experiments across your infrastructure. Inspired by the chaos of post-apocalyptic wastelands, this tool helps you build resilient systems by injecting controlled failures.

## Features

- **Network Chaos**: Introduce latency, packet loss, and bandwidth limitations
- **Service Chaos**: Stop/start/restart services randomly
- **Resource Chaos**: Consume CPU, memory, and disk I/O
- **Time Chaos**: Manipulate system time and NTP settings
- **Random Chaos**: Execute unpredictable system modifications
- **Automated Cleanup**: Restore systems to original state
- **Detailed Reporting**: Generate comprehensive chaos experiment reports

## Requirements

- Ansible 2.10+
- Linux hosts with sudo access
- `tc` (traffic control) for network chaos
- `stress` or `stress-ng` for resource chaos
- `systemctl` for service chaos

## Usage

1. **Clone or copy the playbook directory**
2. **Update inventory** with your target hosts
3. **Configure scenarios** in `vars/chaos_scenarios.yml`
4. **Run the chaos playbook**:

```bash
# Run all chaos experiments
ansible-playbook chaos_orchestrator.yml

# Run specific chaos types
ansible-playbook chaos_orchestrator.yml --tags "network,service"

# Run with custom scenarios
ansible-playbook chaos_orchestrator.yml -e "chaos_duration=300"

# Cleanup only
ansible-playbook chaos_orchestrator.yml --tags "cleanup"
```

## Configuration

### Inventory

Update `inventory` file with your target hosts:

```ini
[chaos_targets]
server1.example.com
server2.example.com
server3.example.com
```

### Chaos Scenarios

Edit `vars/chaos_scenarios.yml` to customize chaos experiments:

```yaml
chaos_scenarios:
  network:
    enabled: true
    experiments:
      - name: "latency"
        probability: 50
        latency_ms: 100
        latency_variation: 50
      - name: "packet_loss"
        probability: 30
        loss_percent: 10
      - name: "bandwidth"
        probability: 25
        bandwidth_limit: "1mbit"

  service:
    enabled: true
    services:
      - name: "nginx"
        probability: 40
      - name: "ssh"
        probability: 20

  resource:
    enabled: true
    cpu_cores: 2
    memory_gb: 1
    disk_io: true
    duration: 300

  time:
    enabled: false
    time_shift_minutes: 60

  random:
    enabled: true
    experiments:
      - name: "disk_fill"
        probability: 20
        fill_percent: 80
      - name: "process_kill"
        probability: 30
        target_process: "python"
```

## Safety Features

- **Dry Run Mode**: Use `--check` to preview changes
- **Automatic Cleanup**: All chaos is automatically reverted
- **Time Limits**: Experiments have maximum duration limits
- **Rollback**: Failed experiments trigger automatic rollback
- **Reporting**: Detailed logs of all chaos activities

## Examples

### Basic Chaos Run

```bash
ansible-playbook chaos_orchestrator.yml
```

### Targeted Network Chaos

```bash
ansible-playbook chaos_orchestrator.yml --tags "network" -e "chaos_duration=180"
```

### Custom Scenario

```bash
ansible-playbook chaos_orchestrator.yml -e "@my_scenarios.yml"
```

## Monitoring

Monitor chaos experiments in real-time:

```bash
# Watch system metrics
watch -n 1 'ps aux | grep -E "(stress|tc)"'

# Monitor network interfaces
watch -n 1 'tc qdisc show'

# Check service status
ansible chaos_targets -m systemd -a "name=nginx"
```

## Cleanup

The playbook automatically cleans up all chaos artifacts. You can also run cleanup manually:

```bash
ansible-playbook chaos_orchestrator.yml --tags "cleanup"
```

## Reporting

After each run, a detailed report is generated showing:

- Chaos experiments executed
- Duration and impact
- Cleanup status
- Any failures or issues
- Recommendations for improvement

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add new chaos experiments or improvements
4. Update tests
5. Submit a pull request

## License

MIT License - see LICENSE file

## Disclaimer

Use this tool responsibly in controlled environments. Chaos engineering can cause system instability. Always test in development environments first.

## Support

- Report issues via GitHub Issues
- Join our Discord for community support
- Check the wiki for advanced usage tips
