# Nightly Apocalypse Safehouse S3

A whimsical yet practical Terraform module that creates an S3 bucket configured as a "safe‑house" for your post‑apocalyptic data stash. The bucket has versioning enabled, a lifecycle rule that expires old objects, and a randomly generated password stored in the bucket tags.

## Features

- **Versioning** – never lose a previous version of a critical file.
- **Lifecycle expiration** – automatically delete objects older than a configurable number of days.
- **Random password** – a cryptographically‑secure password (default 16 characters) is generated at apply time and attached as a tag to the bucket.
- **Zero‑runtime credentials** – the module validates locally; no real AWS credentials are required for `terraform validate`.

## Usage

```hcl
module "safehouse" {
  source          = "./nightly-apocalypse-safehouse-s3"
  region          = "us-east-1"
  bucket_name     = "my‑post‑apoc‑stash"
  password_length = 20
  expiration_days = 365
}
```

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| `region` | AWS region for the bucket | `string` | n/a |
| `bucket_name` | Desired bucket name (must be globally unique) | `string` | n/a |
| `password_length` | Length of the generated password | `number` | `16` |
| `expiration_days` | Days after which objects are expired | `number` | `365` |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_arn` | ARN of the created bucket |
| `generated_password` | The random password stored as a tag |

## Testing

A simple validation script is provided under `tests/validate.sh`. Run it with:

```bash
cd nightly-apocalypse-safehouse-s3
bash tests/validate.sh
```

The script runs `terraform init -backend=false` and `terraform validate`. It should exit with status `0`.
