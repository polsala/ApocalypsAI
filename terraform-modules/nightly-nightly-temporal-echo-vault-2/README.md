# Nightly Temporal Echo Vault

This Terraform module provisions a highly secure AWS S3 bucket, whimsically named the "Temporal Echo Vault." Its purpose is to safely store critical temporal anomaly logs, interdimensional whispers, and other sensitive data that requires robust protection against cosmic fluctuations and unauthorized access.

## Features

*   **Secure Storage**: Configures an S3 bucket with server-side encryption (SSE-S3) by default.
*   **Data Integrity**: Enables versioning to protect against accidental deletions or overwrites.
*   **Access Control**: Blocks all public access to the bucket.
*   **Whimsical Naming**: Automatically generates a unique bucket name based on a provided prefix, suitable for ApocalypsAI operations.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "temporal_echo_vault" {
  source = "./nightly-temporal-echo-vault" # Or a Git/registry source in a real scenario

  bucket_name_prefix = "apocalypsai-echo-logs"
  tags = {
    Project     = "ApocalypsAI"
    Environment = "Production"
    Purpose     = "TemporalEchoStorage"
  }
}

output "vault_bucket_id" {
  description = "The ID of the Temporal Echo Vault S3 bucket."
  value       = module.temporal_echo_vault.bucket_id
}

output "vault_bucket_arn" {
  description = "The ARN of the Temporal Echo Vault S3 bucket."
  value       = module.temporal_echo_vault.bucket_arn
}
```

## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement_terraform) | >= 1.0 |
| <a name="requirement_aws"></a> [aws](#requirement_aws) | >= 4.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider_aws) | >= 4.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_bucket_name_prefix"></a> [bucket_name_prefix](#input_bucket_name_prefix) | A prefix for the S3 bucket name. A random suffix will be appended for uniqueness. | `string` | `"temporal-echo-vault"` | no |
| <a name="input_tags"></a> [tags](#input_tags) | A map of tags to assign to the S3 bucket. | `map(string)` | `{}` | no |

## Outputs

| Name | Description | Value |
|------|-------------|-------|
| <a name="output_bucket_arn"></a> [bucket_arn](#output_bucket_arn) | The ARN of the Temporal Echo Vault S3 bucket. | `string` |
| <a name="output_bucket_id"></a> [bucket_id](#output_bucket_id) | The ID (name) of the Temporal Echo Vault S3 bucket. | `string` |
