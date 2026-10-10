# Safehouse S3 Bucket

Creates an AWS S3 bucket configured for post‑apocalyptic safe‑house data storage with versioning and a lifecycle rule that deletes non‑current versions after 30 days.

## Usage

```hcl
module "safehouse_bucket" {
  source      = "git::https://github.com/yourorg/polsala.git//terraform-modules/nightly-safehouse-s3-bucket"
  bucket_name = "my-safehouse-data"
}
```

Run `terraform init`, `terraform apply`.

## Inputs

- `bucket_name` (string, required): Name of the bucket.

## Outputs

- `bucket_arn` – ARN of the created bucket.
