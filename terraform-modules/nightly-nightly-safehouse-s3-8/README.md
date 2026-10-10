# Safehouse S3 Terraform Module

## Overview

Creates an S3 bucket with versioning enabled and a lifecycle rule that transitions objects to Glacier after 30 days and expires after 365 days. Ideal for storing post‑apocalyptic data backups.

## Usage

```hcl
module "safehouse_s3" {
  source = "github.com/yourorg/apocalypsai//terraform-modules/nightly-safehouse-s3"

  bucket_name = "my-safehouse-bucket"
}
```

## Inputs

- `bucket_name` (string, required): Name of the bucket.

## Outputs

- `bucket_id` – The ID of the created bucket.

## Testing

Run the validation script:

```sh
cd tests && ./validate.sh
```
