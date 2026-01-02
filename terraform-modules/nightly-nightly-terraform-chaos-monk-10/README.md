# Nightly Terraform Chaos Monkey

A Terraform module that introduces controlled chaos into your infrastructure by randomly destroying and recreating cloud resources. Inspired by Netflix's Chaos Monkey, this module helps test your infrastructure's resilience and recovery mechanisms.

## Features

- Randomly selects resources from your Terraform state
- Destroys and recreates resources based on configurable probability
- Supports AWS, Azure, and GCP resources
- Provides detailed logging and reporting
- Can be safely enabled/disabled via Terraform variables

## Usage

```hcl
module "chaos_monkey" {
  source = "./modules/chaos-monkey"
  
  # Enable chaos (set to false in production!)
  enabled = var.enable_chaos
  
  # 10% chance of destroying a resource per run
  destruction_probability = 0.1
  
  # Resources to potentially target
  target_resources = [
    "aws_instance",
    "aws_rds_instance",
    "aws_s3_bucket"
  ]
  
  # Exclude critical resources
  excluded_resources = [
    "aws_s3_bucket.critical-backup"
  ]
}
```

## Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `enabled` | Enable chaos monkey functionality | `false` |
| `destruction_probability` | Probability (0.0-1.0) of destroying a resource | `0.05` |
| `target_resources` | List of resource types to target | `[]` |
| `excluded_resources` | List of specific resources to exclude | `[]` |
| `max_destructions_per_run` | Maximum number of resources to destroy per run | `3` |

## Safety Considerations

⚠️ **WARNING**: This module is designed for testing environments only. Never enable it in production without extensive safeguards.

- Always use `enabled = false` in production
- Use `excluded_resources` to protect critical infrastructure
- Monitor your infrastructure closely when chaos is enabled
- Ensure you have proper backup and recovery procedures

## Example Integration

```hcl
# In your main.tf
module "chaos_monkey" {
  source = "github.com/polsala/ApocalypsAI//terraform-modules/nightly-terraform-chaos-monkey"
  
  enabled = var.environment == "staging"
  destruction_probability = 0.1
  target_resources = [
    "aws_instance",
    "aws_rds_instance"
  ]
}

# Variable definition
variable "environment" {
  description = "Current environment"
  type        = string
  default     = "development"
}
```

## Monitoring

The module outputs a `chaos_report` that includes:

- Resources destroyed in the current run
- Resources recreated
- Total chaos events
- Timestamp of last chaos event

## Contributing

1. Fork the repository
2. Create a feature branch
3. Test thoroughly in a development environment
4. Submit a pull request with detailed description

## License

MIT License - see LICENSE file for details.

---

*Use responsibly and always have a rollback plan!*
