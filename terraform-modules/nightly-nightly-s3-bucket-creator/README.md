# nightly-s3-bucket-creator

Creates an AWS S3 bucket with versioning and server‑side encryption. Simple Terraform module.

## Usage

```hcl
module "my_bucket" {
  source      = "github.com/yourorg/polsala/ApocalypsAI//terraform-modules/nightly-s3-bucket-creator"
  bucket_name = "my-unique-bucket"
}
```

## Variables

- `bucket_name` (string) – Name of the bucket (must be globally unique).
- `aws_region` (string) – AWS region (default: `us-east-1`).

## Outputs

- `bucket_arn` – ARN of the created bucket.

## Testing

Run the test script from the module root:

```bash
bash tests/test_main.sh
```

The script validates the configuration and runs a dry‑run plan without requiring real AWS credentials.
