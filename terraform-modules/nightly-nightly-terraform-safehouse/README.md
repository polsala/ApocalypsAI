# Terraform Safehouse S3 Module

## Overview

Creates an S3 bucket with:

- Randomized name (using random_pet)
- Server‑side encryption (AES‑256)
- Versioning enabled
- Lifecycle rule to delete non‑current versions after 30 days
- Optional tags

## Usage

```hcl
module "safehouse_s3" {
  source = "./"
  bucket_prefix = "safehouse"
  tags = {
    Environment = "post-apocalypse"
  }
}
```

## Inputs

| Name | Description | Type | Default |
|------|-------------|------|---------|
| bucket_prefix | Prefix for bucket name | string | "safehouse" |
| tags | Tags to apply to bucket | map(string) | {} |
| aws_region | AWS region for resources | string | "us-east-1" |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | The name of the created bucket |
| bucket_arn | ARN of the bucket |

## Testing

Run `./tests/test_main.sh` to validate the module.
