# Nightly Apocalypse Safehouse S3

## Overview
Terraform module that creates an S3 bucket configured for durability and security, ideal for storing critical post‑apocalyptic data.

## Features
- Bucket name configurable
- Server‑side encryption (AES‑256)
- Versioning enabled
- Lifecycle rule to expire non‑current versions after 30 days
- Optional tags

## Usage
```hcl
module "safehouse_s3" {
  source      = "./"
  bucket_name = "my-safehouse-bucket"
  tags = {
    Environment = "post-apocalypse"
  }
}
```

## Inputs
| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| bucket_name | Name of the S3 bucket | string | n/a | yes |
| tags | Map of tags to apply | map(string) | {} | no |

## Outputs
| Name | Description |
|------|-------------|
| bucket_id | The ID of the created bucket |
| bucket_arn | ARN of the bucket |

## Testing
Run `./tests/test_module.sh` to validate the module.
