# Nightly Safehouse S3 Terraform Module

## Overview
Creates an S3 bucket configured for durability and versioning, suitable for storing critical supplies in a post‑apocalyptic safe‑house. The module can also generate a random password stored in AWS Secrets Manager via a `null_resource`.

## Usage
```hcl
module "safehouse_s3" {
  source       = "./"
  bucket_name  = "my-safehouse-bucket"
  enable_secret = true
}
```

## Inputs
- `bucket_name` (string, required): Name of the S3 bucket.
- `enable_secret` (bool, default = false): Whether to create a secret with a random password.
- `aws_region` (string, default = "us-east-1"): AWS region for the resources.

## Outputs
- `bucket_id` – The ID of the created S3 bucket.
- `secret_arn` – ARN of the Secrets Manager secret (null if not created).

## Testing
Run the test script from the module root:
```bash
./tests/test_safehouse.sh
```
The script uses a local backend and dummy variables, so no real AWS resources are created.
