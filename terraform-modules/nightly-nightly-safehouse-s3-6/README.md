# Nightly Safehouse S3

A tiny Terraform module that creates an S3 bucket configured for versioning and a lifecycle rule that deletes objects older than 30 days, ideal for storing supplies in a post‑apocalyptic safehouse.

## Usage

```hcl
module "safehouse_s3" {
  source      = "./"
  bucket_name = "my-safehouse-supplies"
}
```

## Inputs

- `bucket_name` (string, required): Name of the S3 bucket.

## Outputs

- `bucket_id` – The ID of the created bucket.

Run `terraform init` and `terraform apply`.
