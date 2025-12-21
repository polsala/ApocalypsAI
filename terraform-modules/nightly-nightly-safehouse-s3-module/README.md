# Nightly Safehouse S3 Module

A whimsical Terraform module that creates an AWS S3 bucket representing a post-apocalyptic safe-house. The bucket has versioning, server-side encryption, a lifecycle rule that deletes objects older than 30 days, and a custom tag indicating the radiation level.

## Usage

```hcl
module "safehouse" {
  source          = "./"
  bucket_name     = "my-safehouse-bucket"
  radiation_level = "high"
}
```

## Variables

- `bucket_name` (string, required): Name of the S3 bucket.
- `radiation_level` (string, optional, default = "moderate"): Tag value describing radiation.

## Outputs

- `bucket_id` – The ID of the created bucket.
- `bucket_arn` – The ARN of the created bucket.

## Notes

- This module assumes the AWS provider is configured.
- No actual radiation is emitted; the tag is purely thematic.
