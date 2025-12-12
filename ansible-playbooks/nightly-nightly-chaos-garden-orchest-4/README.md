# Nightly Chaos Garden Orchestrator

A whimsical-yet-useful Ansible playbook that orchestrates chaos experiments across garden nodes while tracking temporal anomalies. Perfect for testing resilience in distributed systems with a touch of post-apocalyptic flair.

## Features

- 🌱 Orchestrates chaos experiments across multiple garden nodes
- ⚡ Tracks temporal anomalies during chaos runs
- 📊 Generates comprehensive chaos reports
- 🛠️ Supports network, resource, service, and time-based chaos scenarios
- 🧹 Automated cleanup after chaos experiments

## Requirements

- Ansible 2.14+
- Python 3.8+
- SSH access to target nodes

## Usage

1. Configure your inventory in `inventory.ini`
2. Customize chaos scenarios in `vars/chaos_scenarios.yml`
3. Run the orchestrator:

```bash
ansible-playbook chaos_garden_orchestrator.yml
```

## Output

The playbook generates a detailed chaos report in `/tmp/chaos_garden_report.txt` on the control node.

## License

MIT - Use responsibly in your post-apocalyptic testing scenarios!
