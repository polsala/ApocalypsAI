# Nightly Terraform Chaos Garden

A whimsical-yet-useful Terraform module that creates a chaos garden of AWS resources for testing resilience and chaos engineering scenarios.

## Features

- Creates a variety of AWS resources (EC2 instances, S3 buckets, RDS databases, Lambda functions, etc.)
- Configurable chaos scenarios (random failures, resource exhaustion, network partitions)
- Built-in monitoring and observability
- Easy cleanup with Terraform destroy

## Usage

```hcl
module "chaos_garden" {
  source = "./nightly-terraform-chaos-garden"

  # Basic configuration
  environment = "test"
  chaos_level = "medium"  # low, medium, high

  # Resource configuration
  create_ec2_instances = true
  ec2_instance_count = 3
  ec2_instance_type = "t3.micro"

  create_s3_buckets = true
  s3_bucket_count = 2

  create_rds_instances = true
  rds_instance_class = "db.t3.micro"

  create_lambda_functions = true
  lambda_function_count = 2

  # Chaos scenarios
  enable_random_failures = true
  enable_resource_exhaustion = false
  enable_network_partitions = true
}
```

## Chaos Scenarios

### Random Failures
Randomly terminates EC2 instances and RDS databases based on the chaos level.

### Resource Exhaustion
Creates resource exhaustion by:
- Spawning too many EC2 instances
- Filling S3 buckets with data
- Overloading Lambda functions

### Network Partitions
Simulates network partitions by:
- Modifying security groups
- Creating network ACLs
- Blocking specific ports

## Outputs

- `chaos_garden_id`: Unique identifier for the chaos garden
- `ec2_instance_ids`: List of created EC2 instance IDs
- `s3_bucket_names`: List of created S3 bucket names
- `rds_instance_ids`: List of created RDS instance IDs
- `lambda_function_arns`: List of created Lambda function ARNs

## Monitoring

The module creates CloudWatch dashboards and alarms to monitor:
- Resource health
- Chaos scenario execution
- Performance metrics

## Cleanup

To destroy the chaos garden:

```bash
terraform destroy -target module.chaos_garden
```

## Requirements

- Terraform >= 1.0
- AWS provider >= 5.0
- AWS account with appropriate permissions

## License

MIT
