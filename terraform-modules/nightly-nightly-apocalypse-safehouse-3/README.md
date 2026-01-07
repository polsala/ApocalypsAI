# Nightly Apocalypse Safehouse S3 Module

## Overview

This Terraform module provisions an AWS S3 bucket designed for a post‑apocalyptic safe‑house:

* **Versioning** – keep every change forever.
* **Server‑side encryption** – AES‑256 encryption at rest.
* **Lifecycle rule** – automatically transition objects to Glacier after a configurable number of days.
* **Random access token** – a generated password that can be used as a secret for API access or client‑side encryption.

The module is deliberately whimsical but fully functional and can be dropped into any Terraform configuration.

## Usage Example

```hcl
module "safehouse_s3" {
  source          = "./utils/nightly-apocalypse-safehouse-s3"
  bucket_name     = "my‑post‑apoc‑vault"
  tags = {
    Environment = "production"
    Project     = "safehouse"
  }
  lifecycle_days  = 30
  password_length = 24
}

output "bucket_arn" {
  value = module.safehouse_s3.bucket_arn
}

output "access_token" {
  value = module.safehouse_s3.access_token
  sensitive = true
}
```

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| `bucket_name` | Name of the S3 bucket (must be globally unique) | `string` | n/a |
| `tags` | Map of tags to assign to the bucket | `map(string)` | `{}` |
| `lifecycle_days` | Days after which objects transition to Glacier | `number` | `30` |
| `password_length` | Length of the generated random password | `number` | `16` |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_id` | The ID of the created bucket |
| `bucket_arn` | The ARN of the created bucket |
| `access_token` | Randomly generated password (sensitive) |

## Testing

Run the provided test script:

```bash
cd utils/nightly-apocalypse-safehouse-s3
bash tests/test_module.sh
```

The script runs `terraform init` (with a local backend) and `terraform validate` to ensure the module is syntactically correct.
