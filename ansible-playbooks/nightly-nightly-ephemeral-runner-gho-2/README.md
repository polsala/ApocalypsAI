# Nightly Ephemeral Runner Ghost Buster

Automated cleanup of orphaned GitHub Actions self-hosted runners using Ansible.

## Overview

This utility helps maintain clean GitHub Actions environments by automatically detecting and removing orphaned self-hosted runners that may have been left behind due to failed deployments, network issues, or other disruptions.

## Features

- Detects orphaned runners across multiple repositories
- Safely removes runners with confirmation prompts
- Generates detailed cleanup reports
- Supports both single-repository and organization-wide cleanup
- Uses Ansible for reliable, idempotent operations

## Prerequisites

- Ansible 2.12 or later
- GitHub Personal Access Token with `admin:org` scope for organization cleanup
- SSH access to runner hosts (if using SSH-based runner management)

## Installation

1. Clone this repository or copy the playbook files
2. Install required Ansible collections:
   ```bash
   ansible-galaxy collection install community.general
   ```
3. Configure your inventory and variables

## Usage

### Single Repository Cleanup

```bash
ansible-playbook ghost_buster.yml -i inventory.ini -e "repo_owner=myorg repo_name=myrepo"
```

### Organization-wide Cleanup

```bash
ansible-playbook ghost_buster.yml -i inventory.ini -e "org_name=myorg cleanup_mode=organization"
```

### Dry Run (Preview Only)

```bash
ansible-playbook ghost_buster.yml -i inventory.ini --check --diff
```

## Configuration

### Inventory

Create an `inventory.ini` file:

```ini
[runners]
runner1.example.com ansible_host=192.168.1.10
runner2.example.com ansible_host=192.168.1.11
runner3.example.com ansible_host=192.168.1.12
```

### Variables

Set variables in `vars/main.yml` or via command line:

- `github_token`: GitHub Personal Access Token
- `repo_owner`: Repository owner (for single repo mode)
- `repo_name`: Repository name (for single repo mode)
- `org_name`: Organization name (for org mode)
- `cleanup_mode`: `repository` or `organization`
- `confirm_cleanup`: `true` to require confirmation, `false` for automatic cleanup

## Safety Features

- Dry run mode for previewing changes
- Confirmation prompts before actual deletion
- Detailed logging of all operations
- Rollback capabilities for failed operations
- Validation of runner status before removal

## Monitoring

The playbook generates a detailed report after each run, including:

- List of detected orphaned runners
- Actions taken (removed, skipped, failed)
- Timestamps for all operations
- Any errors encountered

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Ensure your GitHub token has the correct scopes
2. **Network Connectivity**: Verify SSH access to runner hosts
3. **Permission Issues**: Check that the runner service account has appropriate permissions

### Debug Mode

Run with verbose output for debugging:

```bash
ansible-playbook ghost_buster.yml -i inventory.ini -vvv
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Test your changes thoroughly
4. Submit a pull request

## License

MIT License - see LICENSE file for details.
