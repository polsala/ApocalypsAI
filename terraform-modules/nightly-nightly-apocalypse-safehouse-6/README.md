# Apocalyptic Safehouse S3 Terraform Module

This module creates an S3 bucket configured for versioning, server-side encryption, and a lifecycle rule that deletes noncurrent versions after 30 days. It also generates a random password using the random provider, useful for storing in Secrets Manager.

## Usage

```hcl
module "safehouse" {
  source = "github.com/yourorg/apocalypsai//terraform-modules/nightly-apocalypse-safehouse-s3"

  bucket_name = "my-safehouse-bucket"
  tags        = {
    Environment = "production"
    Project     = "apocalypse"
  }
}
```

## Inputs

- `bucket_name` (string, required): Name of the S3 bucket.
- `tags` (map(string), optional): Tags to apply.

## Outputs

- `bucket_id`
- `bucket_arn`
- `generated_password`

## Testing

Run `tests/validate.sh` to ensure the module validates.
