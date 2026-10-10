# Nightly Whispering Vault

A Terraform module to provision a secure, ephemeral AWS S3 bucket. This "Whispering Vault" is designed for temporary storage of sensitive or fleeting community messages and small files, ensuring they are encrypted and automatically purged after a configurable retention period.

## Features

*   **Secure**: Server-side encryption (SSE-S3) enabled by default.
*   **Ephemeral**: Configurable lifecycle rule to automatically expire objects after a set number of days.
*   **Versioned**: Object versioning enabled to protect against accidental overwrites or deletions within the retention period.
*   **Private**: Bucket access is private by default.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
provider "aws" {
  region = "us-east-1" # Or your desired AWS region
}

module "community_whisper_vault" {
  source = "./path/to/nightly-whispering-vault" # Adjust path if not local

  bucket_name_prefix = "apocalypsai-whispers"
  region             = "us-east-1"
  retention_days     = 7 # Objects will be deleted after 7 days
}

output "vault_bucket_id" {
  description = "The ID of the created S3 bucket."
  value       = module.community_whisper_vault.bucket_id
}

output "vault_bucket_arn" {
  description = "The ARN of the created S3 bucket."
  value       = module.community_whisper_vault.bucket_arn
}
```

## Inputs

| Name               | Description                                  | Type   | Default            | Required |
| :----------------- | :------------------------------------------- | :----- | :----------------- | :------- |
| `bucket_name_prefix` | A prefix for the S3 bucket name.             | `string` | `"whisper-vault-"` | no       |
| `region`           | The AWS region where the S3 bucket will be created. | `string` | `"us-east-1"`      | no       |
| `retention_days`   | Number of days after which objects will be expired. | `number` | `7`                | no       |

## Outputs

| Name         | Description                                  |
| :----------- | :------------------------------------------- |
| `bucket_id`  | The ID (name) of the created S3 bucket.      |
| `bucket_arn` | The ARN (Amazon Resource Name) of the created S3 bucket. |
