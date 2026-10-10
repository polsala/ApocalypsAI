# Nightly Safehouse S3 Terraform Module

## Overview
Creates an AWS S3 bucket configured for a post‑apocalyptic safe‑house: versioning enabled, encryption at rest, and a lifecycle rule that expires non‑current object versions after 30 days.

## Usage
```hcl
module "safehouse_s3" {
  source      = "git::https://github.com/yourorg/ApocalypsAI.git//terraform-modules/nightly-safehouse-s3"
  bucket_name = "my-safehouse-bucket"
  tags = {
    Environment = "production"
    Project     = "safehouse"
  }
}
```

## Variables
- `bucket_name` (string, required): Name of the S3 bucket.
- `tags` (map(string), optional): Tags to apply.

## Outputs
- `bucket_id` – The ID of the bucket.
- `bucket_arn` – The ARN of the bucket.

## Testing
Run `tests/validate.sh` to ensure the module contains required resources.
