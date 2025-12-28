# Nightly Terraform Chaos Monkey

A whimsical-yet-useful Terraform module that randomly terminates cloud resources to test your infrastructure's resilience. Inspired by Netflix's Chaos Monkey, this module helps ensure your systems can handle unexpected failures.

## Features

- Randomly terminates EC2 instances, RDS databases, and other cloud resources
- Configurable chaos schedule and intensity
- Comprehensive logging and reporting
- Safe mode for testing
- Multi-cloud support (AWS, Azure, GCP)

## Usage

```hcl
module "chaos_monkey" {
  source = "./modules/chaos-monkey"
  
  # Enable chaos monkey
  enabled = true
  
  # Chaos schedule (cron format)
  chaos_schedule = "0 2 * * *"  # Daily at 2 AM
  
  # Chaos intensity (0-100%)
  chaos_intensity = 10
  
  # Resources to target
  target_resources = [
    "aws_instance",
    "aws_rds_instance",
    "aws_ecs_service"
  ]
  
  # Safe mode - only logs what would be terminated
  safe_mode = false
}
```

## Configuration

| Variable | Description | Default | Type |
|----------|-------------|---------|------|
| `enabled` | Enable chaos monkey | `false` | `bool` |
| `chaos_schedule` | Cron schedule for chaos events | `"0 2 * * *"` | `string` |
| `chaos_intensity` | Percentage of resources to terminate (0-100) | `5` | `number` |
| `target_resources` | List of resource types to target | `[]` | `list(string)` |
| `safe_mode` | Only log actions without actually terminating | `true` | `bool` |
| `excluded_tags` | Tags to exclude from chaos | `[]` | `list(string)` |
| `region` | AWS region | `"us-east-1"` | `string` |

## Safety Features

- **Safe Mode**: Test runs without actual resource termination
- **Tag Exclusions**: Protect critical resources with specific tags
- **Resource Limits**: Maximum number of resources to terminate per run
- **Time Windows**: Chaos only runs during specified time windows
- **Audit Logging**: Comprehensive logs of all chaos events

## Installation

1. Clone this repository
2. Navigate to the chaos-monkey module
3. Run `terraform init` and `terraform apply`

## Contributing

We welcome contributions! Please follow our [contribution guidelines](CONTRIBUTING.md).

## License

MIT License - see [LICENSE](LICENSE) for details.

## Disclaimer

This tool is designed to terminate resources. Use with extreme caution in production environments. The authors are not responsible for any data loss or service disruption caused by this tool.

## Support

For support and questions, please open an issue in this repository.
