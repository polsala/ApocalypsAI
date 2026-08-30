# Apocalyptic Safehouse S3 Bucket

This Terraform module creates an AWS S3 bucket configured for long‑term, immutable storage—perfect for safeguarding critical data in a post‑apocalyptic scenario.

## Features
- Versioning enabled
- Server‑side encryption (AES‑256)
- Lifecycle rule to transition objects to Glacier after 30 days and expire after 365 days
- Optional public read block

## Usage

```hcl
module "safehouse_s3" {
  source = "./nightly-apocalypse-safeguard-s3"

  bucket_name = "my-safehouse-bucket"
  enable_public_access_block = false
}
```

## Inputs

| Name | Description | Type | Default |
|------|-------------|------|---------|
| bucket_name | Name of the S3 bucket | string | n/a |
| enable_public_access_block | Whether to block public ACLs and policies | bool | true |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | The ID of the created bucket |
| bucket_arn | The ARN of the created bucket |
