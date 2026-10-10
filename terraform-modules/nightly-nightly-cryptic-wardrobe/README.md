# Cryptic Wardrobe Terraform Module

## Overview

This Terraform module provisions a **secret wardrobe** – an S3 bucket with versioning enabled, a random suffix to keep the name obscure, and a strict bucket policy that only allows a specified IAM role to access its contents. Perfect for stashing apocalypse‑level supplies out of sight.

## Features

- Bucket name is a combination of a user‑defined prefix and a random suffix.
- Versioning is always enabled to protect against accidental deletions.
- Bucket policy denies public access and grants full S3 permissions to a single IAM role you specify.

## Usage Example

```hcl
module "cryptic_wardrobe" {
  source               = "./nightly-cryptic-wardrobe"
  bucket_name_prefix   = "my‑secret‑wardrobe"
  allowed_role_arn     = "arn:aws:iam::123456789012:role/ApocalypseKeeper"
}

output "wardrobe_bucket" {
  value = module.cryptic_wardrobe.bucket_name
}
```

## Variables

| Name | Type | Description | Default |
|------|------|-------------|---------|
| `bucket_name_prefix` | `string` | Prefix for the generated bucket name. | `"cryptic-wardrobe"` |
| `allowed_role_arn` | `string` | IAM Role ARN that is allowed to access the bucket. | n/a |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_name` | The name of the created S3 bucket. |

## Testing

Run the provided test script to ensure the module validates and produces a bucket name with the correct prefix:

```bash
cd nightly-cryptic-wardrobe
bash tests/test_module.sh
```

## Requirements

- Terraform >= 1.0
- AWS provider configured with appropriate credentials

---

*Created by the ApocalypsAI Nightly Integrator*
