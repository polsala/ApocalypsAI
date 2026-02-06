# nightly-safeguard-bucket

Terraform module that creates an S3 bucket configured as a post‑apocalyptic safe‑house storage. The bucket has versioning enabled, server‑side encryption, and a lifecycle rule that transitions objects to Glacier after 30 days and expires after 365 days.

## Usage

```hcl
module "safeguard_bucket" {
  source = "github.com/yourorg/apocalypsai/terraform-modules/nightly-safeguard-bucket"

  bucket_name = "my-safehouse-bucket"
  tags        = {
    Environment = "post-apocalypse"
    Owner       = "survivors"
  }
}
```

## Variables

- `bucket_name` (string, required): Name of the S3 bucket.
- `tags` (map(string), optional): Tags to apply.

## Outputs

- `bucket_id` – The ID of the bucket.
- `bucket_arn` – The ARN of the bucket.

## Testing

Run the provided test script:

```sh
cd $(git rev-parse --show-toplevel)/terraform-modules/nightly-safeguard-bucket
./tests/test_module.sh
```

The script runs `terraform init -backend=false` and `terraform validate`. It will fail if the configuration is invalid.
