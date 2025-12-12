# Nightly Chaos Garden Orchestrator

A whimsical-yet-useful Ansible playbook that orchestrates controlled chaos experiments across garden nodes, with automated cleanup and reporting.

## Features
- Orchestrates multiple chaos scenarios (network, resource, service, time)
- Automated cleanup after chaos experiments
- Generates detailed chaos reports
- Whimsical garden-themed chaos scenarios
- Deterministic testing with mock inventory

## Usage

```bash
# Run the chaos orchestrator
ansible-playbook chaos_garden_orchestrator.yml -i inventory.ini

# Run with specific scenarios
ansible-playbook chaos_garden_orchestrator.yml -i inventory.ini --extra-vars "chaos_scenarios=['network_partition']"
```

## Requirements
- Ansible 2.10+
- Python 3.8+

## License
MIT
