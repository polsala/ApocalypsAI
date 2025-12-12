# Nightly Chaos Garden Orchestrator

A whimsical-yet-useful Ansible playbook that simulates controlled chaos in a garden environment to test system resilience and recovery mechanisms.

## Overview

This playbook orchestrates various chaos engineering scenarios in a garden-themed environment, including:
- Network disruptions (simulating "garden pests" eating cables)
- Resource exhaustion (simulating "overgrown weeds" consuming system resources)
- Service failures (simulating "wilting flowers" in your infrastructure)
- Time distortions (simulating "seasonal shifts" in system behavior)

## Features

- **Garden-themed chaos scenarios**: All chaos experiments are presented with whimsical garden metaphors
- **Configurable chaos levels**: From "gentle breeze" to "tornado in a teacup"
- **Automatic cleanup**: Restores your garden to its original state
- **Detailed reporting**: Generates beautiful reports with garden-themed visualizations
- **Safe defaults**: All chaos experiments are designed to be safe and reversible

## Requirements

- Ansible 2.10 or later
- Python 3.8 or later
- Target systems must have Python installed

## Quick Start

1. Clone this repository
2. Configure your inventory file
3. Run the chaos orchestrator:

```bash
ansible-playbook chaos_garden_orchestrator.yml -i inventory.ini
```

## Configuration

Edit the `vars/chaos_scenarios.yml` file to customize:
- Chaos intensity levels
- Target systems and services
- Duration of chaos experiments
- Recovery procedures

## Safety First

- Always test in a staging environment first
- Review the chaos scenarios before running
- Ensure you have proper backups
- Monitor your systems during chaos experiments

## Contributing

We welcome gardeners (contributors) who want to add new chaos scenarios or improve existing ones. Please follow our whimsical coding standards!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

*Remember: A little chaos keeps your systems humble. Just don't let the weeds take over!*
