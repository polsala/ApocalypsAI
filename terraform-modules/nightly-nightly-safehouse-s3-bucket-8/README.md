# nightly‑safehouse‑s3‑bucket

## Overview

This Terraform module creates a **secure, version‑enabled S3 bucket** that can serve as a digital safe‑house for your most valuable (or cursed) artifacts.  It includes:

* Bucket versioning – never lose a previous revision of a file.
* Lifecycle rule – automatically delete objects older than 365 days to keep the vault tidy.
* Optional server‑side encryption.

The module is deliberately whimsical – think of it as a bunker for your data in a world gone mad.

## Usage

```hcl
module "safehouse" {
  source      = "./utils/nightly-safehouse-s3-bucket"
  bucket_name = "my‑post‑apoc‑vault"
  enable_encryption = true
}
```

## Variables

| Name | Type | Description | Default |
|------|------|-------------|---------|
| `bucket_name` | `string` | Name of the S3 bucket (must be globally unique). | n/a |
| `enable_encryption` | `bool` | Whether to enable AES‑256 server‑side encryption. | `false` |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_id` | The ID of the created bucket. |
| `bucket_arn` | The ARN of the created bucket. |

## Testing

A simple Bash test is provided under `tests/`. Run it with:

```bash
cd utils/nightly-safehouse-s3-bucket
bash tests/test_main.sh
```

The test runs `terraform init` (backend disabled) and `terraform validate` to ensure the configuration is syntactically correct.
