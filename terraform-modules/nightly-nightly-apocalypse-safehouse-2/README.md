# Nightly Apocalypse Safehouse S3

Terraform module that creates an S3 bucket configured for versioning, server‑side encryption, and a lifecycle rule that deletes non‑current versions after 30 days. It also generates a random access token stored in AWS Secrets Manager (optional). Ideal for storing community backups in a post‑apocalyptic scenario.

## Usage

```hcl
module "safehouse_s3" {
  source = "github.com/yourorg/apocalypsai//terraform-modules/nightly-apocalypse-safehouse-s3"

  bucket_name   = "my-safehouse-data"
  enable_secret = true
}
```

## Variables

- `bucket_name` (string, required): Name of the S3 bucket.
- `enable_secret` (bool, default `false`): Whether to create a random secret in Secrets Manager.
- `tags` (map(string), optional): Tags to apply.

## Outputs

- `bucket_id`: ID of the created bucket.
- `secret_arn`: ARN of the secret (if created).

## Testing

Run `tests/validate.sh` to ensure the module validates and plans successfully.
