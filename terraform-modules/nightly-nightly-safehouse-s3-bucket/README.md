# nightly‑safehouse‑s3‑bucket

A tiny Terraform module that creates an AWS S3 bucket suitable for storing critical supplies, logs, or backups in a post‑apocalyptic safe‑house.

## Features

- **Versioning** enabled – never lose a previous copy.
- **Lifecycle rule** that expires objects older than 365 days (you can adjust).
- Simple, opinionated defaults; only the bucket name is required.

## Usage

```hcl
module "safehouse" {
  source      = "./utils/nightly-safehouse-s3-bucket"
  bucket_name = "my‑safe‑house‑bucket"
}
```

Run the usual Terraform workflow:

```bash
terraform init -backend=false   # No remote backend needed for the test
terraform apply -var='bucket_name=my-safe-house-bucket' -auto-approve
```

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|----------|
| `bucket_name` | Name of the S3 bucket to create. Must be globally unique. | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_arn` | ARN of the created bucket |

## Testing

A lightweight test script is provided under `tests/`. It simply verifies that the module defines an `aws_s3_bucket` resource. Run it with:

```bash
cd utils/nightly-safehouse-s3-bucket/tests
bash test.sh
```
