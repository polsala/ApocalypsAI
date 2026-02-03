# nightly‑safehouse‑s3‑module

## Overview

This Terraform module creates an Amazon S3 bucket that acts as a **post‑apocalyptic safe‑house storage vault**. It enables:

* Versioning – never lose a crucial file, even if the world ends.
* Server‑side encryption with a randomly generated password (via the `random_password` resource).
* Lifecycle rule that automatically deletes objects older than a configurable number of days, keeping the vault tidy.

The module is deliberately whimsical but fully functional – you can drop it into any Terraform project that targets AWS.

## Usage

```hcl
module "safehouse" {
  source               = "./utils/nightly-safehouse-s3-module"
  bucket_name          = "my‑post‑apoc‑vault"
  retention_days       = 365
  password_length      = 32
  password_special     = true
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| `bucket_name` | Name of the S3 bucket (must be globally unique) | `string` | n/a | yes |
| `retention_days` | Number of days to retain objects before deletion | `number` | `365` | no |
| `password_length` | Length of the generated password | `number` | `32` | no |
| `password_special` | Include special characters in the password | `bool` | `true` | no |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_arn` | ARN of the created bucket |
| `generated_password` | The random password used for server‑side encryption |

## Testing

Run the provided test script:

```bash
cd utils/nightly-safehouse-s3-module
bash tests/validate.sh
```

The script runs `terraform init` (with a local backend) and `terraform validate`. It should exit with status `0`.

## License

MIT – because even in the wasteland, we love open source.
