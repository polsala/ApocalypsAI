# Nightly Apocalypse Safehouse S3

## Overview

A whimsical yet practical Terraform module that creates a **secure S3 bucket** suitable for storing precious post‑apocalyptic data. Features include:

- Optional custom bucket name or automatically generated whimsical name using `random_pet`
- Server‑side encryption (AES‑256)
- Versioning enabled to protect against accidental overwrites
- Lifecycle rule that expires objects older than 30 days (so you don’t hoard the dead weight)

## Usage

```hcl
module "safehouse" {
  source = "./nightly-apocalypse-safehouse-s3"

  # Optional: provide your own bucket name. If omitted, a random name is generated.
  # bucket_name = "my‑post‑apoc‑vault"

  tags = {
    Environment = "production"
    Project     = "Apocalypse"
  }
}

output "bucket_name" {
  value = module.safehouse.bucket_name
}
```

## Inputs

| Name | Description | Type | Default |
|------|-------------|------|---------|
| `bucket_name` | Custom bucket name. If empty, a random name is generated. | `string` | `""` |
| `tags` | A map of tags to assign to the bucket. | `map(string)` | `{}` |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_id` | The ID of the created bucket |
| `bucket_arn` | The ARN of the created bucket |
| `bucket_name` | The final bucket name (custom or generated) |

## Testing

Run the provided test script:

```bash
cd nightly-apocalypse-safehouse-s3
bash tests/test_module.sh
```

The script will initialize Terraform, validate the configuration, and ensure the plan contains the expected `aws_s3_bucket.safehouse` resource.
