# Nightly Safehouse S3

## Overview

A whimsical Terraform module that creates a secure S3 bucket, versioned, encrypted, with a lifecycle rule to delete objects older than 30 days. The bucket name is generated using the `random_pet` resource to give it a post‑apocalyptic safe‑house feel.

## Usage

```hcl
module "safehouse" {
  source        = "./"
  bucket_prefix = "safehouse"
}
```

## Inputs

- `bucket_prefix` (string, default `"safehouse"`): Prefix for the bucket name.

## Outputs

- `bucket_id`: The ID of the created bucket.
- `bucket_arn`: The ARN of the bucket.

## Requirements

- Terraform >= 1.0
- AWS provider
