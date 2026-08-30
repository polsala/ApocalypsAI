# Nightly Apocalypse Safehouse S3

## Overview

Terraform module that creates a secure S3 bucket suitable for storing critical post‑apocalyptic data. The bucket has:

- Server‑side encryption (AES‑256)
- Versioning enabled
- Lifecycle rule to delete non‑current versions after 30 days
- IAM policy granting read/write access to a specified IAM role

## Usage

```hcl
module "safehouse_s3" {
  source           = "./utils/nightly-apocalypse-safehouse-s3"
  bucket_name      = "my‑post‑apoc‑store"
  allowed_role_arn = "arn:aws:iam::123456789012:role/ApocalypseReader"
}
```

## Variables

- `bucket_name` (string, required): Name of the S3 bucket.
- `allowed_role_arn` (string, required): ARN of the IAM role that will receive read/write permissions.
- `tags` (map(string), optional): Tags to apply to all resources.

## Outputs

- `bucket_id` – ID of the created bucket.
- `bucket_arn` – ARN of the bucket.
- `policy_arn` – ARN of the IAM policy attached to the role.

## Testing

Run the test script:

```bash
cd utils/nightly-apocalypse-safehouse-s3
chmod +x tests/test_module.sh
./tests/test_module.sh
```

The script runs `terraform init` (local backend) and `terraform validate`. It should exit with status 0.
