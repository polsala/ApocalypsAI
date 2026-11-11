# Nightly Echo Chamber Bucket

This Terraform module deploys an AWS S3 bucket configured as a "Temporal Echo Chamber." It's designed to retain all versions of objects, transitioning older versions to cost-effective storage classes like Glacier, and eventually expiring them after a very long period. This ensures that no data is ever truly lost, merely archived into the echoes of time.

## Features

*   **Versioning Enabled**: Keeps all historical versions of objects.
*   **Lifecycle Rules**:
    *   Transitions noncurrent object versions to `GLACIER_IR` after 30 days.
    *   Transitions noncurrent object versions to `GLACIER` after 90 days.
    *   Expires noncurrent object versions after 3650 days (10 years).
    *   Expires incomplete multipart uploads after 7 days.
*   **Configurable Name & Tags**: Allows customization of the bucket name and associated tags.

## Usage

To use this module, include it in your Terraform configuration:

```terraform
module "echo_chamber_bucket" {
  source = "./nightly-echo-chamber-bucket/src" # Adjust path if not in the same repo root
  
  bucket_name = "my-apocalypsai-echo-chamber"
  region      = "us-east-1"
  tags = {
    Project     = "ApocalypsAI"
    Environment = "Dev"
    Purpose     = "TemporalEchoChamber"
  }
}

output "echo_chamber_bucket_id" {
  value       = module.echo_chamber_bucket.bucket_id
  description = "The ID of the created S3 bucket."
}

output "echo_chamber_bucket_arn" {
  value       = module.echo_chamber_bucket.bucket_arn
  description = "The ARN of the created S3 bucket."
}
```

## Inputs

| Name        | Description                               | Type          | Default |
|-------------|-------------------------------------------|---------------|---------|
| `bucket_name` | The name of the S3 bucket to create.      | `string`      | n/a     |
| `region`      | The AWS region where the bucket will be deployed. | `string`      | n/a     |
| `tags`        | A map of tags to assign to the bucket.    | `map(string)` | `{}`    |

## Outputs

| Name                 | Description                       |
|----------------------|-----------------------------------|
| `bucket_id`          | The ID (name) of the S3 bucket.   |
| `bucket_arn`         | The ARN of the S3 bucket.         |
| `bucket_domain_name` | The domain name of the S3 bucket. |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 4.0`

## Testing

This module includes automated tests to validate its syntax and configuration.

To run the tests:

1.  Navigate to the `tests/` directory: `cd tests/`
2.  Execute the test script: `./test.sh`

This script will perform `terraform init`, `terraform validate`, and `terraform fmt --check` to ensure the module is correctly structured and formatted.
