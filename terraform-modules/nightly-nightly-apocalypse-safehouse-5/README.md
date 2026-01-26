# Apocalyptic Safehouse S3 Terraform Module

## Overview
Creates an S3 bucket configured for durability and security, ideal for storing emergency supplies, manuals, and backups in a post‑apocalyptic setting.

## Features
- Server‑side encryption (AES‑256)
- Versioning enabled
- Lifecycle rule to delete objects older than 30 days
- Optional initial "supply‑cache.txt" object with placeholder text
- Fully configurable bucket name and tags

## Usage
```hcl
module "safehouse_s3" {
  source = "./"
  bucket_name = "my-safehouse-bucket"
  tags = {
    Environment = "post-apocalypse"
    Owner       = "survivors"
  }
}
```

## Inputs
| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| bucket_name | Name of the S3 bucket | string | n/a | yes |
| tags | Tags to apply to the bucket | map(string) | {} | no |
| create_initial_object | Whether to create a placeholder object | bool | true | no |
| initial_object_content | Content of the placeholder object | string | "Emergency supplies inventory" | no |

## Outputs
| Name | Description |
|------|-------------|
| bucket_id | The ID of the created bucket |
| bucket_arn | ARN of the bucket |
| initial_object_key | Key of the placeholder object (if created) |

## Testing
Run `tests/test_module.sh` to validate the module.
