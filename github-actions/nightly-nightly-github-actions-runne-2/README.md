# Nightly GitHub Actions Runner Auditor

A GitHub Actions workflow that audits and reports on runner usage across all repositories in an organization. This utility helps identify underutilized runners, track usage patterns, and optimize CI/CD costs.

## Features

- **Organization-wide runner audit**: Scans all repositories for GitHub Actions workflows
- **Runner usage analysis**: Tracks which runners are being used and how frequently
- **Cost optimization insights**: Identifies expensive runners that could be replaced with cheaper alternatives
- **Security compliance**: Flags workflows using self-hosted runners without proper security measures
- **Performance metrics**: Measures workflow execution times and identifies bottlenecks

## Usage

This is a reusable workflow that can be included in any repository to audit runner usage across your organization.

### Basic Usage

```yaml
name: Organization Runner Audit
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  workflow_dispatch:

jobs:
  audit-runners:
    uses: polsala/ApocalypsAI/.github/workflows/nightly-github-actions-runner-auditor.yml@main
    with:
      github-token: ${{ secrets.GITHUB_TOKEN }}
      organization: your-org-name
      include-private: true
      cost-analysis: true
    secrets:
      github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `github-token` | GitHub token with repo access | Required |
| `organization` | Organization name to audit | Required |
| `include-private` | Include private repositories | `false` |
| `cost-analysis` | Enable cost analysis features | `false` |
| `days-to-analyze` | Number of days to analyze | `30` |
| `output-format` | Output format (json, markdown) | `markdown` |

## Output

The workflow generates a comprehensive audit report including:

- Runner usage statistics by repository
- Cost analysis and optimization recommendations
- Security compliance status
- Performance metrics and bottlenecks
- Unused runner identification

## Security

- Uses GitHub's official REST API with proper authentication
- No secrets are logged or exposed
- Respects repository permissions and visibility settings
- Implements rate limiting to avoid API abuse

## Dependencies

- GitHub Actions
- GitHub REST API v3
- No external dependencies required

## License

MIT
