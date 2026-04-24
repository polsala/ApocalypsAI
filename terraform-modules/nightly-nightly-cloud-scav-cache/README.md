# Nightly Cloud Scavenger Cache

This Terraform module provisions a highly durable and available AWS S3 bucket, designed to act as a "scavenger cache" for storing critical, small bits of data in the cloud. Think of it as your digital tin can buried in the cloud, but with enterprise-grade resilience, versioning, and encryption!

## Features

*   **High Durability & Availability:** Leverages AWS S3's inherent design for 99.999999999% (11 nines) durability.
*   **Versioning Enabled:** Automatically keeps multiple versions of your objects, protecting against accidental deletions or overwrites.
*   **Server-Side Encryption (SSE-S3):** All data is encrypted at rest by default using AES256.
*   **Secure by Default:** Blocks all public access to ensure your scavenged data remains private.
*   **Configurable Naming:** Allows for a custom prefix for your bucket name.
*   **Tagging Support:** Easily categorize and manage your caches with AWS tags.

## Why is this useful?

In a world of uncertainty, having a reliable, secure, and easily accessible place to stash vital information – be it coordinates, survival notes, encrypted messages, or small configuration files – is paramount. This module provides that digital safe haven, ensuring your data survives even if other systems fail.

## Usage

To use this module, include it in your root Terraform configuration:

```terraform
module "my_scavenger_cache" {
  source = "./path/to/this/module/src" # Adjust path as needed

  bucket_name_prefix = "my-secret-stash"
  tags = {
    Owner       = "ApocalypsAI-Survivor"
    Purpose     = "Critical-Intel"
    ExpiryDate  = "2042-10-27"
  }
}

output "cache_bucket_id" {
  value = module.my_scavenger_cache.bucket_id
}

output "cache_bucket_arn" {
  value = module.my_scavenger_cache.bucket_arn
}
```

## Inputs

| Name               | Description                                                 | Type        | Default                               |
|--------------------|-------------------------------------------------------------|-------------|---------------------------------------|
| `bucket_name_prefix` | A prefix for the S3 bucket name. Terraform will append a unique suffix. | `string`    | `"apocalypsai-scavenger-cache"`      |
| `tags`             | A map of tags to assign to the S3 bucket.                   | `map(string)` | `{ Project = "ApocalypsAI", Environment = "production", ManagedBy = "ApocalypsAI-Integrator" }` |

## Outputs

| Name                 | Description                               | Value                                   |
|----------------------|-------------------------------------------|-----------------------------------------|
| `bucket_id`          | The ID (name) of the S3 bucket.           | `aws_s3_bucket.scavenger_cache.id`      |
| `bucket_arn`         | The ARN of the S3 bucket.                 | `aws_s3_bucket.scavenger_cache.arn`     |
| `bucket_domain_name` | The S3 bucket regional domain name.       | `aws_s3_bucket.scavenger_cache.bucket_regional_domain_name` |
