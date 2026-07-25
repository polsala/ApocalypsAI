# Nightly Safehouse S3

Utility Terraform module that provisions an S3 bucket with server‑side encryption, versioning, a random name, and a lifecycle rule that deletes objects older than 30 days. Ideal for storing backups or supplies in a post‑apocalyptic setting.

## Usage

```hcl
module "safehouse_s3" {
  source = "./"
}
```

Run `terraform init` and `terraform apply`.

## Features

- Random bucket name using `random_pet`.
- Server‑side encryption (AES‑256).
- Versioning enabled.
- Lifecycle rule to expire objects after 30 days.

## Inputs

| Name | Description | Type | Default |
|------|-------------|------|---------|
| bucket_prefix | Prefix for bucket name | string | "safehouse" |
| aws_region | AWS region to deploy resources | string | "us-east-1" |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | The name of the created bucket |

## Testing

Run `./tests/validate.sh` to ensure the module validates.
