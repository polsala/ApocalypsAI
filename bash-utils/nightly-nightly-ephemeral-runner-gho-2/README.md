# Nightly Ephemeral Runner Ghostbuster

A lightweight Bash utility to detect and clean up orphaned GitHub Actions self-hosted runners across AWS, Azure, and GCP. Designed for environments where ephemeral runners are provisioned dynamically but may be left behind due to failures or scaling issues.

## Features

- **Multi-cloud support**: Works with AWS EC2, Azure VMs, and GCP Compute Engine
- **Orphan detection**: Identifies runners that are no longer registered with GitHub
- **Safe cleanup**: Dry-run mode and confirmation prompts before deletion
- **Comprehensive reporting**: Generates detailed reports of findings and actions taken
- **Integration ready**: Designed to work with existing Ansible playbooks and CI/CD pipelines

## Requirements

- Bash 4.0+
- Cloud CLI tools installed and configured:
  - AWS CLI (for AWS EC2)
  - Azure CLI (for Azure VMs)
  - gcloud CLI (for GCP Compute Engine)
- GitHub CLI (gh) for checking runner registration status

## Installation

```bash
# Clone or download the script
chmod +x ghostbuster.sh
```

## Usage

### Basic Usage

```bash
# Run in dry-run mode (recommended first run)
./ghostbuster.sh --dry-run

# Run with actual cleanup
./ghostbuster.sh --cleanup

# Run for specific cloud provider only
./ghostbuster.sh --provider aws --cleanup
```

### Advanced Options

```bash
# Generate detailed report
./ghostbuster.sh --cleanup --report report.txt

# Set custom age threshold (default: 2 hours)
./ghostbuster.sh --cleanup --age-threshold 3600

# Skip confirmation prompts (for automation)
./ghostbuster.sh --cleanup --yes

# Verbose output
./ghostbuster.sh --cleanup --verbose
```

### Command Line Options

- `--dry-run`: Show what would be deleted without actually deleting
- `--cleanup`: Perform actual cleanup (requires confirmation unless --yes is used)
- `--provider <aws|azure|gcp>`: Limit to specific cloud provider
- `--age-threshold <seconds>`: Only consider runners older than this threshold
- `--report <file>`: Save detailed report to file
- `--yes`: Skip confirmation prompts
- `--verbose`: Enable verbose logging
- `--help`: Show help message

## Configuration

The script reads configuration from environment variables:

```bash
# GitHub organization/repo (required)
export GITHUB_ORG="your-org"
export GITHUB_REPO="your-repo"  # Optional, if checking repo runners

# Age threshold in seconds (default: 7200 = 2 hours)
export AGE_THRESHOLD=7200

# Cloud provider selection (default: all)
export CLOUD_PROVIDERS="aws,azure,gcp"
```

## Output

The script generates output in multiple formats:

1. **Console output**: Real-time progress and summary
2. **JSON report**: Machine-readable details for integration
3. **Text report**: Human-readable summary with recommendations

### Sample Output

```
=== Ephemeral Runner Ghostbuster Report ===

Scanning cloud providers: AWS, Azure, GCP
GitHub Organization: your-org
Age threshold: 2 hours

Found 15 total instances
Found 8 registered runners
Found 7 orphaned instances

Orphaned instances:
- aws-runner-001 (EC2, 3 hours old, i-1234567890abcdef0)
- azure-runner-002 (VM, 4 hours old, /subscriptions/.../resourceGroups/...)
- gcp-runner-003 (Compute Engine, 2.5 hours old, projects/.../zones/...)

Cleanup actions taken: 7 instances terminated

Report saved to: ghostbuster_report_20241201_143022.txt
```

## Integration with CI/CD

### GitHub Actions

```yaml
name: Ghostbuster Cleanup
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Cloud CLIs
        run: |
          # Install and configure your cloud CLIs here
      - name: Run Ghostbuster
        run: |
          ./ghostbuster.sh --cleanup --yes --report ghostbuster_report.txt
      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: ghostbuster-report
          path: ghostbuster_report_*.txt
```

### Ansible Integration

The script is designed to work alongside existing Ansible playbooks. You can call it from Ansible:

```yaml
- name: Run Ghostbuster cleanup
  shell: ./ghostbuster.sh --cleanup --yes --report {{ report_path }}
  args:
    chdir: /path/to/ghostbuster
```

## Safety Features

1. **Dry-run mode**: Always test first to see what would be deleted
2. **Age threshold**: Only considers runners older than the specified threshold
3. **Confirmation prompts**: Requires explicit confirmation before deletion (unless --yes is used)
4. **Detailed logging**: Every action is logged with timestamps and reasoning
5. **Rollback information**: Provides instance IDs and details for manual recovery if needed

## Troubleshooting

### Common Issues

1. **Authentication errors**: Ensure cloud CLIs are configured with proper credentials
2. **GitHub API rate limits**: The script includes built-in rate limiting
3. **Missing dependencies**: Install required CLI tools as specified in Requirements

### Debug Mode

Enable verbose logging for troubleshooting:

```bash
./ghostbuster.sh --cleanup --verbose
```

### Log Files

The script creates timestamped log files in the current directory:

- `ghostbuster_debug_YYYYMMDD_HHMMSS.log` - Debug logs
- `ghostbuster_report_YYYYMMDD_HHMMSS.txt` - Human-readable report
- `ghostbuster_report_YYYYMMDD_HHMMSS.json` - Machine-readable report

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Update documentation
6. Submit a pull request

## License

This utility is part of the ApocalypsAI project and follows the same license terms.

## Support

For issues, questions, or contributions, please use the GitHub repository's issue tracker.

---

*Built with ❤️ by the ApocalypsAI collective*
