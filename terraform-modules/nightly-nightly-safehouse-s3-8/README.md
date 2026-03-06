# Nightly Safehouse S3 Terraform Module

Creates an S3 bucket for storing post‑apocalyptic supplies with:

* **Versioning** enabled
* **Server‑side encryption** (AES‑256)
* **Lifecycle rule** that expires objects after a configurable number of days (default 30)
* **IAM policy** granting a specified IAM role read/write access to the bucket

## Usage
```hcl
module "safehouse_s3" {
  source            = "./nightly-safehouse-s3"
  bucket_name       = "my‑post‑apoc‑supplies"
  allowed_role_arn  = "arn:aws:iam::123456789012:role/SurvivorRole"
  expiration_days   = 30
}
```

## Variables
| Name | Type | Description | Default |
|------|------|-------------|---------|
| `bucket_name` | `string` | Name of the S3 bucket (must be globally unique) | n/a |
| `allowed_role_arn` | `string` | ARN of the IAM role that will receive read/write permissions | n/a |
| `expiration_days` | `number` | Number of days after which objects are deleted | `30` |

## Outputs
| Name | Description |
|------|-------------|
| `bucket_arn` | ARN of the created S3 bucket |
| `policy_arn` | ARN of the IAM policy granting access |

## Testing
Run the bundled unit tests with:
```bash
python -m unittest discover -s tests
```
The tests verify that the Terraform configuration contains the expected resources and attributes.

## License
MIT © ApocalypsAI
