# nightly-safehouse-s3-module

Creates an S3 bucket configured as a post‑apocalyptic safe‑house:

* **Versioning** enabled
* **Server‑side encryption** (AES‑256)
* **Lifecycle rule** that expires objects after a configurable number of days
* Generates a **random vault password** using the `random_password` resource

## Usage

```hcl
module "safehouse" {
  source          = "github.com/your-org/ApocalypsAI//terraform-modules/nightly-safehouse-s3-module"
  bucket_name     = "my‑post‑apoc‑vault"
  expiration_days = 180          # optional, defaults to 365
  password_length = 24           # optional, defaults to 32
}

output "bucket_arn" {
  value = module.safehouse.bucket_arn
}

output "vault_password" {
  value = module.safehouse.vault_password
}
```

## Variables

| Name | Type | Description | Default |
|------|------|-------------|---------|
| `aws_region` | `string` | AWS region for the bucket | `"us-east-1"` |
| `bucket_name` | `string` | Name of the S3 bucket (must be globally unique) | n/a |
| `expiration_days` | `number` | Days after which objects expire | `365` |
| `password_length` | `number` | Length of the generated vault password | `32` |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_arn` | ARN of the created S3 bucket |
| `vault_password` | Randomly generated password for your vault |

## Testing

The module includes a simple test script that runs `terraform init` and `terraform validate` in an isolated temporary directory. See `tests/test_main.sh` for details.
