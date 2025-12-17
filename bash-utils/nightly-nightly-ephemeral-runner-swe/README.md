## Nightly Ephemeral Runner Sweeper

A lightweight Bash utility to discover and clean up orphaned ephemeral GitHub self-hosted runners across your organization.

### Features
- Lists all runners in an organization
- Identifies orphaned runners (no recent activity)
- Provides dry-run and cleanup modes
- Generates a cleanup report

### Usage
```bash
# Dry run (recommended first)
./ephemeral_runner_sweeper.sh --org my-org --dry-run

# Cleanup orphaned runners
./ephemeral_runner_sweeper.sh --org my-org --cleanup

# Set custom inactivity threshold (hours, default: 24)
./ephemeral_runner_sweeper.sh --org my-org --threshold 48 --cleanup
```

### Prerequisites
- `curl` and `jq` installed
- GitHub token with `admin:org` scope
- Set `GITHUB_TOKEN` environment variable

### Environment Variables
- `GITHUB_TOKEN`: GitHub API token
- `GITHUB_API_URL`: GitHub API URL (default: https://api.github.com)

### Output
- Lists all runners with status and last activity
- Shows orphaned runners that would be removed
- Generates `cleanup_report.md` with details

### Safety
- Always run with `--dry-run` first
- The script will not proceed without a valid GitHub token
- Orphaned runners are defined as those with no activity for the specified threshold
