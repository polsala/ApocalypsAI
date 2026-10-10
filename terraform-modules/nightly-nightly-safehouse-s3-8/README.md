# Nightly Safehouse S3

Terraform module that creates an S3 bucket with versioning, server‑side encryption, and a lifecycle rule that transitions objects to Glacier after 30 days and deletes after 365 days. Ideal for storing backups of community resources in a post‑apocalyptic setting.

## Usage

```hcl
module "safehouse_s3" {
  source      = "./"
  bucket_name = "my-safehouse-data"
  tags = {
    Environment = "post-apocalypse"
    Owner       = "community"
  }
}
```

## Inputs

- `bucket_name` (string, required): Name of the bucket. Must be globally unique.
- `tags` (map(string), optional): Tags to apply.

## Outputs

- `bucket_id` – The ID of the created bucket.
- `bucket_arn` – The ARN of the bucket.

## Testing

Run `./tests/validate.sh` from the module root.
