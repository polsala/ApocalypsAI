# Terraform Chaos Monkey

A Terraform module that introduces controlled chaos into your infrastructure by randomly destroying and recreating resources. Inspired by Netflix's Chaos Monkey, this module helps test your infrastructure's resilience and recovery mechanisms.

## Features

- Randomly selects resources for destruction based on configurable probability
- Supports multiple cloud providers (AWS, Azure, GCP)
- Configurable chaos schedules and resource types
- Automatic recreation of destroyed resources
- Detailed logging and reporting
- Safe mode for testing without actual destruction

## Usage

```hcl
module "chaos_monkey" {
  source = "./modules/chaos-monkey"
  
  # Enable chaos monkey
  enabled = true
  
  # 10% chance of destroying a resource per day
  destruction_probability = 0.1
  
  # Only target these resource types
  target_resource_types = [
    "aws_instance",
    "aws_rds_instance",
    "aws_s3_bucket"
  ]
  
  # Chaos schedule (cron format)
  chaos_schedule = "0 2 * * *"  # Daily at 2 AM
  
  # Safe mode - logs actions but doesn't destroy
  safe_mode = false
}
```

## Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | bool | false | Enable/disable the chaos monkey |
| `destruction_probability` | number | 0.05 | Probability (0.0-1.0) of destroying a resource |
| `target_resource_types` | list(string) | [] | Resource types to target for chaos |
| `chaos_schedule` | string | "0 2 * * *" | Cron schedule for chaos execution |
| `safe_mode` | bool | true | Log actions without actually destroying resources |
| `max_resources_per_run` | number | 3 | Maximum number of resources to destroy per chaos run |
| `excluded_resources` | list(string) | [] | Resource IDs to exclude from chaos |

## Safety Considerations

⚠️ **WARNING**: This module can destroy production resources!

- Always test in development environments first
- Use `safe_mode = true` to preview actions
- Exclude critical resources using `excluded_resources`
- Monitor your infrastructure closely
- Ensure you have proper backups and recovery procedures

## Cloud Provider Support

- **AWS**: EC2 instances, RDS databases, S3 buckets, Lambda functions
- **Azure**: Virtual machines, SQL databases, Storage accounts, Functions
- **GCP**: Compute instances, Cloud SQL, Cloud Storage, Cloud Functions

## Monitoring

The module creates CloudWatch/Stackdriver/Azure Monitor logs for:

- Resources selected for destruction
- Destruction success/failure
- Recreation status
- Chaos monkey execution metrics

## License

MIT License - Use at your own risk!

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## Disclaimer

This tool is designed for testing infrastructure resilience. The authors are not responsible for any damage, data loss, or downtime caused by its use. Always use responsibly and in accordance with your organization's policies.
