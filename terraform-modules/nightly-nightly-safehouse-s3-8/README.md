# Nightly Safehouse S3

A whimsical Terraform module that provisions a secure S3 bucket for your post‑apocalyptic safe‑house. The bucket has versioning, server‑side encryption, a random pet name prefix, and a lifecycle rule that deletes objects older than 30 days.

## Usage

```hcl
module "safehouse_s3" {
  source            = "./utils/terraform-modules/nightly-safehouse-s3"
  bucket_name_prefix = "safehouse"
}
```

## Inputs

- `bucket_name_prefix` (string, default `"safehouse"`): Prefix for the bucket name. A random pet name will be appended.

## Outputs

- `bucket_name`: The name of the created bucket.

## Requirements

- Terraform >= 1.0
- AWS provider

## Testing

Run `cd tests && ./validate.sh` to ensure the module validates.
