# Post‑Apocalyptic Safehouse S3 Bucket

This Terraform module creates an S3 bucket configured for durability and secrecy, ideal for storing survival logs, caches, and encrypted data in the wasteland.

## Features

- Server‑side encryption (AES‑256)
- Versioning enabled
- Lifecycle rule to transition non‑current versions to Glacier after 30 days and delete after 365 days
- Optional tags

## Usage

```hcl
module "safehouse_bucket" {
  source      = "github.com/yourorg/apocalypsai//terraform-modules/nightly-postapoc-s3-safehouse"
  bucket_name = "my-safehouse-logs"
  tags = {
    Environment = "post-apocalypse"
    Owner       = "Wasteland Wanderer"
  }
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| bucket_name | Name of the S3 bucket | string | n/a | yes |
| tags | Map of tags to apply | map(string) | {} | no |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | The ID of the bucket |
| bucket_arn | The ARN of the bucket |

## Testing

Run the test script:

```sh
cd tests && ./test_module.sh
```
