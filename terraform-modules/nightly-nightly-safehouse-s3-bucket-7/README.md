# Nightly Safehouse S3 Bucket

Utility creates an S3 bucket configured for post‑apocalyptic safe‑house storage: versioning, server‑side encryption, and a lifecycle rule that expires objects after 30 days. Works with any AWS provider configuration.

## Usage

```hcl
module "safehouse_bucket" {
  source = "git::https://github.com/yourorg/ApocalypsAI.git//terraform-modules/nightly-safehouse-s3-bucket?ref=main"

  bucket_name = "my-safehouse-bucket"
  tags        = {
    Environment = "production"
    Project     = "safehouse"
  }
}
```

## Inputs

- `bucket_name` (string, required): Name of the bucket.
- `tags` (map(string), optional): Tags to apply.

## Outputs

- `bucket_id` – The ID of the bucket.
- `bucket_arn` – The ARN.

## Testing

Run `./tests/test_main.sh` to validate the module.
