# Nightly Chaos Recovery Oracle

A whimsical GitHub Actions workflow that simulates system chaos (like the legendary "ApocalypsAI" chaos orchestrators) and automatically recovers with playful diagnostics. Perfect for testing resilience in a fun, low-stakes environment.

## Features
- Simulates random failures (network hiccups, resource spikes, service disruptions)
- Generates humorous diagnostic reports
- Automatically recovers and validates system health
- Customizable chaos scenarios with YAML configuration

## Usage
Add this workflow to your repository under `.github/workflows/chaos_recovery.yml` to run nightly chaos simulations.

## Configuration
Create a `chaos_config.yml` in your repository root to define chaos scenarios:
```yaml
scenarios:
  - type: network_latency
    probability: 0.3
    max_delay: 5s
  - type: resource_spike
    probability: 0.2
    cpu_percent: 80
```

## Outputs
- `chaos_report.md` - A whimsical report of what went wrong and how it was fixed
- `recovery_status` - Boolean indicating successful recovery

## Contributing
Feel free to extend the chaos scenarios or improve the diagnostic humor! Add new scenario types in `src/scenarios.yml`.

## License
MIT
