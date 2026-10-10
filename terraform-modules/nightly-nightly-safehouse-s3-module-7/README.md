# Safehouse S3 Module

Creates an Amazon S3 bucket designed for resilient, post‑apocalyptic data storage.

## Features

- **Randomized bucket name** using `random_pet` to avoid naming collisions.
- **Server‑side encryption** (AES‑256) enabled by default.
- **Versioning** turned on so you never lose a previous version.
- **Lifecycle rule** that automatically deletes non‑current object versions after 30 days.
- Optional **tags** for cost allocation or identification.

## Usage Example

```hcl
module "safehouse" {
  source = "github.com/your-org/ApocalypsAI//terraform-modules/nightly-safehouse-s3-module"

  bucket_prefix = "my‑post‑apoc"
  tags = {
    Environment = "production"
    Project     = "safehouse"
  }
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| `bucket_prefix` | Prefix for the generated bucket name. | `string` | `"safehouse"` | no |
| `tags` | Map of tags to assign to the bucket. | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_id` | The ID of the created S3 bucket. |
| `bucket_arn` | The ARN of the created S3 bucket. |

## Testing

A simple validation script is provided under `tests/validate.sh`. It runs `terraform init` and `terraform validate` using a local dummy provider configuration, ensuring the module syntax is correct without contacting AWS.
