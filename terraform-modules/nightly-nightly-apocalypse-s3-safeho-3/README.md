# Apocalyptic S3 Safehouse

A whimsical Terraform module that creates a secure S3 bucket with server‑side encryption, versioning, and a lifecycle rule that deletes objects older than 30 days. Perfect for storing your post‑apocalypse backups.

## Usage

```hcl
module "safehouse" {
  source = "git::https://github.com/yourorg/apocalypsai.git//terraform-modules/nightly-apocalypse-s3-safehouse"

  bucket_name = "my‑post‑apoc‑backups"
}
```

## Variables

- `bucket_name` (string, required): Name of the S3 bucket.

## Outputs

- `bucket_id`: The ID of the created bucket.

## Requirements

- Terraform >= 1.0
- AWS provider

## Testing

Run `bash tests/test_main.sh` to verify the module contains the expected resources.
