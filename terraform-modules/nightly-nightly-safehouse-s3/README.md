# Nightly Safehouse S3

A whimsical Terraform module that provisions a secure S3 bucket for storing post‑apocalyptic supplies. The bucket has versioning, server‑side encryption, and a lifecycle rule that expires objects after 30 days.

## Usage

```hcl
module "safehouse_s3" {
  source = "./utils/terraform-modules/nightly-safehouse-s3"

  bucket_name = "my-safehouse-bucket"
}
```

## Inputs

| Name | Description | Type | Default |
|------|-------------|------|---------|
| bucket_name | Name of the S3 bucket | string | n/a |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | The ID of the created bucket |
| bucket_arn | The ARN of the bucket |

## Requirements

- Terraform >= 1.0
- AWS provider
