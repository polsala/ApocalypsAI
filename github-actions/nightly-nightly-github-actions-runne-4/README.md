# Nightly GitHub Actions Runner Health Monitor

A reusable GitHub Actions workflow that monitors the health of self-hosted runners and generates detailed reports.

## Features

- **Health Checks**: Monitors runner availability, job completion rates, and resource usage
- **Metrics Collection**: Tracks CPU, memory, disk space, and network connectivity
- **Alert Generation**: Creates issues when runners are unhealthy or underperforming
- **Historical Reporting**: Maintains a log of runner performance over time
- **Auto-Healing**: Optional cleanup of stuck runners and resource optimization

## Usage

Add this workflow to your repository to monitor your self-hosted runners:

```yaml
name: Monitor Self-Hosted Runners
on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM
  workflow_dispatch:

jobs:
  runner-health-check:
    uses: polsala/ApocalypsAI/.github/workflows/nightly-github-actions-runner-health.yml@main
    with:
      alert-threshold: 80
      cleanup-stuck-runners: true
      include-metrics: true
```

## Inputs

- `alert-threshold` (optional): Percentage threshold for job failure rate alerts (default: 80)
- `cleanup-stuck-runners` (optional): Whether to automatically clean up stuck runners (default: true)
- `include-metrics` (optional): Whether to collect detailed system metrics (default: true)

## Outputs

- `health-report`: Path to the generated health report
- `issues-created`: Number of issues created for unhealthy runners
- `runners-cleaned`: Number of runners cleaned up

## License

MIT
