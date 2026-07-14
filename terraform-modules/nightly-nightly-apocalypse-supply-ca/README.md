# Nightly Apocalypse Supply Cache Terraform Module

Creates an S3 bucket to store emergency supplies with versioning, server‑side encryption, and a lifecycle rule that expires objects after 30 days. Adds a whimsical tag `apocalypse:ready` with a random emoji.

## Usage

```hcl
module "supply_cache" {
  source      = "github.com/yourorg/polsala/ApocalypsAI//terraform-modules/nightly-apocalypse-supply-cache"
  bucket_name = "my-supply-cache"
}
```

## Inputs

- `bucket_name` (string, required): Name of the S3 bucket.

## Outputs

- `bucket_id` – The ID of the created bucket.
- `bucket_arn` – The ARN of the bucket.

## Notes

- Requires the AWS provider.
- The module is deliberately whimsical but fully functional.
