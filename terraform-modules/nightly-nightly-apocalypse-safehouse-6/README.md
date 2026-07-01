# Apocalyptic Safehouse S3 Terraform Module

Creates an S3 bucket with versioning, server‑side encryption, a lifecycle rule to delete old versions after 30 days, and an optional random suffix to avoid name collisions. Ideal for storing post‑apocalypse data backups.

## Usage

```hcl
module "safehouse" {
  source = "git::https://github.com/yourorg/apocalypsai.git//terraform-modules/nightly-apocalypse-safehouse-s3"

  bucket_name = "apocalypse-data"
}
```

## Inputs

| Name | Type | Description | Default |
|------|------|-------------|---------|
| `bucket_name` | string | Base name for the bucket. | n/a |
| `enable_random_suffix` | bool | Append a random suffix to avoid collisions. | `true` |
| `aws_region` | string | AWS region for the bucket. | `"us-east-1"` |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_id` | The ID of the created bucket. |
| `bucket_arn` | The ARN of the created bucket. |
| `bucket_name` | The final bucket name (with suffix if enabled). |

Run `terraform init && terraform apply` to create the safehouse.
