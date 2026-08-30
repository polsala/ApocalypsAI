# Nightly Apocalypse Safehouse S3

## Overview

A tiny Terraform module that creates an Amazon S3 bucket suitable for storing post‑apocalyptic resources. The bucket includes:

* **Versioning** – never lose a previous version of a file.
* **Server‑side encryption** – AES‑256 encryption at rest.
* **Lifecycle rule** – automatically expire objects older than 30 days.
* **Read‑only IAM policy** – a policy ARN you can attach to users or roles that only need to read the bucket.

## Usage

```hcl
module "safehouse" {
  source      = "./nightly-apocalypse-safehouse-s3"
  bucket_name = "my‑post‑apoc‑stash"
  tags = {
    Environment = "production"
    Project     = "apocalypse"
  }
}

output "bucket_arn" {
  value = module.safehouse.bucket_arn
}

output "read_only_policy_arn" {
  value = module.safehouse.read_only_policy_arn
}
```

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| `bucket_name` | Name of the S3 bucket (must be globally unique) | `string` | n/a |
| `tags` | Optional tags to apply to the bucket | `map(string)` | `{}` |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_arn` | ARN of the created bucket |
| `read_only_policy_arn` | ARN of the generated read‑only IAM policy |

## Testing

A simple shell script is provided under `tests/validate.sh` that checks the presence of the required resources without contacting AWS. Run it with:

```bash
cd nightly-apocalypse-safehouse-s3
tests/validate.sh
```

If all checks pass you will see `All checks passed.`.
