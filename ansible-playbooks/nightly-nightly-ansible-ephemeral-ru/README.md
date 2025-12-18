# Nightly Ansible Ephemeral Runner

Automatically provision, monitor, and clean up ephemeral GitHub self-hosted runners using Ansible. This playbook ensures runners are healthy, removes stale runners, and generates reports.

## Features
- Provision GitHub self-hosted runners
- Health check existing runners
- Clean up orphaned or unhealthy runners
- Generate detailed reports

## Usage
```bash
# Provision runners
cd nightly-ansible-ephemeral-runner
ansible-playbook provision_runners.yml -i inventory.ini

# Health check
cd nightly-ansible-ephemeral-runner
ansible-playbook health_check.yml -i inventory.ini

# Cleanup
cd nightly-ansible-ephemeral-runner
ansible-playbook cleanup_runners.yml -i inventory.ini
```

## Requirements
- Ansible 2.14+
- GitHub Personal Access Token (PAT)
- Target hosts with Docker support

## Configuration
Edit `inventory.ini` and `vars/main.yml` with your GitHub repository and runner settings.
