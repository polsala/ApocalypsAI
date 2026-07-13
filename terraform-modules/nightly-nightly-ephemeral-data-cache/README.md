# Nightly Ephemeral Data Cache (Terraform Module)

In the ever-shifting sands of the digital wasteland, data can accumulate like forgotten relics. The `nightly-ephemeral-data-cache` module provides a whimsical-yet-practical solution for managing temporary data storage in AWS S3, ensuring that transient information doesn't become a permanent burden.

This Terraform module provisions an S3 bucket specifically designed for ephemeral data, automatically cleaning up objects after a configurable number of days. It's perfect for temporary logs, intermediate build artifacts, session data, or any information that has a short shelf life, helping you keep your cloud environment tidy and cost-efficient.

## Features

*   **Self-Cleaning**: Automatically deletes objects after a specified `expiration_days` period using S3 lifecycle rules.
*   **Cost-Optimized**: Prevents unnecessary storage costs by ensuring old, temporary data is purged.
*   **Secure by Default**: Configures the bucket with private access and blocks public access to enhance security.
*   **Tagging**: Applies standard tags for easy identification and management.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "my_ephemeral_cache" {
  source = "./path/to/nightly-ephemeral-data-cache/src" # Adjust path as needed

  bucket_name_prefix = "my-project-temp-data"
  expiration_days    = 14 # Objects will be deleted after 14 days
}

output "cache_bucket_name" {
  description = "The name of the ephemeral S3 bucket."
  value       = module.my_ephemeral_cache.s3_bucket_id
}

output "cache_bucket_arn" {
  description = "The ARN of the ephemeral S3 bucket."
  value       = module.my_ephemeral_cache.s3_bucket_arn
}
```

## Inputs

| Name                 | Description                                                                 | Type   | Default                       | Required |
|----------------------|-----------------------------------------------------------------------------|--------|-------------------------------|----------|
| `bucket_name_prefix` | A unique prefix for the S3 bucket name. Terraform will append a unique suffix. | `string` | `"apocalypsai-ephemeral-cache-"` | no       |
| `expiration_days`    | Number of days after which objects in the bucket will be automatically deleted. | `number` | `7`                           | no       |

## Outputs

| Name           | Description                     |
|----------------|---------------------------------|
| `s3_bucket_id` | The ID (name) of the S3 bucket. |
| `s3_bucket_arn`| The ARN of the S3 bucket.       |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 5.0`

## Testing

The module includes a `tests/` directory with a basic `terraform plan` based test script to ensure the module's resources and configurations are correctly defined. Run `tests/test.sh` to execute these tests.
