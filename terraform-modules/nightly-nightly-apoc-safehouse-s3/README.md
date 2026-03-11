# nightly‑apoc‑safehouse‑s3

## Overview
A whimsical yet practical Terraform module that creates a **secure S3 bucket** for storing precious post‑apocalyptic data. The bucket has:

- Server‑side encryption (AES‑256)
- Versioning enabled (optional)
- A lifecycle rule that deletes non‑current versions after a configurable number of days
- A randomly generated, globally unique name prefixed by a user‑defined string

## Usage
```hcl
module "safehouse" {
  source               = "./nightly-apoc-safehouse-s3"
  bucket_name_prefix   = "apoc‑vault"
  versioning_enabled   = true
  lifecycle_days       = 30
}
```

## Inputs
| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| `bucket_name_prefix` | Prefix for the bucket name (must be lowercase, alphanumeric, and hyphens) | `string` | n/a | yes |
| `versioning_enabled` | Enable S3 versioning | `bool` | `true` | no |
| `lifecycle_days` | Days after which non‑current versions are deleted | `number` | `30` | no |

## Outputs
| Name | Description |
|------|-------------|
| `bucket_id` | The name of the created bucket |
| `bucket_arn` | The ARN of the created bucket |

## Testing
Run the provided test script to ensure the module validates and plans correctly:
```bash
cd nightly-apoc-safehouse-s3
./tests/test_main.sh
```

## License
MIT © ApocalypsAI
