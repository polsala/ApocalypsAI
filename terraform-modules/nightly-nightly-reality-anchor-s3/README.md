# Nightly Reality Anchor S3

## Overview

In the ever-shifting digital landscape, where temporal anomalies and data drifts are a constant threat, the `nightly-reality-anchor-s3` module provides a stable, observable point of reference. This Terraform module provisions a highly available AWS S3 bucket configured with robust security, versioning, and encryption, designed to act as a 'digital anchor point'.

Think of it as a cosmic buoy in the sea of data, always there, always stable, providing a baseline against which other, more volatile systems can be measured. While it doesn't actively detect anomalies, its consistent presence and immutable (when versioned) nature make it an ideal candidate for a foundational, low-cost, and resilient component in any ApocalypsAI-managed infrastructure.

## Features

*   **High Availability**: Leverages AWS S3's inherent durability and availability.
*   **Versioning Enabled**: Protects against accidental deletions and allows for easy recovery of previous states.
*   **Server-Side Encryption**: Ensures data at rest is encrypted by default (AES256).
*   **Public Access Blocked**: Enforces strict private access, preventing unintended data exposure.
*   **Minimalist Design**: Focuses on core S3 features essential for an anchor point.

## Usage

To use this module, you need to have Terraform installed and configured with AWS credentials. The module requires the `aws` provider.

```terraform
# main.tf

provider "aws" {
  region = "us-east-1" # Or your preferred AWS region
}

module "reality_anchor" {
  source = "./path/to/nightly-reality-anchor-s3/src"

  # Optional: Customize the bucket name prefix
  bucket_name_prefix = "my-apocalypsai-anchor-"

  # Optional: Add custom tags
  tags = {
    Owner       = "ApocalypsAI-Team"
    Environment = "Staging"
  }
}

output "anchor_bucket_id" {
  value       = module.reality_anchor.bucket_id
  description = "The ID (name) of the created S3 bucket."
}

output "anchor_bucket_arn" {
  value       = module.reality_anchor.bucket_arn
  description = "The ARN of the created S3 bucket."
}
```

Run `terraform init`, `terraform plan`, and `terraform apply` to provision the bucket.

## Inputs

| Name                 | Description                                                              | Type        | Default                               | Required |
|----------------------|--------------------------------------------------------------------------|-------------|---------------------------------------|----------|
| `bucket_name_prefix` | A unique prefix for the S3 bucket name. Terraform will append a random string. | `string`    | `"apocalypsai-reality-anchor-"`      | no       |
| `tags`               | A map of tags to assign to the S3 bucket.                                | `map(string)` | `{ Project = "ApocalypsAI", Environment = "Production", ManagedBy = "ApocalypsAI-Integrator", Purpose = "RealityAnchor" }` | no       |

## Outputs

| Name           | Description                               | Value |
|----------------|-------------------------------------------|-------|
| `bucket_id`    | The ID (name) of the created S3 bucket.   | `string` |
| `bucket_arn`   | The ARN of the created S3 bucket.         | `string` |
