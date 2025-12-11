# nightly-terraform-aws-s3

A minimal Terraform module that provisions an AWS S3 bucket with versioning and lifecycle rules.

## Usage

```hcl
module "s3" {
  source = "../terraform-modules/nightly-terraform-aws-s3"

  bucket_name = "my-bucket"
}
```

## Variables

- `bucket_name` (string, required): The name of the bucket.

## Outputs

- `bucket_arn` (string): The ARN of the created bucket.

## Features

- Versioning enabled.
- Lifecycle rule that transitions objects to Glacier after 30 days and permanently deletes them after 365 days.

## Requirements

- Terraform >= 0.13
- AWS provider
