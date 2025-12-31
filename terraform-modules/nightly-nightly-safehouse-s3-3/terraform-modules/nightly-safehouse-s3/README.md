# nightly‑safehouse‑s3

A whimsical yet practical Terraform module that creates a **secure S3 bucket** to store your post‑apocalyptic supplies.

## Features

- Server‑side encryption (AES‑256)
- Versioning enabled (never lose a supply list)
- Lifecycle rule that deletes objects older than 30 days (keep the cache fresh)
- Optional initial "supply‑cache.txt" object with placeholder content

## Usage

```hcl
module "safehouse" {
  source = "./terraform-modules/nightly-safehouse-s3"

  bucket_name        = "my‑apocalypse‑supplies"
  create_supply_file = true
}
```

## Variables

| Name | Type | Description | Default |
|------|------|-------------|---------|
| `bucket_name` | `string` | Name of the S3 bucket (must be globally unique) | n/a |
| `create_supply_file` | `bool` | Whether to create an initial `supply‑cache.txt` object | `false` |
| `tags` | `map(string)` | Tags to apply to the bucket | `{}` |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_id` | The ID of the created bucket |
| `bucket_arn` | The ARN of the created bucket |
| `supply_file_url` | URL of the optional supply‑cache file (empty if not created) |

## Testing

Run the provided test script:

```bash
cd terraform-modules/nightly-safehouse-s3
bash tests/test_module.sh
```

The script will initialise Terraform, validate the configuration, and ensure the plan contains the expected resources.
