# Nightly Workflow Chaos Orchestrator

A whimsical-yet-useful GitHub Actions reusable workflow that injects controlled chaos into your CI/CD pipelines to test resilience and observability.

## Features

- **Controlled Chaos**: Randomly introduces latency, failures, and resource constraints
- **Observability**: Generates detailed chaos reports with metrics
- **Configurable**: Easy to enable/disable and tune chaos levels
- **Safe**: Only runs on non-production branches by default
- **Reusable**: Works across multiple repositories and workflows

## Usage

### Basic Usage

```yaml
jobs:
  chaos-test:
    uses: polsala/ApocalypsAI/.github/workflows/nightly-workflow-chaos-orchestrator.yml@main
    with:
      chaos-level: "medium"
      target-branch: "main"
```

### Advanced Configuration

```yaml
jobs:
  chaos-test:
    uses: polsala/ApocalypsAI/.github/workflows/nightly-workflow-chaos-orchestrator.yml@main
    with:
      chaos-level: "high"
      target-branch: "develop"
      enable-network-chaos: true
      enable-resource-chaos: true
      enable-time-chaos: true
      chaos-duration: "300"  # 5 minutes in seconds
      report-format: "markdown"
```

## Inputs

| Input | Description | Default | Required |
|-------|-------------|---------|----------|
| `chaos-level` | Level of chaos to inject (low/medium/high) | `medium` | No |
| `target-branch` | Branch to target for chaos testing | `main` | No |
| `enable-network-chaos` | Enable network latency and packet loss | `true` | No |
| `enable-resource-chaos` | Enable CPU and memory stress testing | `true` | No |
| `enable-time-chaos` | Enable time manipulation chaos | `false` | No |
| `chaos-duration` | Duration of chaos in seconds | `180` | No |
| `report-format` | Format of the chaos report (markdown/json) | `markdown` | No |

## Outputs

| Output | Description |
|--------|-------------|
| `chaos-report` | Path to the generated chaos report |
| `chaos-metrics` | JSON string containing chaos metrics |

## Chaos Scenarios

### Low Chaos
- 100ms network latency
- 5% packet loss
- 20% CPU utilization increase
- 100MB memory allocation

### Medium Chaos
- 500ms network latency
- 15% packet loss
- 50% CPU utilization increase
- 500MB memory allocation

### High Chaos
- 1000ms network latency
- 25% packet loss
- 80% CPU utilization increase
- 1GB memory allocation

## Safety Features

- Only runs on specified branches (default: main)
- Respects repository protection rules
- Automatically cleans up chaos after duration
- Generates rollback instructions if needed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Test your changes locally
4. Submit a pull request

## License

MIT License - see LICENSE file for details.
