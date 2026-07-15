# Nightly Digital Bunker Vault

This Terraform module provisions a highly secure, versioned AWS S3 bucket, ideal for storing critical digital survival data, apocalyptic plans, or any information that needs to withstand the test of time and chaos.

## Features

-   **Versioning Enabled**: Keeps a complete history of all object versions, allowing for easy rollback and recovery from accidental deletions or modifications.
-   **Server-Side Encryption (SSE-S3)**: All data is encrypted at rest by default using AES256.
-   **Block Public Access**: Prevents any public access to the bucket, ensuring your sensitive data remains private.
-   **Optional Glacier Transition**: Automatically transitions older object versions to AWS Glacier for cost-effective long-term archival.
-   **Tagging Support**: Easily categorize and manage your bunker vaults with AWS tags.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
provider "aws" {
  region = "us-east-1" # Or your preferred AWS region
}

module "my_survival_vault" {
  source = "./nightly-digital-bunker-vault/src" # Adjust path as needed

  bucket_name = "my-apocalypsai-survival-data-vault-unique-name" # MUST be globally unique
  tags = {
    Project     = "ApocalypsAI"
    Environment = "Production"
    Purpose     = "SurvivalData"
  }
  enable_glacier_transition = true # Set to true to enable cost-effective long-term archival
}

output "vault_bucket_id" {
  value       = module.my_survival_vault.bucket_id
  description = "The name of the provisioned S3 bucket."
}

output "vault_bucket_arn" {
  value       = module.my_survival_vault.bucket_arn
  description = "The ARN of the provisioned S3 bucket."
}
```

## Inputs

| Name                      | Description                                                                                                                               | Type        | Default | Required |
|---------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|-------------|---------|----------|
| `bucket_name`             | The name of the S3 bucket. **Must be globally unique across all AWS accounts.**                                                           | `string`    | n/a     | yes      |
| `tags`                    | A map of tags to assign to the S3 bucket.                                                                                                 | `map(string)` | `{}`    | no       |
| `enable_glacier_transition` | Set to `true` to enable a lifecycle rule that transitions old object versions to Glacier after 30 days and expires them after 365 days. | `bool`      | `false` | no       |

## Outputs

| Name                 | Description                                    |
|----------------------|------------------------------------------------|
| `bucket_id`          | The ID (name) of the S3 bucket.                |
| `bucket_arn`         | The ARN of the S3 bucket.                      |
| `bucket_domain_name` | The S3 bucket's regional domain name.          |

## Requirements

-   Terraform `~> 1.0`
-   AWS Provider `~> 4.0`

## Testing

This module includes automated tests using `terraform test`. To run them:

```bash
cd nightly-digital-bunker-vault
terraform init
terraform test
```

Tests are designed to be deterministic and offline, asserting on the planned outputs and configurations without making actual AWS API calls.
