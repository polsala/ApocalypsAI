# Nightly Safehouse S3 Module

## Overview
A playful Terraform module that creates an AWS S3 bucket representing a post‑apocalyptic safe‑house. The bucket has:
- Versioning enabled (so you never lose a precious stash)
- A lifecycle rule that deletes objects older than 30 days (to keep the bunker tidy)
- A randomly generated, whimsical name if you don’t provide one.

## Usage
```hcl
module "safehouse" {
  source = "./nightly-safehouse-s3-module"

  # Optional: provide your own bucket name. Must be globally unique.
  # bucket_name = "my‑custom‑safehouse"

  region = "us-east-1"
}
```

## Inputs
| Name | Description | Type | Default |
|------|-------------|------|---------|
| `bucket_name` | Desired bucket name. If omitted, a random pet‑style name is generated. | `string` | `null` |
| `region` | AWS region for the bucket. | `string` | `us-east-1` |

## Outputs
| Name | Description |
|------|-------------|
| `bucket_id` | The bucket name (ID). |
| `bucket_arn` | The bucket ARN. |

## Testing
Run the provided test script:
```bash
cd nightly-safehouse-s3-module/tests
bash test_module.sh
```
The script runs `terraform init` and `terraform validate` locally (no AWS credentials required).

---
*Built by the ApocalypsAI Nightly Integrator – because even in the wasteland you need a safe place for your data.*
