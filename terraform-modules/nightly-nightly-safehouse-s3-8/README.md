# Safehouse S3 Terraform Module

Creates an S3 bucket suitable for storing precious post‑apocalyptic supplies.

Features:
- Randomized bucket name using `random_pet` to avoid naming collisions.
- Versioning enabled.
- Server‑side encryption (AES‑256).
- Lifecycle rule that expires objects after configurable days.

## Usage

```hcl
module "safehouse_s3" {
  source          = "./utils/nightly-safehouse-s3"
  region          = "us-west-2"
  bucket_prefix   = "my‑safehouse"
  expiration_days = 45
}
```

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| region | AWS region | string | "us-east-1" |
| bucket_prefix | Prefix for bucket name | string | "safehouse" |
| expiration_days | Days after which objects expire | number | 30 |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | The ID of the created bucket |
| bucket_arn | ARN of the bucket |
| bucket_name | Name of the bucket |

## Testing

Run the provided test script:

```sh
cd utils/nightly-safehouse-s3
bash tests/test_module.sh
```
