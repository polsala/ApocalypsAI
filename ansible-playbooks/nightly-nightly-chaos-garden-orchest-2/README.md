# Nightly Chaos Garden Orchestrator

A whimsical chaos engineering tool that orchestrates random failures across garden nodes to test resilience and generate beautiful chaos reports.

## Features

- 🌱 Orchestrates chaos experiments across multiple garden nodes
- 🎲 Random failure injection (network, services, resources, time)
- 📊 Beautiful chaos reports with insights and recommendations
- 🧹 Automatic cleanup after chaos experiments
- 🎭 Whimsical chaos scenarios for testing resilience

## Usage

```bash
# Run chaos experiments
ansible-playbook chaos_garden_orchestrator.yml -i inventory.ini

# View chaos report
cat /tmp/chaos_garden_report.txt
```

## Requirements

- Ansible 2.11+
- Python 3.8+

## License

MIT
