# Nightly Ansible Chaos Orchestrator

A whimsical-yet-useful Ansible playbook for orchestrating chaos engineering experiments across your infrastructure. Inspired by the post-apocalyptic world of ApocalypsAI, this tool helps you test system resilience by introducing controlled chaos with automated rollback and detailed reporting.

## Features

- **Chaos Scenarios**: Network latency, service restarts, resource exhaustion, and time manipulation
- **Automated Rollback**: Automatic cleanup and restoration after chaos experiments
- **Detailed Reporting**: Generate comprehensive chaos reports with system metrics
- **Safe Testing**: Designed for isolated environments with safety checks

## Quick Start

1. Clone this repository
2. Install Ansible: `pip install ansible`
3. Configure your inventory in `inventory.ini`
4. Run the chaos orchestrator:

```bash
./run_chaos.sh
```

## Configuration

Edit `vars/chaos_scenarios.yml` to customize chaos experiments:

```yaml
chaos_scenarios:
  - name: "Network Latency"
    duration: 30
    probability: 0.5
  - name: "Service Restart"
    services: ["nginx", "apache"]
    duration: 10
```

## Safety First

⚠️ **WARNING**: This tool is designed for testing environments only. Never run it against production systems.

## License

MIT License - Use responsibly in your post-apocalyptic testing scenarios!
