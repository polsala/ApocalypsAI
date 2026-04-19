# Nightly Temporal Data Vault

This Terraform module provisions a highly durable and cost-effective AWS S3 bucket designed for long-term data archival. It automatically enables versioning to protect against accidental deletions and defines lifecycle rules to transition older data to Glacier storage, ensuring your digital relics endure through any temporal distortions or catastrophic events.

## Features

*   **Versioned Storage**: Keeps multiple versions of an object, allowing recovery from accidental overwrites or deletions.
*   **Lifecycle Management**: Automatically transitions older data to AWS Glacier for cost-effective long-term storage.
*   **Secure by Default**: Blocks public access to the bucket.
*   **Tagging**: Applies standard tags for easy identification and cost allocation.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "my_temporal_vault" {
  source = "./path/to/nightly-temporal-data-vault/src"

  bucket_name           = "my-apocalypsai-data-archive"
  environment           = "production"
  retention_days_standard = 30  # Days before moving to Glacier
  retention_days_glacier  = 365 # Days before expiring from Glacier
}

output "vault_bucket_id" {
  value = module.my_temporal_vault.s3_bucket_id
}

output "vault_bucket_arn" {
  value = module.my_temporal_vault.s3_bucket_arn
}
```

## Inputs

| Name                    | Description                                                               | Type     | Default | Required |
|-------------------------|---------------------------------------------------------------------------|----------|---------|----------|
| `bucket_name`           | The name of the S3 bucket to create. Must be globally unique.             | `string` | n/a     | yes      |
| `environment`           | The environment tag for the bucket (e.g., `dev`, `prod`, `staging`).      | `string` | `"prod"`| no       |
| `retention_days_standard` | Number of days after which objects in the STANDARD storage class are transitioned to GLACIER. | `number` | `30`    | no       |
| `retention_days_glacier`| Number of days after which objects in the GLACIER storage class are expired. | `number` | `365`   | no       |

## Outputs

| Name             | Description                                   |
|------------------|-----------------------------------------------|
| `s3_bucket_id`   | The ID (name) of the created S3 bucket.       |
| `s3_bucket_arn`  | The ARN (Amazon Resource Name) of the S3 bucket. |

## Requirements

*   Terraform 0.13+
*   AWS Provider configured with appropriate credentials.
