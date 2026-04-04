# Nightly Safehouse S3 Terraform Module

Creates an S3 bucket named with a random pet name, with versioning, server‑side encryption (AES256), and a lifecycle rule to delete non‑current versions after 30 days. Useful for storing post‑apocalyptic logs, backups, or supplies.

## Usage

```hcl
module "safehouse_s3" {
  source = "git::https://github.com/yourorg/polsala.git//terraform-modules/nightly-safehouse-s3"
}
```

## Requirements

- Terraform >= 1.0
- AWS provider

## Inputs

_None._

## Outputs

- `bucket_name` – Name of the created S3 bucket
- `bucket_arn` – ARN of the created S3 bucket

## Testing

Run the validation script:

```bash
./tests/validate.sh
```
