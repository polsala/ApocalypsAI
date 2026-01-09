# Nightly GitHub Actions Runner Health Checker

A GitHub Actions workflow that monitors and reports on the health of self-hosted runners across multiple repositories in an organization.

## Features

- **Multi-repository runner monitoring**: Checks runner health across all repositories in an organization
- **Health status reporting**: Generates detailed reports on runner availability, job success rates, and performance metrics
- **Automated alerts**: Creates issues when runners are offline or experiencing problems
- **Performance insights**: Tracks runner utilization and identifies bottlenecks
- **Historical tracking**: Maintains health history for trend analysis

## Usage

This is a reusable workflow that can be included in any repository to monitor runner health.

### Basic Usage

```yaml
name: Monitor Runner Health

on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM
  workflow_dispatch:

jobs:
  check-runner-health:
    uses: polsala/ApocalypsAI/.github/workflows/nightly-github-actions-runner-health-checker.yml@main
    with:
      github-token: ${{ secrets.GITHUB_TOKEN }}
      organization: "your-org-name"
      alert-threshold: 5  # Create issues if more than 5 runners are offline
```

### Advanced Configuration

```yaml
jobs:
  check-runner-health:
    uses: polsala/ApocalypsAI/.github/workflows/nightly-github-actions-runner-health-checker.yml@main
    with:
      github-token: ${{ secrets.GITHUB_TOKEN }}
      organization: "your-org-name"
      alert-threshold: 3
      include-repositories: "repo1,repo2,repo3"
      exclude-repositories: "repo4,repo5"
      report-format: "markdown"  # or "json"
      create-issues: true
      dry-run: false
```

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `github-token` | Yes | - | GitHub token with repo access |
| `organization` | Yes | - | Organization name to monitor |
| `alert-threshold` | No | 3 | Number of offline runners before creating an issue |
| `include-repositories` | No | All repos | Comma-separated list of repositories to include |
| `exclude-repositories` | No | None | Comma-separated list of repositories to exclude |
| `report-format` | No | markdown | Output format (markdown or json) |
| `create-issues` | No | true | Whether to create issues for unhealthy runners |
| `dry-run` | No | false | Run without creating issues or making changes |

## Outputs

| Output | Description |
|--------|-------------|
| `health-report` | Path to the generated health report |
| `unhealthy-runners-count` | Number of unhealthy runners detected |
| `total-runners-count` | Total number of runners monitored |

## Example Report

```
# GitHub Actions Runner Health Report

**Organization**: your-org-name
**Generated**: 2024-01-15 10:30:00 UTC
**Time Range**: Last 24 hours

## Summary
- Total Runners: 15
- Healthy Runners: 12
- Unhealthy Runners: 3
- Success Rate: 94.2%

## Unhealthy Runners

| Repository | Runner Name | Status | Last Seen | Issues |
|------------|-------------|--------|-----------|--------|
| repo1 | runner-001 | Offline | 2024-01-15 08:15:00 | No recent activity |
| repo2 | runner-005 | Offline | 2024-01-15 07:45:00 | No recent activity |
| repo3 | runner-009 | Busy | 2024-01-15 10:25:00 | High CPU usage |

## Performance Metrics

### Job Success Rates by Repository
- repo1: 98.5% (124/126 jobs)
- repo2: 92.1% (89/97 jobs)
- repo3: 95.7% (156/163 jobs)

### Average Job Duration
- repo1: 4.2 minutes
- repo2: 6.8 minutes
- repo3: 3.9 minutes

## Recommendations
1. Investigate runner-001 and runner-005 for potential hardware issues
2. Consider scaling up runners for repo2 due to lower success rate
3. Monitor runner-009 for resource constraints
```

## Security

- Uses GitHub's built-in secrets management
- Minimal permissions required (repo access only)
- No external dependencies or network calls
- All data stays within GitHub ecosystem

## Contributing

1. Fork the repository
2. Create a feature branch
3. Test your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions, please:
1. Check the existing issues
2. Create a new issue with detailed information
3. Include the workflow run logs when reporting problems
