# Nightly Safehouse S3 Module

Creates an S3 bucket configured as a post‑apocalyptic safe‑house:

* **Versioning** enabled
* **Server‑side encryption** (AES‑256)
* **Lifecycle rule** that deletes objects older than 30 days
* A placeholder object `supply.txt` with a whimsical message

## Usage
```hcl
module "safehouse" {
  source      = "./nightly-safehouse-s3-module"
  bucket_name = "my‑post‑apoc‑safehouse"
  # region defaults to "us-east-1"
}
```

## Variables
| Name | Description | Type | Default |
|------|-------------|------|---------|
| `bucket_name` | Name of the S3 bucket. | `string` | n/a |
| `region` | AWS region for the bucket. | `string` | `"us-east-1"` |

## Outputs
| Name | Description |
|------|-------------|
| `bucket_id` | The ID of the created bucket. |
| `bucket_arn` | The ARN of the created bucket. |

## Testing
Run the provided test script:
```bash
cd nightly-safehouse-s3-module
bash tests/test.sh
```
The script runs `terraform init` (backend disabled) and `terraform validate` to ensure the module is syntactically correct.
