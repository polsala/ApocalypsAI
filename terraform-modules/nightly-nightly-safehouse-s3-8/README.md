# Nightly Safehouse S3 Terraform Module

## Overview
Creates an S3 bucket configured for apocalypse‑ready storage: versioning enabled, server‑side encryption, lifecycle rule to transition old objects to Glacier, and a randomly generated access password stored in SSM Parameter Store.

## Usage
```hcl
module "safehouse_s3" {
  source = "./utils/terraform-modules/nightly-safehouse-s3"

  bucket_name        = "my-apocalypse-store"
  ssm_parameter_name = "/apocalypse/safehouse/password"
}
```

## Inputs
- `bucket_name` (string, required): Name of the bucket.
- `ssm_parameter_name` (string, required): Name of the SSM Parameter to store the password.

## Outputs
- `bucket_arn`
- `password_parameter_arn`

## Testing
Run `bash tests/test_module.sh` from the module directory.
