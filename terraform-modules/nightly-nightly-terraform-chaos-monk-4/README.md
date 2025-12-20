# Terraform Chaos Monkey Module

A whimsical-yet-useful Terraform module that introduces controlled chaos into your cloud infrastructure to test resilience and improve system robustness.

## Features

- **Random Resource Disruption**: Randomly terminates EC2 instances, stops services, or introduces latency
- **Configurable Chaos**: Set chaos levels from gentle to extreme
- **Safety First**: Built-in safeguards to prevent complete system failure
- **Multi-Cloud Support**: Works with AWS, Azure, and GCP
- **Detailed Logging**: Tracks all chaos events for analysis

## Usage

```hcl
module "chaos_monkey" {
  source = "./modules/nightly-terraform-chaos-monkey"
  
  # Basic configuration
  chaos_level = "medium"
  enabled     = true
  
  # Target resources
  target_instances = ["i-1234567890abcdef0", "i-0987654321fedcba0"]
  
  # Schedule (optional)
  chaos_schedule = "cron(0 2 * * ? *)" # Daily at 2 AM UTC
}
```

## Chaos Levels

- **gentle**: 1% chance of disruption per hour
- **medium**: 5% chance of disruption per hour
- **extreme**: 15% chance of disruption per hour

## Safety Features

- **Minimum Instance Count**: Always keeps at least N instances running
- **Maintenance Windows**: Respects scheduled maintenance periods
- **Circuit Breaker**: Automatically disables chaos if too many failures occur
- **Dry Run Mode**: Test chaos scenarios without actual disruption

## Installation

1. Add the module to your Terraform configuration
2. Configure your chaos parameters
3. Apply the configuration
4. Monitor the chaos events in your logs

## Monitoring

The module outputs chaos events to CloudWatch Logs, Azure Monitor, or GCP Cloud Logging depending on your cloud provider. Use these logs to:

- Analyze system resilience
- Identify weak points in your architecture
- Improve your disaster recovery procedures

## Contributing

We welcome contributions! Please follow our [contribution guidelines](CONTRIBUTING.md).

## License

This module is licensed under the MIT License.

## Disclaimer

Use this module responsibly. Always test in development environments first and ensure you have proper backup and recovery procedures in place.

---

*This module is part of the ApocalypsAI project - building resilient systems through controlled chaos.*
