# Nightly Chronos Cache Provisioner

This Terraform module provisions a secure, versioned AWS S3 bucket, whimsically named a "Chronos Cache," designed for storing time-sensitive or ephemeral data with a robust history of changes.

## Features

*   **Secure by Default**: Blocks public access, enforces server-side encryption (SSE-S3).
*   **Versioned**: Keeps a history of all object versions, protecting against accidental deletions or overwrites.
*   **Tagging**: Automatically applies `ManagedBy` and `Purpose` tags, with support for custom tags.
*   **Whimsical Naming**: Embrace the temporal theme with a "Chronos Cache" for your data.

## Usage

To use this module, include it in your Terraform configuration and provide the required `bucket_name`.

```terraform
module "my_chronos_cache" {
  source = "./path/to/nightly-chronos-cache-provisioner/src"

  bucket_name = "my-apocalypsai-temporal-data-store"
  tags = {
    Environment = "Production"
    Owner       = "ApocalypsAI-Team"
  }
}

output "cache_bucket_id" {
  value = module.my_chronos_cache.bucket_id
}

output "cache_bucket_arn" {
  value = module.my_chronos_cache.bucket_arn
}
```

## Inputs

| Name        | Description                               | Type        | Default | Required |
|-------------|-------------------------------------------|-------------|---------|----------|
| `bucket_name` | The name of the S3 bucket to create.      | `string`    | n/a     | yes      |
| `tags`        | A map of tags to assign to the bucket.    | `map(string)` | `{}`    | no       |

## Outputs

| Name               | Description                                |
|--------------------|--------------------------------------------|
| `bucket_id`          | The ID (name) of the S3 bucket.            |
| `bucket_arn`         | The ARN of the S3 bucket.                  |
| `bucket_domain_name` | The S3 bucket regional domain name.        |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 5.0`

## Testing

To run the automated tests for this module, navigate to the `tests/` directory and execute the `test.sh` script:

```bash
cd tests/
./test.sh
```

This script performs a `terraform plan` dry run and asserts on the expected resources and configurations without provisioning actual cloud resources.
