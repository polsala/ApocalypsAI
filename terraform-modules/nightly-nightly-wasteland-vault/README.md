# Nightly Wasteland Vault

A Terraform module to provision a secure, minimal AWS S3 vault for critical post-apocalyptic data. This vault is designed to be resilient, private, and cost-effective, perfect for safeguarding your most precious digital artifacts in the digital wasteland.

## Features

*   **Secure S3 Bucket**: Provisions an AWS S3 bucket with best practices for security.
*   **Encryption**: Server-side encryption (SSE-S3) enabled by default.
*   **Versioning**: Keeps multiple versions of objects, protecting against accidental deletions or overwrites.
*   **Public Access Block**: Prevents accidental public exposure of your vault's contents.
*   **Minimalist**: Focuses on essential features to keep costs low and complexity manageable.

## Usage

To use this module, include it in your Terraform configuration:

```terraform
module "wasteland_vault" {
  source = "./path/to/nightly-wasteland-vault/src" # Adjust path as necessary
  
  bucket_name_prefix = "apocalypsai-vault"
  environment        = "production"
  tags = {
    Project   = "ApocalypsAI"
    ManagedBy = "NightlyIntegrator"
  }
}

output "vault_bucket_id" {
  description = "The ID of the Wasteland Vault S3 bucket."
  value       = module.wasteland_vault.bucket_id
}

output "vault_bucket_arn" {
  description = "The ARN of the Wasteland Vault S3 bucket."
  value       = module.wasteland_vault.bucket_arn
}
```

### Inputs

| Name                 | Description                                                                 | Type          | Default | Required |
|----------------------|-----------------------------------------------------------------------------|---------------|---------|----------|
| `bucket_name_prefix` | A prefix for the S3 bucket name. A unique suffix will be appended.          | `string`      | n/a     | yes      |
| `environment`        | The environment name (e.g., "dev", "prod") to include in the bucket name.   | `string`      | n/a     | yes      |
| `tags`               | A map of tags to apply to the S3 bucket.                                    | `map(string)` | `{}`    | no       |

### Outputs

| Name               | Description                                  |
|--------------------|----------------------------------------------|
| `bucket_id`        | The ID (name) of the created S3 bucket.      |
| `bucket_arn`       | The ARN of the created S3 bucket.            |
| `bucket_domain_name` | The domain name of the created S3 bucket.  |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 4.0`

## Development & Testing

The module includes a `tests/` directory with an example configuration and a bash script to validate and plan the module without actual deployment.

To run tests:
```bash
cd tests
chmod +x test_vault.sh
./test_vault.sh
```
