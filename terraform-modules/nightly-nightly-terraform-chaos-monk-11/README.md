# Nightly Terraform Chaos Monkey

A whimsical-yet-useful Terraform module that randomly terminates cloud resources to test your infrastructure's resilience.

## What It Does

This module creates a scheduled Lambda function (or equivalent) that randomly selects and terminates resources in your cloud environment. Perfect for chaos engineering and testing your disaster recovery procedures!

## Features

- Randomly terminates EC2 instances, RDS databases, or other cloud resources
- Configurable chaos schedule (daily, hourly, etc.)
- Resource selection filters to avoid critical systems
- Detailed logging and reporting
- Easy opt-out mechanism

## Installation

```hcl
module "chaos_monkey" {
  source = "./modules/nightly-terraform-chaos-monkey"
  
  # Configuration options
  chaos_schedule = "cron(0 2 * * ? *)"  # Daily at 2 AM UTC
  resource_types = ["ec2", "rds"]
  exclude_tags = {
    Environment = "production"
    Critical    = "true"
  }
}
```

## Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `chaos_schedule` | string | `"cron(0 2 * * ? *)"` | CloudWatch Events schedule expression |
| `resource_types` | list(string) | `["ec2"]` | Resource types to target for chaos |
| `exclude_tags` | map(string) | `{}` | Tags to exclude from chaos |
| `max_chaos_per_run` | number | `3` | Maximum resources to terminate per execution |
| `enabled` | bool | `true` | Enable/disable chaos monkey |

## Safety Features

- **Tag-based exclusion**: Mark critical resources with specific tags to protect them
- **Resource limits**: Configure maximum chaos per execution
- **Dry run mode**: Test mode that logs what would be terminated without actually doing it
- **Opt-out capability**: Disable chaos monkey entirely via configuration

## Usage Examples

### Basic Usage

```hcl
module "chaos_monkey" {
  source = "./modules/nightly-terraform-chaos-monkey"
  
  chaos_schedule = "rate(1 hour)"
  resource_types = ["ec2"]
}
```

### Production-Safe Configuration

```hcl
module "chaos_monkey" {
  source = "./modules/nightly-terraform-chaos-monkey"
  
  chaos_schedule = "cron(0 3 * * ? *)"  # 3 AM UTC
  resource_types = ["ec2", "rds", "elasticache"]
  exclude_tags = {
    Environment = "production"
    Critical    = "true"
    Team        = "platform"
  }
  max_chaos_per_run = 1
  enabled = var.enable_chaos_engineering
}
```

## Monitoring

The chaos monkey logs all actions to CloudWatch Logs. You can monitor:

- Resources selected for termination
- Resources that were excluded
- Execution status and errors
- Chaos metrics and statistics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Disclaimer

⚠️ **Use at your own risk!** This tool is designed to terminate resources. Always test in non-production environments first and ensure you have proper backups and recovery procedures in place.

## Inspiration

Inspired by Netflix's Chaos Monkey and the need for more resilient cloud infrastructure. May your systems be strong enough to survive the chaos!
