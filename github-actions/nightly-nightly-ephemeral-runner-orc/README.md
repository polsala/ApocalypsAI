# Nightly Ephemeral Runner Orchestrator

Automatically provision and manage ephemeral GitHub Actions runners with health checks and cleanup.

## Features

- **Auto-provision**: Spin up runners on demand based on queue length
- **Health monitoring**: Continuous health checks with automatic recovery
- **Smart cleanup**: Remove idle runners and failed instances
- **Resource optimization**: Scale runners based on actual workload
- **Cost control**: Automatically terminate expensive runners after peak hours

## Usage

### Basic Setup

1. Add the workflow to your repository:

```yaml
name: Ephemeral Runner Orchestrator
on:
  schedule:
    - cron: '*/15 * * * *'  # Run every 15 minutes
  workflow_dispatch:

jobs:
  manage-runners:
    uses: polsala/ApocalypsAI/.github/workflows/nightly-ephemeral-runner-orchestrator.yml@main
    with:
      max-runners: 10
      min-runners: 2
      queue-threshold: 5
      idle-timeout: 30
```

### Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `max-runners` | Maximum number of runners to maintain | 10 |
| `min-runners` | Minimum number of runners to keep alive | 2 |
| `queue-threshold` | Queue length that triggers runner scaling | 5 |
| `idle-timeout` | Minutes before idle runners are terminated | 30 |
| `cost-control` | Enable cost control during off-peak hours | true |
| `peak-start` | Peak hours start time (24h format) | 09:00 |
| `peak-end` | Peak hours end time (24h format) | 17:00 |

## How It Works

1. **Queue Monitoring**: Checks GitHub Actions queue length every 15 minutes
2. **Scaling Logic**: Adds runners when queue exceeds threshold, removes when idle
3. **Health Checks**: Monitors runner health and replaces failed instances
4. **Cost Optimization**: Reduces runner count during off-peak hours
5. **Cleanup**: Removes orphaned runners and failed provisioning attempts

## Benefits

- **Reliability**: Always have enough runners for your workload
- **Cost Efficiency**: Only run what you need when you need it
- **Automation**: No manual intervention required
- **Monitoring**: Clear visibility into runner status and performance

## Requirements

- GitHub Actions permissions to manage self-hosted runners
- Access to your runner infrastructure (VMs, containers, etc.)
- Appropriate cloud provider credentials for provisioning

## Monitoring

The orchestrator provides detailed logs for:

- Runner provisioning status
- Queue length trends
- Health check results
- Cost optimization actions
- Cleanup operations

## Troubleshooting

### Runners Not Provisioning

1. Check cloud provider credentials
2. Verify runner image availability
3. Review GitHub Actions permissions

### High Costs

1. Adjust `max-runners` parameter
2. Enable `cost-control` mode
3. Review peak/off-peak timing

### Health Check Failures

1. Check runner connectivity
2. Verify runner software versions
3. Review system resource usage

## Contributing

Contributions welcome! Please:

1. Test changes in a development environment
2. Update documentation for new features
3. Add appropriate error handling
4. Follow existing code patterns

## License

MIT - see LICENSE file for details.
