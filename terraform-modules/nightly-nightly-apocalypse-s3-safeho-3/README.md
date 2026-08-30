# Apocalyptic S3 Safehouse Terraform Module

## Overview

Creates an S3 bucket with versioning, server‑side encryption, and a lifecycle rule that expires objects after 365 days. The bucket name is generated randomly with a configurable prefix, perfect for storing critical data in a post‑apocalyptic scenario.

## Usage

```hcl
module "safehouse" {
  source = "git::https://github.com/yourorg/apocalypsai.git//terraform-modules/nightly-apocalypse-s3-safehouse"

  bucket_prefix = "vault"
  tags = {
    Environment = "production"
    Owner       = "apocalypse"
  }
}
```

## Variables

- `bucket_prefix` (string, default `"apocalypse"`): Prefix for the bucket name.
- `tags` (map(string), optional): Tags to apply.
- `aws_region` (string, default `"us-east-1"`): AWS region for the bucket.

## Outputs

- `bucket_name`: The generated bucket name.
- `bucket_arn`: ARN of the bucket.

## Testing

Run the provided test script:

```sh
cd tests && ./test_main.sh
```

The script runs `terraform init -backend=false` and `terraform validate` using the `null` provider, ensuring the module syntax is correct without contacting AWS.
