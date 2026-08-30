# Nightly Wasteland Safehouse S3

A whimsical Terraform module that provisions an S3 bucket representing a post‑apocalyptic safe‑house. The bucket has versioning, server‑side encryption, a lifecycle rule to delete objects older than 30 days, and a custom tag `radiation_level` that can be set to `low`, `moderate`, or `high`.

## Usage

```hcl
module "safehouse" {
  source          = "./src"
  bucket_name     = "my-safehouse-bucket"
  radiation_level = "moderate"
}
```

## Inputs

- `bucket_name` (string, required): Name of the S3 bucket.
- `radiation_level` (string, optional, default `"low"`): Tag value indicating radiation.
- `aws_region` (string, optional, default `"us-east-1"`): AWS region for the provider.

## Outputs

- `bucket_id`: The ID of the created bucket.
- `bucket_arn`: The ARN of the bucket.

## Notes

- The module uses the AWS provider; ensure credentials are available when applying.
- The lifecycle rule only applies to objects with the tag `RadiationLevel` matching the supplied `radiation_level`.
