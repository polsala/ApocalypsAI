# Post‑Apocalyptic S3 Safehouse Terraform Module

## Overview
Creates an Amazon S3 bucket hardened for storing critical data after the world ends. The bucket has:

- Server‑side encryption (AES‑256)
- Versioning enabled
- Lifecycle rule that expires objects after a configurable number of days
- Optional tags

## Usage

```hcl
module "safehouse" {
  source          = "github.com/yourorg/ApocalypsAI//terraform-modules/nightly-postapoc-s3-safehouse"
  bucket_name     = "my-postapoc-vault"
  expiration_days = 30
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| bucket_name | Name of the S3 bucket (must be globally unique) | string | n/a | yes |
| expiration_days | Days after which objects are deleted | number | 30 | no |
| tags | Map of tags to apply | map(string) | {} | no |
| region | AWS region | string | "us-east-1" | no |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | The bucket name |
| bucket_arn | The bucket ARN |

## Testing

Run the provided test script:

```sh
cd tests
./test_module.sh
```
