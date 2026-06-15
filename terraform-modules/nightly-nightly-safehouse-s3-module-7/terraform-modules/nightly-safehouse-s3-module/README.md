# Nightly Safehouse S3 Module

Creates an S3 bucket configured as a post‑apocalyptic safe‑house for supplies.

## Features

- Versioning enabled
- Server‑side encryption (AES‑256)
- Lifecycle rule to delete objects older than 30 days
- Random `supply_cache_id` tag for uniqueness

## Usage

```hcl
module "safehouse" {
  source      = "./terraform-modules/nightly-safehouse-s3-module"
  bucket_name = "my-safehouse-bucket"
}
```

## Variables

| Name | Description | Type |
|------|-------------|------|
| `bucket_name` | Name of the S3 bucket | `string` |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_id` | ID of the created bucket |
| `bucket_arn` | ARN of the created bucket |

## Testing

Run the test script:

```bash
cd terraform-modules/nightly-safehouse-s3-module/tests
bash test_module.sh
```
