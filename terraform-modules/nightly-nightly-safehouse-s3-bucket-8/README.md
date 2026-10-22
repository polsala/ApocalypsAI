# Safehouse S3 Bucket

Terraform module that creates a secure S3 bucket with versioning, server‑side encryption, and a lifecycle rule that expires objects after 30 days. Ideal for storing critical post‑apocalyptic data.

## Usage

```hcl
module "safehouse_bucket" {
  source              = "./src"
  bucket_name_prefix  = "my-safehouse"
}
```

## Inputs

- `bucket_name_prefix` (string, required): Prefix for the bucket name; a random suffix will be added.
- `tags` (map(string), optional): Tags to apply to the bucket.

## Outputs

- `bucket_id` – The name of the bucket.
- `bucket_arn` – The ARN of the bucket.
