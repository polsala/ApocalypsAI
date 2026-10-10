# Nightly Chronicle Vault

A Terraform module designed to provision a secure, versioned, and lifecycle-managed AWS S3 bucket. This "Chronicle Vault" acts as a digital time capsule, perfect for storing critical data, historical records, or messages for future generations with robust data durability and cost-effective long-term archiving.

## Features

*   **Secure**: Enforces server-side encryption (SSE-S3) and blocks all public access.
*   **Versioned**: Keeps a complete history of all objects, protecting against accidental deletions or overwrites.
*   **Lifecycle Managed**: Automatically transitions older versions of objects to AWS Glacier Deep Archive for cost-effective long-term storage and cleans up incomplete multipart uploads.
*   **Configurable**: Allows customization of bucket name prefix, tags, and lifecycle transition days.

## Usage

To use this module, include it in your Terraform configuration:

```terraform
module "chronicle_vault" {
  source = "./nightly-chronicle-vault/src" # Adjust path if not local
  
  bucket_name_prefix         = "apocalypsai-chronicle"
  glacier_transition_days    = 365 # Transition old versions to Glacier Deep Archive after 1 year
  multipart_upload_expiration_days = 7 # Clean up incomplete uploads after 7 days

  tags = {
    Project     = "ApocalypsAI"
    Environment = "Production"
    Purpose     = "ChronicleVault"
  }
}

output "vault_bucket_id" {
  description = "The ID of the Chronicle Vault S3 bucket."
  value       = module.chronicle_vault.bucket_id
}

output "vault_bucket_arn" {
  description = "The ARN of the Chronicle Vault S3 bucket."
  value       = module.chronicle_vault.bucket_arn
}
```

## Inputs

| Name                               | Description                                                                 | Type   | Default | Required |
| :--------------------------------- | :-------------------------------------------------------------------------- | :----- | :------ | :------- |
| `bucket_name_prefix`               | A prefix for the S3 bucket name. A random suffix will be appended.          | `string` | `"chronicle-vault"` | no       |
| `tags`                             | A map of tags to assign to the S3 bucket.                                   | `map(string)` | `{}`    | no       |
| `glacier_transition_days`          | Number of days after which noncurrent versions transition to Glacier Deep Archive. | `number` | `365`   | no       |
| `multipart_upload_expiration_days` | Number of days after which incomplete multipart uploads expire.             | `number` | `7`     | no       |

## Outputs

| Name                 | Description                                    |
| :------------------- | :--------------------------------------------- |
| `bucket_id`          | The ID (name) of the created S3 bucket.        |
| `bucket_arn`         | The ARN of the created S3 bucket.              |
| `bucket_domain_name` | The domain name of the created S3 bucket.      |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 4.0`
*   Configured AWS credentials
