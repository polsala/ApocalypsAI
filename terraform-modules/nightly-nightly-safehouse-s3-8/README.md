# Safehouse S3 Terraform Module

## Overview

Creates an S3 bucket configured for post‑apocalyptic supply storage:

- Versioning enabled
- Server‑side encryption (AES‑256)
- Lifecycle rule to delete objects older than 30 days
- Optional tags

## Usage

```hcl
module "safehouse" {
  source      = "git::https://github.com/yourorg/apocalypsai.git//terraform-modules/nightly-safehouse-s3"
  bucket_name = "my-apocalypse-supplies"
  tags = {
    Environment = "production"
    Project     = "Safehouse"
  }
}
```

Run `terraform init` and `terraform apply`.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| bucket_name | Name of the S3 bucket | string | n/a | yes |
| tags | Map of tags to assign | map(string) | {} | no |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | ID of the bucket |
| bucket_arn | ARN of the bucket |
