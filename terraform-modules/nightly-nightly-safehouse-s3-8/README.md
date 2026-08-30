# Nightly Safehouse S3 Terraform Module

## Overview

Creates an S3 bucket with versioning, server‑side encryption, and a lifecycle rule that deletes non‑current versions after 30 days—perfect for storing precious post‑apocalyptic data.

## Usage

```hcl
module "safehouse_s3" {
  source = "git::https://github.com/yourorg/ApocalypsAI.git//terraform-modules/nightly-safehouse-s3"

  bucket_name = "my-safe-house-bucket"
}
```

## Inputs

- `bucket_name` (string, required): Name of the bucket.

## Outputs

- `bucket_id` – The ID of the created bucket.

## Testing

Run `./tests/validate.sh` to ensure the module renders correctly.
