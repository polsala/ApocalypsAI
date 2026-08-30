# Nightly Chrono-Cache Provisioner

This Terraform module provisions a whimsical-yet-useful 'Chrono-Cache' – a time-limited AWS S3 bucket designed for storing ephemeral data, 'temporal echoes', or temporary logs that should automatically vanish after a specified duration.

It's perfect for scenarios where you need temporary storage for processing, transient data, or simply want to ensure old data doesn't linger indefinitely, keeping your digital wasteland tidy.

## Features

*   **Ephemeral Storage**: Creates an AWS S3 bucket.
*   **Self-Cleaning**: Configures a lifecycle rule to automatically expire objects after a defined number of days.
*   **Configurable**: Easily set the bucket name prefix, expiration period, and AWS region.

## Usage

To use this module, include it in your Terraform configuration:

```terraform
module "chrono_cache" {
  source = "./nightly-chrono-cache-provisioner/src" # Path to the module's source directory

  bucket_name_prefix = "my-temporal-echoes"
  expiration_days    = 30
  aws_region         = "us-east-1"
}

output "chrono_cache_bucket_id" {
  value = module.chrono_cache.bucket_id
}

output "chrono_cache_bucket_arn" {
  value = module.chrono_cache.bucket_arn
}
```

## Inputs

| Name               | Description                                                              | Type     | Default          | Required |
|--------------------|--------------------------------------------------------------------------|----------|------------------|----------|
| `bucket_name_prefix` | A prefix for the S3 bucket name. A unique suffix will be appended.       | `string` | `"chrono-cache"` | no       |
| `expiration_days`  | Number of days after which objects in the bucket will be expired/deleted. | `number` | `7`              | no       |
| `aws_region`       | The AWS region where the S3 bucket will be created.                      | `string` | `"us-east-1"`    | no       |

## Outputs

| Name                    | Description                                |
|-------------------------|--------------------------------------------|
| `bucket_id`             | The ID (name) of the created S3 bucket.    |
| `bucket_arn`            | The ARN of the created S3 bucket.          |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 5.0`
*   Random Provider `~> 3.0`

## Testing

Refer to the `tests/` directory for how to run offline validation and plan generation tests for this module.
