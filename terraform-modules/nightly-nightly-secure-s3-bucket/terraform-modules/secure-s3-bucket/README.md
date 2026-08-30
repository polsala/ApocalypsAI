# Secure S3 Bucket Module

This Terraform module creates an S3 bucket with:

- Server‑side encryption (AES‑256)
- Versioning enabled
- Lifecycle rule to delete non‑current versions after 30 days
- Randomized bucket name using `random_pet` to avoid naming collisions

## Usage

```hcl
module "secure_bucket" {
  source = "./terraform-modules/secure-s3-bucket"

  bucket_prefix = "apocalypse"
  tags = {
    Environment = "production"
    Owner       = "survivors"
  }
}
```

## Inputs

| Name | Description | Type | Default |
|------|-------------|------|---------|
| bucket_prefix | Prefix for the bucket name | string | `"apocalypse"` |
| tags | Tags to apply to the bucket | map(string) | `{}` |
| aws_region | AWS region for the provider (used in tests) | string | `"us-east-1"` |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | The name of the created bucket |
| bucket_arn | ARN of the bucket |

## Testing

Run `./tests/run.sh` to execute `terraform init` and `terraform validate` in a temporary directory. The test uses dummy AWS credentials and does not make network calls.
