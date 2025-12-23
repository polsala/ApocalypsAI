# Nightly Ephemeral Runner Ghost Buster

Automated cleanup of orphaned GitHub Actions self-hosted runners using Ansible.

## Overview

This utility helps maintain clean GitHub Actions environments by automatically detecting and cleaning up orphaned self-hosted runners that may have been left behind due to failed deployments, network issues, or other disruptions.

## Features

- Detects orphaned runners across multiple repositories
- Safely removes orphaned runners without affecting active ones
- Generates detailed cleanup reports
- Supports both GitHub.com and GitHub Enterprise
- Configurable cleanup policies

## Requirements

- Ansible 2.12+
- Python 3.8+
- GitHub Personal Access Token with repo access
- SSH access to runner hosts

## Installation

1. Clone this repository
2. Install required Ansible collections:
   ```bash
   ansible-galaxy collection install community.general
   ```

## Usage

### Basic Cleanup

```bash
ansible-playbook ghost_buster.yml -i inventory.ini
```

### Cleanup with Custom Policy

```bash
ansible-playbook ghost_buster.yml -i inventory.ini --extra-vars "cleanup_policy=aggressive"
```

### Dry Run (Report Only)

```bash
ansible-playbook ghost_buster.yml -i inventory.ini --extra-vars "dry_run=true"
```

## Configuration

### Inventory File

Create an `inventory.ini` file:

```ini
[runners]
runner-01 ansible_host=192.168.1.10
runner-02 ansible_host=192.168.1.11
runner-03 ansible_host=192.168.1.12

[runners:vars]
github_token=your_github_token_here
organization=your-org-name
```

### Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `github_token` | GitHub Personal Access Token | Required |
| `organization` | GitHub organization name | Required |
| `cleanup_policy` | Cleanup policy: `conservative`, `moderate`, `aggressive` | `moderate` |
| `dry_run` | Report only, no actual cleanup | `false` |
| `max_age_hours` | Maximum age of runners before cleanup | `24` |

## Cleanup Policies

- **conservative**: Only remove runners that are definitely orphaned and older than 48 hours
- **moderate**: Remove orphaned runners older than 24 hours (default)
- **aggressive**: Remove any orphaned runners, regardless of age

## Reports

After each run, a detailed report is generated showing:

- Total runners detected
- Active runners
- Orphaned runners found
- Cleanup actions performed
- Any errors encountered

## Safety Features

- Always performs dry-run analysis first
- Validates runner status before removal
- Maintains audit trail of all actions
- Supports rollback in case of issues
- Respects GitHub rate limits

## Monitoring

The utility includes health checks and can be integrated with monitoring systems:

- Exit codes indicate success/failure
- JSON output for programmatic consumption
- Integration with Prometheus/Grafana

## Troubleshooting

### Common Issues

1. **Authentication Failed**: Verify your GitHub token has sufficient permissions
2. **Network Connectivity**: Ensure SSH access to runner hosts
3. **Rate Limiting**: The tool respects GitHub rate limits automatically

### Debug Mode

Enable verbose output:

```bash
ansible-playbook ghost_buster.yml -i inventory.ini -vvv
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Test your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions, please:

1. Check the troubleshooting section
2. Review existing issues
3. Create a new issue with detailed information

## Security

- Never commit GitHub tokens to version control
- Use environment variables or Ansible vault for secrets
- Regularly rotate access tokens
- Monitor GitHub API usage

## Changelog

### v1.0.0
- Initial release
- Basic orphaned runner detection
- Conservative cleanup policy
- Detailed reporting

### v1.1.0
- Added multiple cleanup policies
- Dry-run mode
- Enhanced error handling
- Improved reporting format

---

**Note**: This utility is designed for automated nightly cleanup. Always test in a non-production environment first.
