# nightly-safehouse-s3-bucket

Terraform module that provisions a secure S3 bucket for post‑apocalyptic safe‑house data storage.

## Features
- Versioning enabled
- Server‑side encryption (AES‑256)
- Lifecycle rule to delete objects older than 30 days
- Optional bucket name input

## Usage

```hcl
module "safehouse_bucket" {
  source = "./path/to/nightly-safehouse-s3-bucket"

  bucket_name = "my-safehouse-bucket"
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| bucket_name | Name of the S3 bucket | string | null | no (if omitted, a random name is generated) |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | The ID of the created bucket |
| bucket_arn | The ARN of the created bucket |
