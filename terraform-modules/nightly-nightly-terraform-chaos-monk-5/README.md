# Nightly Terraform Chaos Monkey

A Terraform module that introduces controlled chaos by randomly destroying and recreating cloud resources to test your infrastructure's resilience.

## Features

- Randomly selects resources from your state to destroy
- Automatically recreates destroyed resources
- Configurable chaos intensity and schedule
- Safe mode with dry-run capabilities
- Detailed logging and reporting

## Usage

```hcl
module "chaos_monkey" {
  source = "./modules/chaos-monkey"
  
  # Enable chaos mode
  chaos_enabled = true
  
  # Destroy 10% of resources daily
  chaos_probability = 0.1
  chaos_schedule    = "0 2 * * *"
  
  # Target specific resource types
  target_resource_types = [
    "aws_instance",
    "aws_security_group",
    "aws_rds_instance"
  ]
  
  # Exclude critical resources
  excluded_resources = [
    "production-db",
    "critical-load-balancer"
  ]
}
```

## Configuration Options

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `chaos_enabled` | `bool` | `false` | Enable/disable chaos mode |
| `chaos_probability` | `number` | `0.05` | Probability (0-1) of destroying a resource |
| `chaos_schedule` | `string` | `"0 3 * * *"` | Cron schedule for chaos execution |
| `target_resource_types` | `list(string)` | `[]` | Resource types to target (empty = all) |
| `excluded_resources` | `list(string)` | `[]` | Resource names to exclude from chaos |
| `dry_run` | `bool` | `true` | Enable dry-run mode (no actual destruction) |
| `log_level` | `string` | `"INFO"` | Logging verbosity level |

## Safety Features

- **Dry-run mode**: Test chaos scenarios without actual destruction
- **Resource exclusion**: Protect critical infrastructure from chaos
- **Probability controls**: Fine-tune chaos intensity
- **Detailed logging**: Track all chaos activities for analysis
- **Rollback capability**: Automatic recreation of destroyed resources

## Installation

1. Clone this module into your Terraform project
2. Configure the module variables
3. Run `terraform init` and `terraform apply`

## Monitoring

The module outputs chaos metrics that can be integrated with monitoring systems:

```hcl
output "chaos_metrics" {
  value = module.chaos_monkey.chaos_metrics
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Test thoroughly with dry-run mode
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Warning

⚠️ **Use extreme caution in production environments** ⚠️

This module is designed for testing infrastructure resilience. Always:

- Start with dry-run mode
- Exclude critical resources
- Monitor your infrastructure closely
- Have rollback plans in place
- Test in development environments first

The authors are not responsible for any damage caused by this module.
