# Apocalypse Safehouse S3 Terraform Module

This module creates an Amazon S3 bucket configured as a post‑apocalyptic safehouse.

## Features

- **Versioning** – keep every change to your supplies.
- **Server‑side encryption (AES‑256)** – protect contents at rest.
- **Lifecycle rule** – automatically delete objects older than 30 days.
- **Optional initial supply file** – drop a starter "supply cache" object into the bucket.

## Usage Example

```hcl
module "safehouse" {
  source          = "./nightly-apocalypse-safehouse-s3"
  bucket_name     = "my‑post‑apoc‑safehouse"
  region          = "us-east-1"
  create_supply   = true
  supply_content  = "Emergency rations: water, canned beans, solar charger"
}

output "bucket_id" {
  value = module.safehouse.bucket_id
}
```

## Variables

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| `bucket_name` | Name of the S3 bucket (must be globally unique) | `string` | n/a | yes |
| `region` | AWS region for the bucket | `string` | `us-east-1` | no |
| `create_supply` | Whether to create an initial supply object | `bool` | `false` | no |
| `supply_content` | Content of the initial supply object (plain text) | `string` | `""` | no |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_id` | The name (ID) of the created bucket |
| `bucket_arn` | ARN of the bucket |
| `supply_object_key` | Key of the optional supply object (empty string if not created) |

## Testing

A simple test script is provided under `tests/test.sh`. It runs `terraform init`, `terraform validate`, and checks that the plan contains the expected resources. The test runs entirely offline (no AWS credentials required).
