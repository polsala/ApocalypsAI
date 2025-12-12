# Nightly Chaos Garden Orchestrator

A whimsical yet practical Ansible playbook that orchestrates controlled chaos experiments across your infrastructure, complete with automated rollback and detailed reporting.

## Features

- 🌱 **Garden Metaphor**: Chaos experiments are "weeding" your infrastructure
- 🎲 **Random Chaos**: Introduces unpredictable but safe failures
- 🔄 **Automatic Rollback**: Restores services if chaos goes too far
- 📊 **Detailed Reporting**: Generates comprehensive chaos experiment reports
- 🧪 **Safe Testing**: All chaos is bounded and reversible

## Usage

```bash
# Run chaos experiments on all hosts
ansible-playbook chaos_garden_orchestrator.yml

# Run specific chaos type
ansible-playbook chaos_garden_orchestrator.yml --tags network-chaos

# Cleanup after chaos
ansible-playbook chaos_garden_orchestrator.yml --tags cleanup
```

## Requirements

- Ansible 2.9+
- Python 3.6+
- Target hosts must have systemd or service management

## Safety Features

- Maximum chaos duration limits
- Automatic service restoration
- Health check validation
- Rollback on failure

## Contributing

Add new chaos scenarios to `vars/chaos_scenarios.yml` or create new task files in `tasks/chaos/`.
