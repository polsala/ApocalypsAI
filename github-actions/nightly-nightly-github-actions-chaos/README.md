# Nightly Chaos Chaos Workflow

This GitHub Actions workflow introduces controlled chaos into your CI pipelines to test resilience and observability. It randomly injects delays, failures, and resource constraints to ensure your workflows can handle unexpected conditions.

## Features

- **Random Delays**: Introduces unpredictable delays to simulate network latency
- **Controlled Failures**: Randomly fails steps to test error handling
- **Resource Constraints**: Simulates CPU and memory constraints
- **Observability**: Logs chaos events for analysis
- **Configurable**: Easy to enable/disable and tune chaos levels

## Usage

1. Copy the `chaos-chaos.yml` workflow file to your repository's `.github/workflows/` directory
2. Adjust the chaos configuration in the workflow file
3. Enable the workflow by setting `CHAOS_ENABLED` to `true`

## Configuration

- `CHAOS_ENABLED`: Set to `true` to enable chaos (default: `false`)
- `CHAOS_PROBABILITY`: Probability of chaos events (0.0 - 1.0, default: 0.3)
- `MAX_DELAY_SECONDS`: Maximum delay in seconds (default: 30)
- `MAX_CPU_LOAD`: Maximum CPU load percentage (default: 80)
- `MAX_MEMORY_USAGE`: Maximum memory usage percentage (default: 70)

## Example

```yaml
env:
  CHAOS_ENABLED: true
  CHAOS_PROBABILITY: 0.5
  MAX_DELAY_SECONDS: 60
  MAX_CPU_LOAD: 90
  MAX_MEMORY_USAGE: 80
```

## Safety

This workflow is designed to be safe:
- Chaos is disabled by default
- All chaos events are logged for transparency
- Resource constraints are temporary and self-limiting
- No actual data corruption or permanent damage occurs

## Contributing

Feel free to submit issues and enhancement requests!

## License

This workflow is provided as-is for educational and testing purposes.
