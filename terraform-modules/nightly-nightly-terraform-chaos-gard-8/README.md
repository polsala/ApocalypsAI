# Nightly Terraform Chaos Garden Orchestrator

A whimsical-yet-useful Terraform module that creates a chaos garden orchestrator for testing infrastructure resilience. Inspired by the chaos engineering principles, this module helps you build a controlled environment where you can practice chaos engineering on your cloud resources.

## Features

- **Chaos Scenarios**: Pre-configured chaos scenarios including network latency, resource deletion, and service disruption
- **Whimsical Naming**: Uses whimsical names for chaos experiments (e.g., "Chaos Goblin", "Entropy Sprite")
- **Safety Controls**: Built-in safety controls to prevent accidental damage to production environments
- **Monitoring**: Comprehensive monitoring and alerting for chaos experiments
- **Rollback**: Automatic rollback mechanisms for failed experiments

## Usage

```hcl
module "chaos_garden" {
  source = "./modules/chaos_garden"

  # Basic configuration
  environment = "staging"
  region      = "us-west-2"

  # Chaos scenarios to enable
  chaos_scenarios = [
    "network_latency",
    "resource_deletion",
    "service_disruption"
  ]

  # Safety controls
  max_concurrent_experiments = 3
  experiment_duration        = "30m"
  rollback_enabled          = true

  # Monitoring
  enable_monitoring = true
  alert_email       = "ops@example.com"
}
```

## Providers

This module supports multiple cloud providers:
- AWS
- Azure
- Google Cloud Platform

## Outputs

- `chaos_garden_url`: URL to access the chaos garden dashboard
- `experiment_results`: Results of chaos experiments
- `monitoring_dashboard_url`: URL to the monitoring dashboard

## Safety Guidelines

1. **Never run in production**: This module is designed for testing environments only
2. **Start small**: Begin with simple chaos scenarios and gradually increase complexity
3. **Monitor closely**: Always monitor your systems during chaos experiments
4. **Have a rollback plan**: Ensure you can quickly revert any changes if needed
5. **Learn and adapt**: Use the results to improve your system's resilience

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

## License

This module is licensed under the MIT License. See [LICENSE](LICENSE) for more information.

---

*Remember: With great power comes great responsibility. Use chaos engineering wisely!*
