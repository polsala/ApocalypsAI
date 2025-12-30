# Nightly Ephemeral Runner Ghost Buster

A utility to detect and clean up orphaned GitHub Actions self-hosted runners across cloud providers (AWS, Azure, GCP).

## Overview

When using ephemeral self-hosted runners, sometimes runners can become orphaned due to:
- Failed cleanup scripts
- Network issues during shutdown
- Manual intervention
- Provider API failures

This tool scans for and removes these orphaned runners to prevent resource waste and security issues.

## Features

- **Multi-cloud support**: AWS EC2, Azure VMs, GCP Compute Engine
- **Safe detection**: Only removes runners that are truly orphaned
- **Detailed reporting**: Generates comprehensive cleanup reports
- **Dry-run mode**: Test before making changes
- **Age-based filtering**: Only clean up runners older than a specified threshold

## Requirements

- Ansible 2.12+
- Cloud provider CLI tools (aws, az, gcloud)
- Appropriate cloud provider credentials
- GitHub Actions runner labels for identification

## Usage

### Basic Cleanup

```bash
ansible-playbook ghost_buster.yml -i inventory.ini
```

### Dry Run (Recommended First)

```bash
ansible-playbook ghost_buster.yml -i inventory.ini --extra-vars "dry_run=true"
```

### Custom Age Threshold

```bash
ansible-playbook ghost_buster.yml -i inventory.ini --extra-vars "max_age_hours=2"
```

### Provider-Specific Cleanup

```bash
# Only AWS
ansible-playbook ghost_buster.yml -i inventory.ini --extra-vars "providers=['aws']"

# Only Azure and GCP
ansible-playbook ghost_buster.yml -i inventory.ini --extra-vars "providers=['azure', 'gcp']"
```

## Configuration

### Inventory

Create an `inventory.ini` file:

```ini
[aws]
aws-runner-1 ansible_host=1.2.3.4
aws-runner-2 ansible_host=5.6.7.8

[azure]
azure-runner-1 ansible_host=9.10.11.12

[gcp]
gcp-runner-1 ansible_host=13.14.15.16
```

### Variables

Set variables in `vars/main.yml` or via `--extra-vars`:

```yaml
# Maximum age in hours for runners to be considered for cleanup
max_age_hours: 4

# List of providers to check (aws, azure, gcp)
providers:
  - aws
  - azure
  - gcp

# GitHub Actions runner labels to identify ephemeral runners
runner_labels:
  - "ephemeral"
  - "self-hosted"

# Dry run mode (true/false)
dry_run: false
```

## Output

The tool generates a detailed report showing:

- **Found runners**: All detected runners with their status
- **Orphaned runners**: Runners marked for cleanup
- **Cleanup actions**: What will be/was removed
- **Summary**: Total resources cleaned up

## Safety Features

- **Verification**: Confirms runners are not currently running jobs
- **Age filtering**: Only removes runners older than the threshold
- **Provider validation**: Ensures cloud resources exist before cleanup
- **Rollback info**: Provides details for manual restoration if needed

## Integration

This tool can be integrated into your CI/CD pipeline to run automatically:

```yaml
name: Ghost Buster
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Ghost Buster
        run: |
          ansible-playbook ghost_buster.yml -i inventory.ini
```

## Troubleshooting

### Common Issues

1. **Authentication failures**: Ensure cloud provider credentials are properly configured
2. **Permission denied**: Verify IAM roles have necessary permissions for resource deletion
3. **Network timeouts**: Check connectivity to cloud provider APIs

### Debug Mode

Enable verbose output for troubleshooting:

```bash
ansible-playbook ghost_buster.yml -i inventory.ini -vvv
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details.
