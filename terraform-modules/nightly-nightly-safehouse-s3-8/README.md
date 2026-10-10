# Nightly Safehouse S3

A whimsical Terraform module that creates a secure S3 bucket for storing safe‑house data.

## Features

- Randomized bucket name using `random_pet`
- Server‑side encryption (AES‑256)
- Versioning enabled
- Lifecycle rule to delete non‑current versions after 30 days
- Optional tags for organization

## Usage

```hcl
module "safehouse" {
  source = "./nightly-safehouse-s3"

  # Optional custom tags
  tags = {
    Environment = "post‑apocalypse"
    Owner       = "survivors"
  }
}
```

The module will create a bucket named something like `safehouse‑fluffy‑rabbit`.

## Inputs

| Name | Description | Type | Default |
|------|-------------|------|---------|
| tags | A map of tags to assign to the bucket | map(string) | `{}` |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id   | The ID of the created bucket |
| bucket_arn  | The ARN of the created bucket |
| bucket_name | The name of the created bucket |

## Testing

Run the provided test script to ensure the configuration validates:

```bash
cd nightly-safehouse-s3
./tests/validate.sh
```
