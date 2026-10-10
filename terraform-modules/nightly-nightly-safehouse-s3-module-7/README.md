# Nightly Safehouse S3 Module

## Overview

This Terraform module creates an Amazon S3 bucket that acts as a **post‑apocalyptic safe‑house** for your critical data. The bucket is:

- **Versioned** – every change is retained.
- **Encrypted** with AES‑256 server‑side encryption.
- **Self‑cleaning** – objects older than 30 days are automatically deleted via a lifecycle rule.

The module is deliberately simple and fully self‑contained, making it perfect for demos, learning, or as a quirky addition to any infrastructure.

## Usage

```hcl
module "safehouse" {
  source = "./utils/nightly-safehouse-s3-module"

  bucket_name = "my‑post‑apoc‑safehouse"
  tags = {
    Environment = "production"
    Owner       = "apocalypse‑team"
  }
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| `bucket_name` | Name of the S3 bucket (must be globally unique) | `string` | n/a | yes |
| `tags` | A map of tags to assign to the bucket | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_id` | The ID of the created S3 bucket |
| `bucket_arn` | The ARN of the created S3 bucket |

## Testing

The module includes a deterministic offline test suite located in `tests/`. Run it with:

```bash
cd utils/nightly-safehouse-s3-module
bash tests/validate.sh
```

The script runs `terraform init` (with a local backend) and `terraform validate` to ensure the configuration is syntactically correct.

## License

MIT – because even in the wasteland we respect open source.
