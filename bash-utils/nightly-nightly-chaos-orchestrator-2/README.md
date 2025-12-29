# Nightly Chaos Orchestrator

A whimsical chaos engineering tool that injects controlled mayhem into systems using configurable scenarios. Perfect for testing system resilience in a fun and safe way!

## Features

- 🎲 Random chaos scenarios
- 🕸️ Network disruption
- 💾 Resource exhaustion
- ⏰ Time manipulation
- 🔄 Service disruption
- 🧹 Automatic cleanup
- 📊 Chaos reports

## Quick Start

```bash
# Run with default scenarios
./run_chaos.sh

# Run with custom inventory
./run_chaos.sh --inventory custom_inventory.ini

# Run specific scenario
./run_chaos.sh --scenario network_partition

# Dry run (no actual chaos)
./run_chaos.sh --dry-run
```

## Configuration

### Inventory

Define your chaos targets in `inventory.ini`:

```ini
[targets]
web-server = localhost
api-server = 192.168.1.100
```

### Scenarios

Configure chaos scenarios in `vars/chaos_scenarios.yml`:

```yaml
chaos_scenarios:
  network_partition:
    description: "Simulate network partition"
    duration: 30
    probability: 0.3
  resource_exhaustion:
    description: "Consume system resources"
    duration: 60
    probability: 0.2
```

## Safety Features

- All chaos operations are logged
- Automatic cleanup after each scenario
- Configurable probability to prevent constant chaos
- Dry-run mode for testing

## Requirements

- Bash 4.0+
- Python 3.6+ (for Jinja2 templating)
- Ansible 2.9+ (for orchestration)

## License

MIT - because chaos should be shared!
