# nightly-s3-bucket-creator

Creates an AWS S3 bucket with versioning and server‑side encryption (AES‑256).

## Usage

Add this module to your Terraform configuration:

```hcl
module "s3_bucket" {
  source      = "./nightly-s3-bucket-creator"
  bucket_name = "my‑awesome‑bucket"
}

output "bucket_arn" {
  value = module.s3_bucket.bucket_arn
}
```

## Variables

| Name | Type | Description |
|------|------|-------------|
| `bucket_name` | `string` | Name of the S3 bucket to create. Must be globally unique. |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_arn` | ARN of the created bucket. |

## Requirements

* Terraform ≥ 1.0.0
* AWS provider (no credentials needed for `terraform validate`)

## Testing

Run the provided test script:

```bash
cd nightly-s3-bucket-creator
bash tests/test_main.sh
```

The script runs `terraform init` (backend disabled) and `terraform validate` to ensure the module syntax is correct.
