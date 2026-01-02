# Safehouse S3 Terraform Module

## Overview

Creates an AWS S3 bucket with versioning enabled, a lifecycle rule that transitions objects to Glacier after 30 days and expires after 365 days, and generates a random password stored in a local file (simulating a secret for safe‑house access).

## Usage

```hcl
module "safehouse_s3" {
  source = "git::https://github.com/yourorg/apocalypsai.git//terraform-modules/nightly-safehouse-s3"

  bucket_name = "my-safehouse-bucket"
}
```

## Inputs

- `bucket_name` (string, required): Name of the S3 bucket.
- `tags` (map(string), optional): Tags to apply.
- `aws_region` (string, optional): AWS region (default: `us-east-1`).

## Outputs

- `bucket_id` – The ID of the created bucket.
- `password_file` – Path to the generated password file.

## Testing

```sh
cd terraform-modules/nightly-safehouse-s3
./tests/test_main.sh
```
