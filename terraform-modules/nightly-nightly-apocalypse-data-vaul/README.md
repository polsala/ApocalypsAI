# Nightly Apocalypse Data Vault

This Terraform module provisions a highly resilient and secure S3 bucket, designed to safeguard critical data against unforeseen digital and physical calamities. It includes features like versioning, server-side encryption, and optional cross-region replication and lifecycle management for long-term archival.

## Features

*   **Versioned Storage**: Keeps multiple versions of objects, protecting against accidental deletions or overwrites.
*   **Server-Side Encryption**: Encrypts data at rest using S3-managed keys (SSE-S3).
*   **Optional Cross-Region Replication (CRR)**: Replicates data to a bucket in a different AWS region for enhanced disaster recovery.
*   **Optional Glacier Archival**: Automatically transitions older data to Amazon S3 Glacier or Glacier Deep Archive for cost-effective long-term storage.

## Usage

To use this module, define it in your Terraform configuration and provide the necessary variables.

```terraform
module "apocalypse_vault" {
  source = "./modules/nightly-apocalypse-data-vault" # Adjust path if using a registry

  bucket_name_prefix = "my-critical-vault"
  region             = "us-east-1"

  # Optional: Enable replication to another bucket
  enable_replication             = true
  replication_destination_bucket_arn = "arn:aws:s3:::my-backup-vault-us-west-2"

  # Optional: Enable Glacier archiving
  enable_glacier_archive = true
  glacier_transition_days = 90
}

output "vault_bucket_id" {
  value = module.apocalypse_vault.vault_bucket_id
}

output "vault_bucket_arn" {
  value = module.apocalypse_vault.vault_bucket_arn
}
```

## Inputs

| Name                             | Description                                                                 | Type     | Default     | Required |
|----------------------------------|-----------------------------------------------------------------------------|----------|-------------|----------|
| `bucket_name_prefix`             | A prefix for the S3 bucket name. A unique suffix will be appended.          | `string` | `null`      | yes      |
| `region`                         | The AWS region where the S3 bucket will be created.                         | `string` | `null`      | yes      |
| `enable_replication`             | Whether to enable cross-region replication.                                 | `bool`   | `false`     | no       |
| `replication_destination_bucket_arn` | ARN of the destination bucket for replication. Required if `enable_replication` is `true`. | `string` | `null`      | no       |
| `enable_glacier_archive`         | Whether to enable lifecycle rules to transition objects to Glacier.         | `bool`   | `false`     | no       |
| `glacier_transition_days`        | Number of days after which to transition objects to Glacier.                | `number` | `30`        | no       |

## Outputs

| Name               | Description                               | Type     |
|--------------------|-------------------------------------------|----------|
| `vault_bucket_id`  | The ID (name) of the created S3 bucket.   | `string` |
| `vault_bucket_arn` | The ARN of the created S3 bucket.         | `string` |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 4.0`
*   Random Provider `~> 3.0`

## Testing

Refer to the `tests/test.sh` script for how to run automated tests for this module.
