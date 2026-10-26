# Nightly Cloud Critter Cuddler

A Terraform module for AWS that provisions a small, cost-optimized EC2 instance and an S3 bucket, along with a CloudWatch Event Rule and Lambda function to automatically stop the instance during specified "sleep" hours and start it during "wake" hours. Perfect for dev/staging environments to save costs by tucking your cloud critters into bed when not in use.

## Features

- **Cost Optimization**: Automatically stops/starts an EC2 instance based on a schedule.
- **Ephemeral Workloads**: Ideal for development, testing, or temporary environments.
- **Simple S3 Storage**: Includes a dedicated S3 bucket for logs, data, or configuration.
- **Whimsical Automation**: Your cloud resources get their beauty sleep!

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "critter_cuddler" {
  source = "./path/to/nightly-cloud-critter-cuddler/src" # Adjust path as needed

  name                = "my-dev-critter"
  instance_type       = "t2.micro"
  ami_id              = "ami-0abcdef1234567890" # Replace with a valid AMI ID for your region
  key_name            = "my-ssh-key"          # Replace with an existing EC2 Key Pair name
  vpc_id              = "vpc-0123456789abcdef0" # Replace with your VPC ID
  subnet_id           = "subnet-0fedcba9876543210" # Replace with a subnet ID in your VPC
  
  # Cron expressions for stopping and starting the instance.
  # Example: "cron(0 22 * * ? *)" for 10 PM UTC, "cron(0 8 * * ? *)" for 8 AM UTC
  sleep_cron_expression = "cron(0 22 * * ? *)" # Stop at 10 PM UTC
  wake_cron_expression  = "cron(0 8 * * ? *)"  # Start at 8 AM UTC

  tags = {
    Project     = "ApocalypsAI"
    Environment = "Dev"
  }
}

output "critter_instance_id" {
  description = "The ID of the cuddled EC2 instance."
  value       = module.critter_cuddler.instance_id
}

output "critter_s3_bucket_name" {
  description = "The name of the S3 bucket for the cuddled critter."
  value       = module.critter_cuddler.s3_bucket_name
}
```

## Inputs

| Name                    | Description                                                               | Type          | Default | Required |
|-------------------------|---------------------------------------------------------------------------|---------------|---------|----------|
| `name`                  | A unique name for the critter resources.                                  | `string`      | n/a     | yes      |
| `instance_type`         | The EC2 instance type.                                                    | `string`      | `"t2.micro"` | no       |
| `ami_id`                | The AMI ID for the EC2 instance.                                          | `string`      | n/a     | yes      |
| `key_name`              | The name of the EC2 Key Pair to use for the instance.                     | `string`      | n/a     | yes      |
| `vpc_id`                | The ID of the VPC where the instance will be launched.                    | `string`      | n/a     | yes      |
| `subnet_id`             | The ID of the subnet where the instance will be launched.                 | `string`      | n/a     | yes      |
| `sleep_cron_expression` | Cron expression for when the EC2 instance should stop (e.g., `cron(0 22 * * ? *)` for 10 PM UTC). | `string` | n/a     | yes      |
| `wake_cron_expression`  | Cron expression for when the EC2 instance should start (e.g., `cron(0 8 * * ? *)` for 8 AM UTC). | `string` | n/a     | yes      |
| `tags`                  | A map of tags to assign to all resources.                                 | `map(string)` | `{}`    | no       |

## Outputs

| Name                   | Description                                  |
|------------------------|----------------------------------------------|
| `instance_id`          | The ID of the provisioned EC2 instance.      |
| `s3_bucket_name`       | The name of the provisioned S3 bucket.       |
| `security_group_id`    | The ID of the security group created for the instance. |

## Requirements

- AWS Provider configured with appropriate credentials.
- An existing VPC, subnet, and EC2 Key Pair.
- Terraform `v1.0+`
