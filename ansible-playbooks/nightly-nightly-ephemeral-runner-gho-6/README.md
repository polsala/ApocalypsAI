# Nightly Ephemeral Runner Ghost Buster

A utility to detect and clean up orphaned GitHub Actions self-hosted runners across AWS, Azure, and GCP.

## Purpose

When using ephemeral runners, sometimes runners can become orphaned due to:
- Failed cleanup scripts
- Network timeouts during shutdown
- Manual intervention or system errors

This utility scans your cloud environments for instances that were created as GitHub runners but are no longer registered with GitHub, then safely terminates them.

## Features

- **Multi-cloud support**: AWS EC2, Azure VMs, and GCP Compute Engine
- **Safe detection**: Only targets instances with GitHub runner tags/metadata
- **Age-based cleanup**: Configurable age thresholds for cleanup
- **Detailed reporting**: Generates comprehensive cleanup reports
- **Dry-run mode**: Test runs without making changes

## Requirements

- Ansible 2.12+
- Cloud provider CLI tools (aws, az, gcloud) with appropriate permissions
- GitHub API access token for runner registration checks

## Usage

### Basic Cleanup

```bash
ansible-playbook ghost_buster.yml -i inventory.ini
```

### Dry Run (No Changes)

```bash
ansible-playbook ghost_buster.yml -i inventory.ini --extra-vars "dry_run=true"
```

### Custom Age Threshold

```bash
ansible-playbook ghost_buster.yml -i inventory.ini --extra-vars "max_age_hours=2"
```

## Configuration

Edit `vars/main.yml` to configure:

- `github_token`: Your GitHub API token
- `max_age_hours`: Maximum age before cleanup (default: 4 hours)
- `cloud_providers`: Which providers to scan
- `tags_to_check`: Instance tags that identify GitHub runners

## Output

The utility generates a detailed report showing:

- Total instances scanned per provider
- Orphaned runners found
- Instances scheduled for cleanup
- Cleanup actions performed
- Any errors encountered

## Safety Features

- Only targets instances with GitHub runner identification tags
- Respects instance protection settings
- Provides detailed logging for audit trails
- Supports dry-run mode for testing

## Integration

This utility is designed to run as part of your nightly maintenance workflows to ensure clean, cost-effective runner management.
