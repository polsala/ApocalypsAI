# Nightly Terraform Chaos Monkey

A Terraform module that introduces controlled chaos by randomly terminating cloud resources to test your infrastructure's resilience.

## Features

- Randomly terminates EC2 instances, RDS databases, and other cloud resources
- Configurable chaos schedule and probability
- Automatic rollback and recovery testing
- Detailed logging and reporting
- Safe mode for development environments

## Usage

```hcl
module "chaos_monkey" {
  source = "./modules/chaos-monkey"
  
  # Enable chaos in production (use with caution!)
  enabled = var.environment == "production"
  
  # 5% chance of chaos per hour
  chaos_probability = 0.05
  
  # Only target specific resource types
  target_resource_types = ["aws_instance", "aws_rds_instance"]
  
  # Exclude critical resources
  excluded_tags = {
    environment = "critical"
    team        = "ops"
  }
}
```

## Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `enabled` | bool | false | Enable chaos monkey functionality |
| `chaos_probability` | number | 0.01 | Probability (0.0-1.0) of chaos per hour |
| `target_resource_types` | list(string) | ["aws_instance"] | Resource types to target |
| `excluded_tags` | map(string) | {} | Tags that exclude resources from chaos |
| `safe_mode` | bool | true | Enable safety checks and confirmations |

## Safety Features

- **Dry Run Mode**: Preview chaos actions without executing them
- **Resource Exclusions**: Protect critical infrastructure with tag-based filtering
- **Time Windows**: Only run chaos during specified hours
- **Rollback Testing**: Verify that your infrastructure can recover automatically

## Installation

1. Add this module to your Terraform configuration
2. Configure your chaos parameters
3. Run `terraform apply`
4. Monitor the chaos logs and verify recovery

## Monitoring

The module outputs chaos events to CloudWatch Logs and creates metrics for:

- Chaos events triggered
- Resources terminated
- Recovery time
- Failed recovery attempts

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Disclaimer

Use this tool responsibly. Always test in development environments first. The authors are not responsible for any damage caused by misuse.
