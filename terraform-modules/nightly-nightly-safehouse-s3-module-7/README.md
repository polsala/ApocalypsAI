# Nightly Safehouse S3 Module

Creates an S3 bucket configured for post‑apocalyptic safe‑house storage.

## Features
- **Versioning** enabled
- **Server‑side encryption** (AES256)
- **Lifecycle rule**: automatically delete objects older than 30 days
- **Read‑only IAM policy** for external services or users

## Usage
```hcl
module "safehouse" {
  source      = "./utils/nightly-safehouse-s3-module"
  bucket_name = "my‑safehouse‑bucket"
  tags = {
    Environment = "production"
    Project     = "safehouse"
  }
}
```

## Variables
| Name | Description | Type | Default |
|------|-------------|------|---------|
| `bucket_name` | Name of the S3 bucket | `string` | n/a |
| `tags` | Tags to apply to the bucket | `map(string)` | `{}` |

## Outputs
| Name | Description |
|------|-------------|
| `bucket_id` | ID of the created bucket |
| `bucket_arn` | ARN of the created bucket |
| `read_only_policy_arn` | ARN of the generated read‑only IAM policy |

## Testing
Run the provided test script:
```bash
cd utils/nightly-safehouse-s3-module
bash tests/test_main.sh
```
The script validates the Terraform configuration and checks that the expected resources are present in a plan.
