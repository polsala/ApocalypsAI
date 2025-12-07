# Nightly Digital Data Bunker

A Terraform module designed to provision a secure, low-cost cloud storage solution for your most critical post-apocalyptic data. Think of it as your digital fallout shelter, protecting precious blueprints, survival guides, and meme archives from the ravages of time and digital decay.

## Features

*   **Secure S3 Bucket**: A dedicated S3 bucket with server-side encryption (KMS), versioning enabled, and public access blocked by default.
*   **Glacier Archival**: Automatically transitions older, less frequently accessed data to AWS Glacier for significant cost savings, ensuring long-term preservation.
*   **KMS Encryption**: Uses an AWS Key Management Service (KMS) key for robust encryption of your data at rest.
*   **Whimsical Naming**: Resources are named with a touch of post-apocalyptic charm.

## Usage

To deploy your Digital Data Bunker, include this module in your Terraform configuration:

```terraform
module "data_bunker" {
  source = "./src" # Or a Git/S3 source if published

  bunker_name_prefix = "my-survival-vault"
  aws_region         = "us-east-1"
  tags = {
    Environment = "Apocalypse"
    Project     = "DataPreservation"
  }
}

output "bunker_s3_id" {
  description = "The ID of the S3 bucket (your digital bunker)."
  value       = module.data_bunker.bunker_id
}

output "bunker_s3_arn" {
  description = "The ARN of the S3 bucket."
  value       = module.data_bunker.bunker_arn
}

output "kms_key_arn" {
  description = "The ARN of the KMS key used for encryption."
  value       = module.data_bunker.kms_key_arn
}
```

### Requirements

*   Terraform CLI (v1.0.0 or higher)
*   Configured AWS credentials (for actual deployment, not for testing)

## Module Inputs

| Name                 | Description                                       | Type          | Default                      | Required |
| :------------------- | :------------------------------------------------ | :------------ | :--------------------------- | :------- |
| `bunker_name_prefix` | Prefix for the S3 bucket name. A random suffix will be added. | `string`      | `"apocalypsai-data-bunker"` | no       |
| `aws_region`         | AWS region to deploy the bunker in.               | `string`      | `"us-east-1"`                | no       |
| `tags`               | A map of tags to apply to all resources.          | `map(string)` | `{}`                         | no       |

## Module Outputs

| Name          | Description                                   |
| :------------ | :-------------------------------------------- |
| `bunker_id`   | The ID of the S3 bucket (your digital bunker). |
| `bunker_arn`  | The ARN of the S3 bucket.                     |
| `kms_key_arn` | The ARN of the KMS key used for encryption.   |

## Development & Testing

Tests are run using `terraform validate` against a minimal test configuration. This ensures the module's HCL syntax and configuration logic are correct without requiring actual cloud deployments.

```bash
./tests/run_tests.sh
```
