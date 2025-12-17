# Nightly Chrono-Vault: Digital Survival Cache

## Overview

The `nightly-chrono-vault` is a Terraform module designed to provision a highly resilient, versioned, and encrypted AWS S3 bucket. This "Chrono-Vault" acts as a digital survival cache, ideal for storing critical data, blueprints, encrypted messages, or any information you need to safeguard against digital entropy and unforeseen events.

It ensures data integrity and availability through features like versioning, server-side encryption, and lifecycle management for older data versions.

## Features

*   **Versioning Enabled**: Automatically keeps multiple versions of your objects, allowing recovery from accidental deletions or overwrites.
*   **Server-Side Encryption**: Protects your data at rest using AES256 or AWS KMS.
*   **Public Access Blocked**: Ensures the vault is private by default, preventing unintended public exposure.
*   **Lifecycle Management**: Configurable rules to transition older versions to cheaper storage classes (like Glacier) or expire them after a set period.
*   **TLS Enforcement**: A default bucket policy ensures all access is made over HTTPS.
*   **Optional Static Website Hosting**: Can be configured to host a simple static website, useful for a "manifest" or emergency instructions.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "my_survival_cache" {
  source = "./path/to/nightly-chrono-vault/src"

  bucket_name = "my-unique-apocalypsai-survival-cache-12345"
  # Required: A globally unique name for your S3 bucket.

  encryption_algorithm = "aws:kms" # Use AES256 or aws:kms
  kms_key_arn          = "arn:aws:kms:us-east-1:123456789012:key/your-kms-key-id" # Required if encryption_algorithm is aws:kms

  noncurrent_version_transition_days = 60 # Transition old versions to Glacier after 60 days
  noncurrent_version_expiration_days = 730 # Expire old versions after 2 years

  enable_static_website = true
  website_index_document = "emergency_manifest.html"
  website_error_document = "404.html"

  tags = {
    Environment = "Production"
    Project     = "ApocalypsAI"
    Owner       = "TheIntegrator"
  }
}

output "cache_bucket_id" {
  value = module.my_survival_cache.bucket_id
}

output "cache_website_endpoint" {
  value = module.my_survival_cache.website_endpoint
}
```

## Inputs

| Name                               | Description                                                                 | Type        | Default           | Required |
|------------------------------------|-----------------------------------------------------------------------------|-------------|-------------------|----------|
| `bucket_name`                      | The name of the S3 bucket to create. Must be globally unique.               | `string`    | n/a               | yes      |
| `encryption_algorithm`             | The server-side encryption algorithm to use. Can be 'AES256' or 'aws:kms'. | `string`    | `"AES256"`        | no       |
| `kms_key_arn`                      | The ARN of the KMS key to use if `encryption_algorithm` is 'aws:kms'.       | `string`    | `null`            | no       |
| `noncurrent_version_transition_days` | Number of days after which noncurrent versions transition to GLACIER.       | `number`    | `30`              | no       |
| `noncurrent_version_expiration_days` | Number of days after which noncurrent versions expire.                      | `number`    | `365`             | no       |
| `tags`                             | A map of tags to assign to the bucket.                                      | `map(string)` | `{}`              | no       |
| `attach_policy`                    | Whether to attach a default bucket policy (e.g., requiring TLS).            | `bool`      | `true`            | no       |
| `enable_static_website`            | Whether to enable static website hosting for the bucket.                    | `bool`      | `false`           | no       |
| `website_index_document`           | The name of the index document for static website hosting.                  | `string`    | `"index.html"`    | no       |
| `website_error_document`           | The name of the error document for static website hosting.                  | `string`    | `"error.html"`    | no       |

## Outputs

| Name                           | Description                                       |
|--------------------------------|---------------------------------------------------|
| `bucket_id`                    | The ID of the S3 bucket.                          |
| `bucket_arn`                   | The ARN of the S3 bucket.                         |
| `bucket_regional_domain_name`  | The regional domain name of the S3 bucket.        |
| `website_endpoint`             | The S3 bucket website endpoint (if enabled).      |

## Tests

The tests for this module are designed to be run offline and deterministically. They validate the Terraform syntax, variable definitions, and module structure without requiring AWS credentials or deploying actual resources.

To run the tests:

```bash
cd nightly-chrono-vault
./tests/test.sh
```

This script will perform `terraform init -backend=false`, `terraform validate`, and `terraform plan -destroy` within the `tests/` directory to ensure the module is correctly defined.
