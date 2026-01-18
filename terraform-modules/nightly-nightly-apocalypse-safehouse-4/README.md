# Apocalyptic Safehouse S3 Terraform Module

## Overview

This Terraform module creates an AWS S3 bucket configured for post‑apocalyptic data storage:

- Server‑side encryption (AES‑256)
- Versioning enabled
- Lifecycle rule that expires objects after 30 days
- Optional custom bucket name; otherwise a random pet name is generated
- Tags for identification

## Usage

```hcl
module "safehouse" {
  source      = "github.com/yourorg/apocalypsai//terraform-modules/nightly-apocalypse-safehouse-s3"
  bucket_name = "my‑post‑apoc‑store"
  tags = {
    Environment = "production"
    Project     = "apocalypse"
  }
}
```

## Inputs

| Name | Description | Type | Default |
|------|-------------|------|---------|
| bucket_name | Custom bucket name (must be globally unique). If omitted, a random name is generated. | string | `null` |
| tags | A map of tags to assign to the bucket. | map(string) | `{}` |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | The name of the created bucket |
| bucket_arn | The ARN of the created bucket |

## Requirements

- Terraform >= 1.0
- AWS provider configured with appropriate credentials

## License

MIT
