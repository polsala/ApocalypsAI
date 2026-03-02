# Nightly Cosmic Dust Collector

This Terraform module provisions a whimsical-yet-useful "Cosmic Dust Collector" in your AWS environment. It sets up an S3 bucket designed to collect ephemeral data, logs, or any small, miscellaneous files you might consider "cosmic dust" from your various applications and services. It also includes an associated CloudWatch Log Group for monitoring the collector's activities or for general logging related to its purpose.

Think of it as a digital catch-all for the bits and bytes that drift through your cloud infrastructure.

## Features

*   **S3 Bucket**: A dedicated S3 bucket for storing arbitrary data.
*   **CloudWatch Log Group**: A log group for monitoring bucket access, or for general application logs directed to this collector.
*   **Configurable**: Easily customize bucket naming and tags.

## Usage

To use this module, include it in your Terraform configuration:

```terraform
module "cosmic_dust_collector" {
  source = "./path/to/nightly-cosmic-dust-collector" # Or a Git URL/Registry path
  
  bucket_name_prefix = "my-app-dust"
  environment        = "dev"
  tags = {
    Owner       = "ApocalypsAI"
    Purpose     = "CosmicDustCollection"
    Retention   = "7_days"
  }
}

output "dust_bucket_id" {
  value       = module.cosmic_dust_collector.bucket_id
  description = "The ID of the Cosmic Dust S3 bucket."
}

output "dust_log_group_name" {
  value       = module.cosmic_dust_collector.log_group_name
  description = "The name of the CloudWatch Log Group for the Cosmic Dust Collector."
}
```

## Requirements

*   Terraform CLI (v1.0.0+)
*   AWS Provider configured with appropriate credentials.

## Inputs

| Name                 | Description                                                               | Type     | Default | Required |
| :------------------- | :------------------------------------------------------------------------ | :------- | :------ | :------- |
| `bucket_name_prefix` | A prefix for the S3 bucket name. The full name will be generated.         | `string` | `null`  | yes      |
| `environment`        | The environment (e.g., `dev`, `prod`) to tag resources with.              | `string` | `"dev"` | no       |
| `tags`               | A map of additional tags to apply to the S3 bucket and CloudWatch Log Group. | `map(string)` | `{}`    | no       |

## Outputs

| Name                | Description                                         |
| :------------------ | :-------------------------------------------------- |
| `bucket_id`         | The ID of the created S3 bucket.                    |
| `bucket_arn`        | The ARN of the created S3 bucket.                   |
| `log_group_name`    | The name of the CloudWatch Log Group.               |

## Development & Testing

This module includes a basic test setup to validate its Terraform configuration.

To run tests:

1.  Navigate to the `tests/` directory.
2.  Run the `test.sh` script: `./test.sh`

This script performs `terraform init -backend=false`, `terraform validate`, and `terraform plan` to ensure the module's syntax and structure are correct without deploying actual resources.
