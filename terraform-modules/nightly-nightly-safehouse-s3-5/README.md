# Safehouse S3 Terraform Module

Provision an S3 bucket with versioning, server‑side encryption, and a lifecycle rule that transitions objects to Glacier after 30 days and deletes after 365 days. The bucket name is generated with a random suffix to avoid collisions.

## Usage

```hcl
module "safehouse_s3" {
  source = "github.com/yourorg/apocalypsai//terraform-modules/nightly-safehouse-s3"

  bucket_prefix = "safehouse"
  tags = {
    Environment = "post-apocalypse"
  }
}
```

## Inputs

- `bucket_prefix` (string, required): Prefix for bucket name.
- `tags` (map(string), optional): Tags to apply.

## Outputs

- `bucket_name` – The name of the created bucket.
- `bucket_arn` – The ARN of the bucket.

## Requirements

- Terraform >= 1.0
- AWS provider

## Testing

Run `tests/test_main.sh` from the module root.
