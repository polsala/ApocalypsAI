# Nightly Cosmic Dust Collector

This Terraform module provisions an AWS S3 bucket designed for collecting ephemeral "cosmic dust" – small, miscellaneous files, temporary backups, logs, or any data that needs a temporary home before being automatically swept away.

It comes pre-configured with sensible lifecycle rules to transition older objects to Infrequent Access (IA) storage and eventually delete them, preventing indefinite storage costs and clutter.

## Features

*   **Ephemeral Storage**: Ideal for temporary files that don't require long-term retention.
*   **Cost-Optimized**: Automatically transitions older objects to S3 Glacier Instant Retrieval (GLACIER_IR) storage.
*   **Self-Cleaning**: Configures lifecycle rules to automatically delete objects after a specified retention period.
*   **Secure by Default**: Blocks public access and enables versioning to prevent accidental data loss.
*   **Customizable**: Easily adjust bucket name prefix, environment tags, and retention periods.

## Usage

To use this module, include it in your Terraform configuration and provide the necessary variables.

```terraform
module "cosmic_dust_bucket" {
  source  = "./modules/nightly-cosmic-dust-collector" # Adjust path if not local

  bucket_name_prefix    = "my-app-dust"
  environment           = "dev"
  retention_days        = 45  # Keep dust for 45 days before deletion
  transition_days_to_ia = 15  # Move to GLACIER_IR after 15 days
}

output "dust_bucket_id" {
  description = "The ID of the cosmic dust collection bucket."
  value       = module.cosmic_dust_bucket.bucket_id
}

output "dust_bucket_arn" {
  description = "The ARN of the cosmic dust collection bucket."
  value       = module.cosmic_dust_bucket.bucket_arn
}
```

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 5.0`
*   Configured AWS credentials (e.g., via `~/.aws/credentials` or environment variables).

## Inputs

| Name                    | Description                                                               | Type     | Default | Required |
|-------------------------|---------------------------------------------------------------------------|----------|---------|----------|
| `bucket_name_prefix`    | A prefix for the S3 bucket name. A unique suffix will be appended.        | `string` | `null`  | yes      |
| `environment`           | The environment tag for the bucket (e.g., `dev`, `prod`).                 | `string` | `"dev"` | no       |
| `retention_days`        | Number of days after which objects in the bucket will be permanently deleted. | `number` | `30`    | no       |
| `transition_days_to_ia` | Number of days after which objects will transition to S3 Glacier Instant Retrieval. | `number` | `7`     | no       |

## Outputs

| Name                 | Description                                    |
|----------------------|------------------------------------------------|
| `bucket_id`          | The ID (name) of the created S3 bucket.        |
| `bucket_arn`         | The ARN of the created S3 bucket.              |
| `bucket_domain_name` | The domain name of the created S3 bucket.      |

## Testing

This module includes automated tests using Terraform's built-in testing framework. To run the tests:

1.  Navigate to the module's root directory.
2.  Run `terraform init`.
3.  Run `terraform test`.

These tests validate the module's configuration against expected resource attributes and outputs without provisioning actual AWS resources during the plan phase. They ensure that the bucket is configured with public access blocked, versioning enabled, and the correct lifecycle rules are applied based on the input variables.
