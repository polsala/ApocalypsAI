# Nightly Workflow Chaos Orchestrator

A whimsical-yet-useful GitHub Actions workflow that injects controlled chaos into your CI/CD pipelines to test resilience and failure handling.

## Features

- **Chaos Injection**: Randomly introduces failures, delays, and resource constraints
- **Resilience Testing**: Ensures your workflows can handle unexpected failures
- **Configurable Chaos**: Customize chaos levels and types via workflow inputs
- **Safe Defaults**: Chaos is disabled by default - opt-in when ready!
- **Detailed Reporting**: Generates chaos reports with actionable insights

## Usage

Add this workflow to your repository to test the resilience of your existing workflows:

```yaml
name: Chaos Testing

on:
  workflow_dispatch:
    inputs:
      chaos_level:
        description: 'Chaos level (1-10)'
        required: false
        default: '5'
        type: string
      chaos_types:
        description: 'Types of chaos to inject (comma-separated)'
        required: false
        default: 'network,cpu,memory,disk'
        type: string

jobs:
  chaos-orchestrator:
    uses: polsala/ApocalypsAI/.github/workflows/nightly-workflow-chaos-orchestrator.yml@main
    with:
      chaos_level: ${{ github.event.inputs.chaos_level }}
      chaos_types: ${{ github.event.inputs.chaos_types }}
    secrets: inherit
```

## Chaos Types

- **network**: Introduces network latency and packet loss
- **cpu**: Spawns CPU-intensive processes
- **memory**: Consumes available memory
- **disk**: Fills disk space and introduces I/O delays
- **time**: Manipulates system time
- **random**: Random failures and unexpected behavior

## Safety Features

- Chaos is disabled by default (set `chaos_level` to 0)
- All chaos effects are temporary and cleaned up after the workflow
- Detailed logging for debugging and analysis
- Fallback mechanisms to ensure workflow completion

## Contributing

1. Fork the repository
2. Create a feature branch
3. Test your changes thoroughly
4. Submit a pull request

## License

MIT License - see LICENSE file for details.
