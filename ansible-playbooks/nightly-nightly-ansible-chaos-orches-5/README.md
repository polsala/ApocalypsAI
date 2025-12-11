# Nightly Ansible Chaos Orchestrator

A whimsical-yet-useful Ansible playbook that orchestrates chaos engineering experiments across your infrastructure with randomized scenarios and detailed reporting.

## Features

- **Randomized Chaos Scenarios**: Network latency, service restarts, resource exhaustion, and time manipulation
- **Detailed Reporting**: Generate comprehensive chaos reports with impact analysis
- **Safe Execution**: Configurable chaos duration and automatic cleanup
- **Whimsical Touch**: Includes "apocalypse preparedness" scoring

## Requirements

- Ansible 2.12+
- Python 3.8+
- SSH access to target hosts

## Usage

1. Clone this playbook
2. Configure your inventory file
3. Adjust chaos scenarios in `vars/chaos_scenarios.yml`
4. Run: `ansible-playbook chaos_orchestrator.yml`

## Example Inventory

```ini
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com
db2.example.com
```

## Safety First

- Always test in a staging environment first
- Use the `--limit` flag to target specific hosts
- Monitor the chaos report for any unexpected impacts

## License

MIT - Use responsibly and may your chaos be controlled!
