# Nightly Terraform Chaos Garden

A whimsical-yet-useful Terraform module that creates a "chaos garden" of AWS resources with built-in chaos experiments and automated cleanup schedules. Perfect for testing resilience, practicing incident response, or just watching chaos unfold in a controlled environment.

## Features

- 🌱 **Garden Creation**: Spawns EC2 instances, Lambda functions, S3 buckets, and RDS databases
- 🌪️ **Chaos Experiments**: Configurable chaos experiments (instance termination, network latency, CPU stress)
- 🧹 **Automated Cleanup**: Scheduled cleanup jobs to prevent resource sprawl
- 📊 **Monitoring**: CloudWatch dashboards and alarms for chaos metrics
- 🎲 **Randomness**: Configurable chaos schedules with random intervals

## Usage

```hcl
module "chaos_garden" {
  source = "./modules/chaos-garden"
  
  garden_name = "apocalypsi-chaos-garden"
  
  # Resource configuration
  create_ec2_instances = true
  ec2_instance_count  = 3
  
  create_lambda_functions = true
  lambda_function_count  = 2
  
  create_s3_buckets = true
  s3_bucket_count  = 2
  
  create_rds_instances = true
  rds_instance_count  = 1
  
  # Chaos configuration
  enable_chaos_experiments = true
  chaos_schedule          = "cron(0 */6 * * ? *)" # Every 6 hours
  
  # Cleanup configuration
  enable_automatic_cleanup = true
  cleanup_schedule         = "cron(0 3 * * ? *)" # Daily at 3 AM
  
  # Monitoring
  enable_cloudwatch_dashboard = true
  enable_alarms              = true
}
```

## Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `garden_name` | Name prefix for all resources | `"chaos-garden"` |
| `create_ec2_instances` | Whether to create EC2 instances | `true` |
| `ec2_instance_count` | Number of EC2 instances to create | `3` |
| `create_lambda_functions` | Whether to create Lambda functions | `true` |
| `lambda_function_count` | Number of Lambda functions to create | `2` |
| `create_s3_buckets` | Whether to create S3 buckets | `true` |
| `s3_bucket_count` | Number of S3 buckets to create | `2` |
| `create_rds_instances` | Whether to create RDS instances | `true` |
| `rds_instance_count` | Number of RDS instances to create | `1` |
| `enable_chaos_experiments` | Whether to enable chaos experiments | `true` |
| `chaos_schedule` | Schedule for chaos experiments (cron expression) | `"cron(0 */6 * * ? *)"` |
| `enable_automatic_cleanup` | Whether to enable automatic cleanup | `true` |
| `cleanup_schedule` | Schedule for cleanup jobs (cron expression) | `"cron(0 3 * * ? *)"` |
| `enable_cloudwatch_dashboard` | Whether to create CloudWatch dashboard | `true` |
| `enable_alarms` | Whether to create CloudWatch alarms | `true` |

## Outputs

| Output | Description |
|--------|-------------|
| `garden_resources` | Map of created resources with their IDs and types |
| `chaos_schedule` | The chaos experiment schedule expression |
| `cleanup_schedule` | The cleanup job schedule expression |
| `dashboard_url` | URL to the CloudWatch dashboard (if enabled) |

## Safety Notes

- This module is designed for testing and learning purposes
- Always use in a dedicated AWS account or sandbox environment
- Monitor your AWS billing to avoid unexpected charges
- The chaos experiments are designed to be safe but can cause temporary service disruption

## License

MIT License - Use at your own risk (pun intended)!
