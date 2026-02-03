# Nightly Safehouse S3 Module

A whimsical Terraform module that creates a secure S3 bucket, perfect for storing your post‑apocalyptic supplies, logs, or secret maps.

## Features

- Bucket with server‑side encryption (AES‑256)
- Versioning enabled
- Lifecycle rule to delete non‑current versions after 30 days
- Optional public access block
- Outputs bucket name and ARN

## Usage

```hcl
module "safehouse" {
  source = "github.com/yourorg/polsala//terraform-modules/nightly-safehouse-s3-module"

  bucket_name = "my‑safehouse‑bucket"
}
```

## Inputs

| Name                | Description                     | Type   | Default | Required |
|---------------------|---------------------------------|--------|---------|----------|
| bucket_name         | Name of the S3 bucket           | string | n/a     | yes      |
| force_destroy       | Allow destroying non‑empty bucket | bool   | false   | no       |
| block_public_access | Enable S3 Block Public Access   | bool   | true    | no       |

## Outputs

| Name       | Description               |
|------------|---------------------------|
| bucket_id  | The name of the bucket    |
| bucket_arn | The ARN of the bucket     |
