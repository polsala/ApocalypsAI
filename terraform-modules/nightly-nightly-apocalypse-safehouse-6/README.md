# nightly‑apocalypse‑safehouse‑s3

A tiny Terraform module that creates a **secure S3 bucket** suitable for storing precious post‑apocalyptic data.

## Features

- Server‑side encryption (AES‑256)
- Versioning enabled
- Lifecycle rule that deletes non‑current versions after 30 days
- Randomly generated `RadiationLevel` tag (1‑10) to add a bit of flavor

## Usage

```hcl
module "safehouse" {
  source      = "./nightly-apocalypse-safehouse-s3"
  bucket_name = "my‑post‑apoc‑vault"
}

output "bucket_id" {
  value = module.safehouse.bucket_id
}
```

## Variables

| Name | Type | Description | Default |
|------|------|-------------|---------|
| `bucket_name` | `string` | Name of the S3 bucket (must be globally unique) | n/a |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_id` | The ID of the created bucket |
| `bucket_arn` | The ARN of the created bucket |
| `radiation_level` | Randomly generated radiation level (1‑10) |

## Testing

Run the provided test script:

```bash
cd nightly-apocalypse-safehouse-s3/tests
bash validate.sh
```

The script runs `terraform init -backend=false` and `terraform validate` in a temporary directory.
