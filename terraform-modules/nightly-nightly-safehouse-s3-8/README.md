# Nightly Safehouse S3 Terraform Module

## Overview
Creates a secure S3 bucket with versioning, server‑side encryption, a lifecycle rule that expires objects after a configurable number of days, and attaches a read/write IAM policy to a specified IAM role. Perfect for storing critical post‑apocalyptic data without worrying about accidental deletions.

## Usage
```hcl
module "safehouse_s3" {
  source          = "./path/to/nightly-safehouse-s3"
  bucket_name     = "my-post-apoc-vault"
  iam_role_name   = "safehouse-role"
  expiration_days = 30
}
```

## Variables
- `bucket_name` (string, required): Name of the S3 bucket.
- `iam_role_name` (string, required): Name of the IAM role to attach the policy.
- `expiration_days` (number, optional, default = 30): Days after which objects are deleted.

## Outputs
- `bucket_id` – The ID of the created bucket.
- `bucket_arn` – The ARN of the created bucket.

## Testing
Run the provided test script:
```bash
cd utils/terraform-modules/nightly-safehouse-s3
chmod +x tests/test.sh
./tests/test.sh
```
The script runs `terraform init` and `terraform validate` using a mock AWS provider configuration.
