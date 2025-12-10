# Nightly GitHub Chaos Workflow

A reusable GitHub Actions workflow that introduces controlled chaos testing into your CI/CD pipelines to improve system resilience.

## Features

- **Controlled Chaos**: Introduces random failures, delays, and resource constraints
- **Configurable**: Easy to customize chaos parameters per environment
- **Safe**: Only runs on non-production branches by default
- **Reusable**: Use across multiple repositories with a single include

## Usage

Add this to your workflow file:

```yaml
name: Chaos Testing

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  chaos-test:
    uses: polsala/ApocalypsAI/.github/workflows/nightly-github-chaos-workflow.yml@main
    with:
      chaos-level: "medium"
      target-environment: "staging"
      max-failure-rate: 20
    secrets:
      github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Parameters

- `chaos-level`: "low", "medium", or "high" (default: "medium")
- `target-environment`: Environment to apply chaos to (default: "staging")
- `max-failure-rate`: Maximum percentage of tests that can fail before pipeline fails (default: 20)

## Chaos Events

- **Network Latency**: Adds random delays to network requests
- **Random Failures**: Randomly fails a percentage of test runs
- **Resource Constraints**: Limits CPU/memory for test containers
- **Time Distortion**: Speeds up or slows down time perception

## Safety

- Only runs on non-production branches by default
- Can be disabled by setting `chaos-enabled` to false
- All chaos events are logged for debugging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Test your changes
4. Submit a pull request

## License

MIT
