# Apocalyptic Safehouse S3

A whimsical Terraform module that creates a secure S3 bucket for storing precious supplies in the wasteland. Features:

- Randomly generated bucket name using `random_pet`.
- Server‑side encryption (AES256).
- Versioning enabled.
- Lifecycle rule to delete non‑current versions after 30 days.

## Usage

```hcl
module "safehouse" {
  source        = "git::https://github.com/yourorg/apocalypsai.git//terraform-modules/nightly-apocalypse-safehouse-s3"
  bucket_prefix = "wasteland"
}
```

## Inputs

| Name | Description | Type | Default |
|------|-------------|------|---------|
| bucket_prefix | Prefix for bucket name | string | `"apocalypse"` |
| aws_region    | AWS region for resources | string | `"us-east-1"` |

## Outputs

| Name | Description |
|------|-------------|
| bucket_name | The name of the created S3 bucket |

## Testing

Run the provided test script:

```sh
cd $(git rev-parse --show-toplevel)/terraform-modules/nightly-apocalypse-safehouse-s3
bash tests/test_module.sh
```
