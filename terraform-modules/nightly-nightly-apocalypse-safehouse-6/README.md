# nightly‑apocalypse‑safehouse‑s3

A whimsical yet practical Terraform module that creates an S3 bucket suitable for storing precious supplies in a post‑apocalyptic safe‑house. The bucket has:

* **Versioning** enabled – never lose a crucial recipe or map.
* **Lifecycle rule** that moves old versions to Glacier after 30 days and deletes them after 365 days.
* **Randomly generated password** stored in AWS Secrets Manager (simulated via `random_password` data source) for access control.

## Usage
```hcl
module "safehouse_s3" {
  source       = "./nightly-apocalypse-safehouse-s3"
  bucket_name  = "my‑safehouse‑supplies"
  tags         = {
    Environment = "post‑apocalypse"
    Owner       = "survivors"
  }
}
```

## Inputs
| Name | Description | Type | Default |
|------|-------------|------|---------|
| `bucket_name` | Name of the S3 bucket (must be globally unique) | `string` | n/a |
| `tags` | Map of tags to apply to the bucket | `map(string)` | `{}` |
| `password_length` | Length of the generated password | `number` | `16` |
| `password_special` | Include special characters in password | `bool` | `true` |

## Outputs
| Name | Description |
|------|-------------|
| `bucket_id` | The ID of the created S3 bucket |
| `bucket_arn` | ARN of the bucket |
| `generated_password` | The random password (for demonstration; in real life store in Secrets Manager) |

## Testing
Run the provided test script:
```bash
cd nightly-apocalypse-safehouse-s3
bash tests/test_main.sh
```
The script runs `terraform init` (backend disabled) and `terraform validate` to ensure the module is syntactically correct.
