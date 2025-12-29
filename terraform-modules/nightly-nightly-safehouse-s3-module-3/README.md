# nightly-safehouse-s3-module

## Overview

Terraform module that creates an S3 bucket configured for durability and security, ideal for storing critical data in a post‑apocalyptic setting.

**Features**:
- Bucket name is configurable.
- Server‑side encryption (AES‑256).
- Versioning enabled.
- Lifecycle rule to delete non‑current versions after 30 days.
- Optional tags.

## Usage

```hcl
module "safehouse_bucket" {
  source = "./src"

  bucket_name = "my-safehouse-bucket"
  tags = {
    Environment = "post-apocalypse"
  }
}
```

Run `terraform init`, `terraform apply`.

## Inputs

| Name | Description | Type | Default |
|------|-------------|------|---------|
| bucket_name | Name of the S3 bucket | string | n/a |
| tags | Tags to apply to the bucket | map(string) | {} |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | The ID of the created bucket |
| bucket_arn | ARN of the bucket |

## Testing

```sh
cd tests && ./test_validate.sh
```
