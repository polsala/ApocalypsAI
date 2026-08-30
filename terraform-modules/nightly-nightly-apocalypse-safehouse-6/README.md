# Nightly Apocalypse Safehouse S3

## Overview

This Terraform module creates an S3 bucket that serves as a post‑apocalyptic safe‑house for your data. The bucket is:

- Uniquely named using `random_pet` (e.g., `safehouse-fluffy-wolf`)
- Encrypted with SSE‑S3
- Versioning enabled
- Lifecycle rule that expires objects after 30 days

## Usage

```hcl
module "safehouse" {
  source        = "./utils/nightly-apocalypse-safehouse-s3"
  bucket_prefix = "my-vault"
}
```

## Inputs

| Name          | Description                     | Type   | Default   |
|---------------|---------------------------------|--------|-----------|
| bucket_prefix | Prefix for the bucket name      | string | "safehouse" |
| aws_region    | AWS region for the bucket       | string | "us-east-1" |

## Outputs

| Name      | Description                     |
|-----------|---------------------------------|
| bucket_id | The name of the created bucket |

## Testing

Run the validation script:

```sh
cd utils/nightly-apocalypse-safehouse-s3
./tests/validate.sh
```
