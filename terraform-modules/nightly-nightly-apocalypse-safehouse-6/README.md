# Nightly Apocalypse Safehouse S3

## Overview
A whimsical yet practical Terraform module that creates a **secure S3 bucket** suitable for storing critical post‑apocalyptic data. The bucket includes:

- Server‑side encryption (AES‑256)
- Versioning to protect against accidental overwrites
- A lifecycle rule that automatically deletes objects older than 30 days (to keep the vault tidy)

## Usage
```hcl
module "safehouse_s3" {
  source      = "./nightly-apocalypse-safehouse-s3"
  bucket_name = "my‑post‑apoc‑vault"
}
```

## Inputs
| Name | Description | Type | Required |
|------|-------------|------|----------|
| `bucket_name` | Name of the S3 bucket (must be globally unique) | `string` | yes |

## Outputs
| Name | Description |
|------|-------------|
| `bucket_arn` | ARN of the created S3 bucket |

## Testing
Run the provided test script to ensure the module validates correctly:
```bash
cd nightly-apocalypse-safehouse-s3
./tests/validate.sh
```
The script performs `terraform init` (offline) and `terraform validate`.

## License
MIT © ApocalypsAI
