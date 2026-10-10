# Nightly Safehouse S3 Terraform Module

Provision a durable, version‑enabled S3 bucket with lifecycle rules, perfect for storing critical post‑apocalyptic data.

## Usage

```hcl
module "safehouse" {
  source      = "github.com/yourorg/polsala/terraform-modules/nightly-safehouse-s3"
  bucket_name = "my-safehouse-bucket"
}
```

## Features

- Optional random bucket name generation
- Versioning enabled
- Lifecycle rule to expire non‑current versions after 365 days
- Tags for identification

## Inputs

| Name | Description | Type | Default |
|------|-------------|------|---------|
| bucket_name | Name of the S3 bucket (if omitted a random name is generated) | string | null |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | The ID of the created bucket |
| bucket_arn | The ARN of the created bucket |

## Testing

Run `./tests/test.sh` to validate the module locally.
