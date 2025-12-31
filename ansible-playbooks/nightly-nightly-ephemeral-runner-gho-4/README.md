# Nightly Ephemeral Runner Ghost Buster

A utility to detect and clean up orphaned GitHub Actions self-hosted runners across AWS, Azure, and GCP.

## Purpose

When using ephemeral self-hosted runners, sometimes runners can become orphaned due to:
- Failed cleanup scripts
- Network timeouts during termination
- Manual intervention that breaks the cleanup flow
- Provider API rate limits or temporary outages

This utility scans for these orphaned runners and safely terminates them.

## Features

- **Multi-cloud support**: AWS EC2, Azure VMs, and GCP Compute Engine
- **Safe detection**: Only targets instances that are confirmed to be orphaned runners
- **Comprehensive reporting**: Generates detailed reports of cleanup actions
- **Dry-run mode**: Test the utility before making actual changes
- **Age-based filtering**: Only clean up runners older than a specified threshold

## Usage

### Prerequisites

- Ansible 2.12+
- Cloud provider CLI tools installed and configured
- Appropriate IAM permissions for instance management

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

## Configuration

### Inventory

Update `inventory.ini` with your cloud provider credentials and regions:

```ini
[aws]
aws_region=us-east-1

[azure]
az_subscription_id=your-subscription-id
az_resource_group=your-resource-group

[gcp]
gcp_project_id=your-project-id
gcp_zone=us-central1-a
```

### Variables

Edit `vars/main.yml` to customize:

- `max_age_hours`: Maximum age of runners before cleanup (default: 4 hours)
- `tag_prefix`: Tag prefix used to identify ephemeral runners (default: "ephemeral-runner")
- `cleanup_tags`: Additional tags to apply during cleanup

## Reports

After each run, a detailed report is generated at `reports/ghost_buster_report_YYYY-MM-DD_HH-MM-SS.json` containing:

- Detected orphaned runners
- Cleanup actions taken
- Any errors encountered
- Summary statistics

## Safety Features

- **Confirmation prompts**: Interactive confirmation before terminating instances
- **Backup tagging**: Adds cleanup metadata tags before termination
- **Error handling**: Graceful handling of API failures and permission issues
- **Logging**: Comprehensive logging for audit trails

## Integration

This utility can be integrated into your CI/CD pipeline to run automatically:

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

1. **Permission Denied**: Ensure your cloud provider credentials have sufficient permissions
2. **API Rate Limits**: The utility includes built-in retry logic, but you may need to adjust rate limits
3. **Network Timeouts**: Increase timeout values in the playbook if needed

### Debug Mode

Enable verbose logging:

```bash
ansible-playbook ghost_buster.yml -i inventory.ini -v
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Test your changes thoroughly
4. Submit a pull request

## License

MIT License - see LICENSE file for details.
