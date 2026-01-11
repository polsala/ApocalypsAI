# Nightly Ephemeral Runner Ghost Buster

A Bash utility to detect and clean up orphaned GitHub Actions self-hosted runners across AWS, Azure, and GCP.

## Features

- Detects runners registered to a GitHub repo but not running on any cloud instance.
- Cleans up orphaned instances by age (default 24 hours).
- Supports AWS EC2, Azure VMs, and GCP Compute Engine.
- Generates a detailed report.

## Usage

```bash
# Run the full cleanup
./ghost_buster.sh --repo-owner myorg --repo-name myrepo --cloud aws --age 24

# Dry run to see what would be deleted
./ghost_buster.sh --repo-owner myorg --repo-name myrepo --cloud aws --dry-run

# Cleanup by age only (no orphan detection)
./ghost_buster.sh --cloud aws --age 24
```

## Prerequisites

- AWS CLI, Azure CLI, or gcloud CLI configured with appropriate permissions.
- `jq` installed for JSON parsing.
- GitHub token with `repo` scope exported as `GITHUB_TOKEN`.

## Output

The script outputs a JSON report to `ghost_buster_report.json` detailing:

- Detected orphaned runners.
- Instances cleaned up.
- Summary statistics.
