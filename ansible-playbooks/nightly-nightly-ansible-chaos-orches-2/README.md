# Nightly Ansible Chaos Orchestrator

A whimsical yet practical Ansible playbook that orchestrates controlled chaos experiments across your infrastructure. Inspired by chaos engineering principles, this tool helps you build confidence in your system's resilience.

## Features

- **Chaos Scenarios**: Network latency, service failures, resource exhaustion, and time manipulation
- **Whimsical Reporting**: Generates a chaos report with ASCII art and humorous commentary
- **Automatic Cleanup**: Ensures systems are restored after chaos experiments
- **Configurable**: Easy to customize chaos scenarios and targets

## Requirements

- Ansible 2.10+
- Target hosts must have `tc` (traffic control) for network chaos
- Root/sudo access on target hosts

## Usage

1. Clone this repository
2. Update the `inventory` file with your target hosts
3. Customize `vars/chaos_scenarios.yml` to configure chaos experiments
4. Run the playbook:

```bash
./run_chaos.sh
```

## Example Output

```
========================================
          CHAOS EXPERIMENT REPORT
========================================

Target Host: server-01
Experiment: Network Latency
Duration: 60 seconds
Status: SUCCESS

ASCII Art: 
  (╯°□°）╯︵ ┻━┻

Commentary: Looks like someone spilled coffee on the network cables!

========================================
```

## Safety First

- Always test in development environments first
- Ensure you have rollback procedures
- Monitor your systems during chaos experiments

## License

MIT
