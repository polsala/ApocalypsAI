# Nightly Safehouse S3 Terraform Module

Creates an S3 bucket configured as a post‑apocalyptic safe‑house: versioning enabled, server‑side encryption, and a lifecycle rule that expires objects after 30 days.

## Usage

```hcl
module "safehouse" {
  source      = "github.com/yourorg/polsala/terraform-modules//nightly-safehouse-s3"
  bucket_name = "my-safehouse-bucket"
  tags = {
    Environment = "production"
    Project     = "ApocalypsAI"
  }
}
```

## Inputs

- `bucket_name` (string, required): Name of the bucket.
- `tags` (map(string), optional): Tags to apply.

## Outputs

- `bucket_id` – The ID of the created bucket.

## Requirements

- Terraform >= 1.0
- AWS provider
