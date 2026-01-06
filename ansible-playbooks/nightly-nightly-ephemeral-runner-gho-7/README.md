# Nightly Ephemeral Runner Ghost Buster

A utility to detect and clean up orphaned GitHub Actions self-hosted runners across cloud providers (AWS, Azure, GCP).

## Purpose

When using ephemeral runners, sometimes runners can become orphaned due to:
- Failed cleanup scripts
- Network issues during shutdown
- Manual intervention
- Provider API failures

This utility scans for and removes these orphaned runners to prevent resource waste and security issues.

## Features

- **Multi-cloud support**: AWS EC2, Azure VMs, GCP Compute Engine
- **Age-based cleanup**: Only removes runners older than a configurable threshold
- **Dry-run mode**: Preview what would be deleted
- **Detailed reporting**: Generates comprehensive cleanup reports
- **Safe operation**: Requires explicit confirmation before deletion

## Usage

### Prerequisites

- Ansible 2.14+
- Cloud provider CLI tools installed and configured
- Appropriate IAM permissions for your cloud provider

### Basic Usage

```bash
# Run with default settings (24h age threshold)
ansible-playbook ghost_buster.yml

# Dry run to see what would be deleted
ansible-playbook ghost_buster.yml --extra-vars "dry_run=true"

# Custom age threshold (in hours)
ansible-playbook ghost_buster.yml --extra-vars "max_age_hours=12"

# Force cleanup without confirmation
ansible-playbook ghost_buster.yml --extra-vars "force_cleanup=true"
```

### Configuration

Edit the `vars/main.yml` file to customize:

```yaml
# Maximum age in hours before a runner is considered orphaned
max_age_hours: 24

# List of GitHub organizations to scan
github_orgs:
  - "my-org"
  - "another-org"

# Cloud providers to scan (aws, azure, gcp)
cloud_providers:
  - "aws"
  - "azure"
  - "gcp"
```

## Output

The utility generates a detailed report showing:

- Total runners found per provider
- Orphaned runners identified
- Actions taken (deleted, skipped)
- Any errors encountered

## Safety Features

- **Confirmation prompts**: By default, requires manual confirmation before deletion
- **Age threshold**: Only removes runners older than the specified threshold
- **Dry-run mode**: Preview mode shows what would be deleted without making changes
- **Error handling**: Gracefully handles API failures and permission issues

## Integration with CI/CD

This utility can be integrated into your CI/CD pipeline to automatically clean up orphaned runners:

```yaml
# Example GitHub Actions workflow
name: Ephemeral Runner Cleanup
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Ansible
        uses: ansible/ansible-setup-action@v2
      - name: Run Ghost Buster
        run: |
          ansible-playbook ansible-playbooks/nightly-ephemeral-runner-ghost-buster/ghost_buster.yml
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AZURE_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
          AZURE_CLIENT_SECRET: ${{ secrets.AZURE_CLIENT_SECRET }}
          AZURE_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          AZURE_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
          GOOGLE_APPLICATION_CREDENTIALS: ${{ secrets.GOOGLE_APPLICATION_CREDENTIALS }}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
