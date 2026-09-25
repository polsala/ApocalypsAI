# Nightly Chrono-Vault

A Terraform module to provision an AWS S3 bucket configured for secure, versioned, and cost-effective long-term data archiving. This module automatically enables versioning, server-side encryption, public access blocking, and defines lifecycle rules to transition data to cheaper storage classes and expire old versions.

## Features

*   **Versioning**: Keeps a history of all object changes, crucial for data integrity and recovery.
*   **Server-Side Encryption**: Encrypts data at rest using AES256 or AWS KMS.
*   **Public Access Blocking**: Ensures the bucket is not publicly accessible by default.
*   **Lifecycle Management**: Automatically transitions objects to `STANDARD_IA` and `GLACIER` storage classes to optimize costs, and expires non-current versions.
*   **Access Logging (Optional)**: Configures logging to another S3 bucket for audit and security purposes.

## Usage

To use this module, include it in your root Terraform configuration and provide the required variables.

```terraform
provider "aws" {
  region = "us-east-1"
}

module "my_chrono_vault" {
  source = "./path/to/nightly-chrono-vault/src" # Adjust path as necessary

  bucket_name                       = "my-critical-archive-data"
  region                            = "us-east-1"
  transition_days_standard_ia       = 30
  transition_days_glacier           = 90
  expiration_days_noncurrent_versions = 60
  enable_access_logging             = true
  log_bucket_name                   = "my-s3-access-logs-bucket" # Must exist and be accessible
  # kms_key_id                        = "arn:aws:kms:us-east-1:123456789012:key/your-kms-key-id" # Optional: for KMS encryption
}

output "chrono_vault_id" {
  value = module.my_chrono_vault.bucket_id
}

output "chrono_vault_arn" {
  value = module.my_chrono_vault.bucket_arn
}
```

## Inputs

| Name                                | Description                                                                   | Type     | Default     | Required |
| :---------------------------------- | :---------------------------------------------------------------------------- | :------- | :---------- | :------- |
| `bucket_name`                       | The name of the S3 bucket to create.                                          | `string` | n/a         | yes      |
| `region`                            | The AWS region where the bucket will be created.                              | `string` | `"us-east-1"` | no       |
| `transition_days_standard_ia`       | Number of days after which to transition objects to STANDARD_IA storage class. | `number` | `30`        | no       |
| `transition_days_glacier`           | Number of days after which to transition objects to GLACIER storage class.    | `number` | `90`        | no       |
| `expiration_days_noncurrent_versions` | Number of days after which to transition noncurrent versions to GLACIER and then expire them. | `number` | `60`        | no       |
| `enable_access_logging`             | Set to `true` to enable access logging for the bucket.                        | `bool`   | `false`     | no       |
| `log_bucket_name`                   | The name of the S3 bucket where access logs will be stored. Required if `enable_access_logging` is `true`. | `string` | `null`      | no       |
| `kms_key_id`                        | Optional: The ARN of the KMS key to use for server-side encryption. If `null`, AES256 will be used. | `string` | `null`      | no       |

## Outputs

| Name                 | Description                               | Value |
| :------------------- | :---------------------------------------- | :---- |
| `bucket_id`          | The ID (name) of the S3 bucket.           | `string` |
| `bucket_arn`         | The ARN of the S3 bucket.                 | `string` |
| `bucket_domain_name` | The S3 bucket regional domain name.       | `string` |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 4.0`
*   `jq` for running tests (used in `tests/test.sh`)
