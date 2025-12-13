# Nightly Chaos Garden Orchestrator

A whimsical-yet-useful Ansible playbook that orchestrates controlled chaos in your infrastructure garden. Perfect for chaos engineering, resilience testing, and keeping your ops team on their toes!

## Features

- 🌪️ Orchestrates multiple chaos scenarios (network, resource, service, time)
- 🧹 Automatic cleanup after chaos experiments
- 📊 Detailed chaos reports with metrics and recommendations
- 🎲 Random chaos injection for unpredictable testing
- 🌱 Garden-themed chaos with plant metaphors

## Quick Start

```bash
# Clone and run the chaos orchestrator
./run_chaos.sh

# Or run directly with Ansible
ansible-playbook chaos_garden_orchestrator.yml -i inventory.ini
```

## Chaos Scenarios

- **Network Chaos**: Packet loss, latency, and bandwidth throttling
- **Resource Chaos**: CPU/memory spikes and disk I/O stress
- **Service Chaos**: Random service restarts and failures
- **Time Chaos**: Clock skew and time manipulation
- **Random Chaos**: Completely unpredictable chaos injection

## Safety Features

- Pre-chaos health checks
- Automatic rollback on critical failures
- Detailed logging and reporting
- Configurable chaos intensity

## Requirements

- Ansible 2.9+
- Python 3.8+
- Target hosts with SSH access

## License

MIT - because chaos should be shared!
