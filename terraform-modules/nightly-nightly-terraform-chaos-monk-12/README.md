# Nightly Terraform Chaos Monkey

A Terraform module that randomly terminates cloud resources to test system resilience and chaos engineering practices.

## Features

- Randomly selects resources from your infrastructure
- Supports AWS, Azure, and GCP
- Configurable chaos intervals and resource types
- Safety mechanisms to prevent total destruction
- Detailed logging and reporting

## Usage

```hcl
module "chaos_monkey" {
  source = "./modules/chaos-monkey"
  
  # Enable chaos engineering
  chaos_enabled = true
  
  # Chaos configuration
  chaos_interval_hours = 2
  max_resources_per_run = 3
  
  # Resource types to target
  target_resource_types = [
    "aws_instance",
    "aws_rds_instance",
    "aws_elasticache_cluster"
  ]
  
  # Safety exclusions
  excluded_resources = [
    "production-db",
    "critical-app-server"
  ]
}
```

## Configuration Options

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `chaos_enabled` | `bool` | `false` | Enable/disable chaos engineering |
| `chaos_interval_hours` | `number` | `1` | Hours between chaos runs |
| `max_resources_per_run` | `number` | `1` | Maximum resources to terminate per run |
| `target_resource_types` | `list(string)` | `[]` | Resource types to target for chaos |
| `excluded_resources` | `list(string)` | `[]` | Resource names to exclude from chaos |
| `dry_run` | `bool` | `true` | Only log what would be destroyed, don't actually destroy |

## Safety Features

- **Dry run mode**: Always enabled by default
- **Resource exclusions**: Protect critical infrastructure
- **Rate limiting**: Configurable chaos frequency
- **Audit logging**: All actions are logged for review
- **Resource validation**: Only targets resources that exist

## Installation

1. Clone this module into your Terraform project
2. Configure the variables as needed
3. Run `terraform init` and `terraform apply`
4. Monitor the chaos logs in your cloud provider's logging service

## Monitoring

The module creates CloudWatch logs (AWS) or equivalent logging in other providers. Monitor these logs to track chaos events and system resilience.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Disclaimer

This tool is designed for testing resilience in controlled environments. Use with caution in production systems. The authors are not responsible for any damage caused by misuse.
