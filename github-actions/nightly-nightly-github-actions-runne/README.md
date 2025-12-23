# GitHub Actions Runner Ghost Buster

Automated cleanup of orphaned GitHub Actions self-hosted runners with health checks and reporting.

## Features

- Detects and removes orphaned runners from GitHub repositories
- Performs health checks on active runners
- Generates detailed cleanup reports
- Supports multiple repositories in a single run
- Uses GitHub Actions for automated execution

## Usage

### Manual Execution

```bash
# Run the cleanup playbook
ansible-playbook cleanup_runners.yml -i inventory.ini

# Run health checks only
ansible-playbook health_check.yml -i inventory.ini

# Run full provisioning (cleanup + health check)
ansible-playbook provision_runners.yml -i inventory.ini
```

### Automated Execution

The playbook is designed to run as a GitHub Action that:
1. Detects orphaned runners across configured repositories
2. Removes them automatically
3. Performs health checks on remaining runners
4. Generates and uploads a cleanup report

## Configuration

### Inventory File (inventory.ini)

```ini
[github_repos]
repo1 ansible_host=github.com org=your-org repo=your-repo1
repo2 ansible_host=github.com org=your-org repo=your-repo2
```

### Variables (vars/main.yml)

```yaml
# GitHub API configuration
github_api_token: "{{ lookup('env', 'GITHUB_TOKEN') }}"

# Cleanup configuration
max_runner_age_hours: 24
health_check_timeout: 30

# Reporting
generate_report: true
report_format: "json"
```

## Requirements

- Ansible 2.11+
- Python 3.8+
- GitHub API token with repo access
- Network access to GitHub API

## License

MIT
