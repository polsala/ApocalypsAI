# nightly-terraform-s3-bucket

## Summary
Terraform module that creates an S3 bucket with server‑side encryption, versioning, and optional public access block.

## Usage
```hcl
module "secure_bucket" {
  source = "./utils/nightly-terraform-s3-bucket"

  bucket_name          = "my-app-data"
  versioning           = true
  block_public_access  = true
  tags = {
    Environment = "dev"
    Owner       = "team-a"
  }
}
```

## Variables
- **bucket_name** (string, required): Name of the bucket.
- **versioning** (bool, default `true`): Enable versioning.
- **block_public_access** (bool, default `true`): Enable public access block.
- **tags** (map(string), optional): Tags to apply to the bucket.

## Outputs
- **bucket_id** – ID of the S3 bucket.
- **bucket_arn** – ARN of the S3 bucket.
