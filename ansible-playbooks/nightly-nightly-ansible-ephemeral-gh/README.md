# Nightly Ansible Ephemeral Ghost Buster

A whimsical-yet-useful Ansible playbook that hunts and cleans up orphaned ephemeral resources across cloud and on-prem environments. Think of it as a ghostbuster for your infrastructure—catching those pesky leftover resources that no one remembers creating.

## Features
- Detects orphaned resources by comparing live state with inventory and tags
- Supports AWS, Azure, GCP, and on-prem resources
- Generates a cleanup report with mock rationale for each action
- Includes comprehensive tests with mocked scenarios

## Usage
1. Clone this repository
2. Install Ansible (tested with 2.14+)
3. Configure your inventory and cloud credentials
4. Run the playbook:
   ```bash
   ansible-playbook -i inventory.ini ghost_buster.yml
   ```
5. Review the generated report in `reports/ghost_buster_report.html`

## Requirements
- Ansible 2.14+
- Cloud provider CLI tools (aws, az, gcloud) for live runs
- Python 3.11+ for tests

## License
MIT
