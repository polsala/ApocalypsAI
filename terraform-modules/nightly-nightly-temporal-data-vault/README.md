# Nightly Temporal Data Vault

## Overview

In the ever-shifting sands of the post-apocalyptic landscape, data integrity is paramount. The `nightly-temporal-data-vault` is a whimsical-yet-critical Terraform module designed to provision a highly secure, versioned AWS S3 bucket. This "vault" is intended to store your most vital temporal data, ensuring that even if timelines ripple or reality itself frays, your information remains accessible and recoverable through its various historical states.

It's perfect for storing critical configuration backups, historical logs, or even your most cherished recipes for irradiated squirrel stew, safe from both digital decay and temporal anomalies.

## Features

*   **Versioned Storage**: Keeps multiple versions of your objects, allowing you to recover from accidental deletions or overwrites, or even revert to a previous timeline's data state.
*   **Server-Side Encryption (SSE-S3)**: All data at rest is automatically encrypted with AES256, providing a basic layer of security.
*   **Public Access Block**: Ensures the bucket is not publicly accessible, protecting your sensitive temporal data from unintended exposure.
*   **Incomplete Multipart Upload Abort**: Automatically cleans up incomplete multipart uploads after 7 days to manage storage costs and prevent orphaned data fragments.

## Usage

To use this module, include it in your Terraform configuration and provide the necessary inputs.

### Example

```terraform
provider "aws" {
  region = "us-east-1" # Or your desired AWS region
}

module "my_temporal_vault" {
  source = "./path/to/nightly-temporal-data-vault/src"

  bucket_name = "my-critical-temporal-archive"
  tags = {
    Environment = "Production"
    Owner       = "ApocalypsAI-Team"
    DataTier    = "Critical"
  }
  region = "us-east-1"
}

output "vault_bucket_name" {
  description = "The name of the created Temporal Data Vault S3 bucket."
  value       = module.my_temporal_vault.bucket_name
}

output "vault_bucket_arn" {
  description = "The ARN of the created Temporal Data Vault S3 bucket."
  value       = module.my_temporal_vault.bucket_arn
}
```

### Inputs

| Name        | Description                                     | Type        | Default                                 | Required |
| :---------- | :---------------------------------------------- | :---------- | :-------------------------------------- | :------- |
| `bucket_name` | The name of the S3 bucket for the Temporal Data Vault. | `string`    | `"apocalypsai-temporal-data-vault"` | no       |
| `tags`        | A map of tags to assign to the bucket.          | `map(string)` | `{ Project = "ApocalypsAI", ManagedBy = "NightlyIntegrator", Purpose = "TemporalDataVault" }` | no       |
| `region`      | AWS region where the bucket will be created.    | `string`    | `"us-east-1"`                           | no       |

### Outputs

| Name          | Description                                     |
| :------------ | :---------------------------------------------- |
| `bucket_id`   | The ID of the created S3 bucket.                |
| `bucket_arn`  | The ARN of the created S3 bucket.               |
| `bucket_name` | The name of the created S3 bucket.              |

## Testing

To run the automated tests for this module, navigate to the utility's root directory and execute the `test.sh` script:

```bash
./tests/test.sh
```

This script performs static analysis and content verification to ensure the module's syntax is correct and critical security/versioning features are declared, without requiring actual AWS credentials or network access.
