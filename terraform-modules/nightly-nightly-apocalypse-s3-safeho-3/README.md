# Apocalyptic Safehouse S3 Bucket

This Terraform module provisions an AWS S3 bucket configured as a resilient safe‑house for your post‑apocalyptic data.

## Features

- Versioning enabled
- Server‑side encryption (AES‑256)
- Lifecycle rule: transition to Glacier after 30 days, delete after 365 days
- Optional public‑read block

## Usage

```hcl
module "safehouse" {
  source                = "./"
  bucket_name           = "my-apocalypse-store"
  enable_public_access  = false
}
```

## Inputs

| Name                 | Description                     | Type   | Default |
|----------------------|---------------------------------|--------|---------|
| `bucket_name`        | Name of the S3 bucket           | string | n/a     |
| `enable_public_access` | Whether to allow public read access | bool   | false   |

## Outputs

| Name       | Description                |
|------------|----------------------------|
| `bucket_arn` | ARN of the created bucket |
| `bucket_id`  | ID of the bucket           |

Run `terraform init` and `terraform apply`.
