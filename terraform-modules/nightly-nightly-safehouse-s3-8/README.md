# Nightly Safehouse S3 Terraform Module

Creates an S3 bucket configured as a post‑apocalyptic safe‑house: versioning, server‑side encryption, public‑access block, and a lifecycle rule that expires objects after 30 days. Also creates a placeholder "supply‑cache.txt" object.

## Usage

```hcl
module "safehouse" {
  source = "./path/to/nightly-safehouse-s3"

  bucket_name = "my-safe-house-bucket"
}
```

## Inputs

- `bucket_name` (string, required): Name of the S3 bucket.
- `aws_region` (string, optional, default: `us-east-1`): AWS region for the bucket.

## Outputs

- `bucket_id` – The ID of the created bucket.
- `supply_cache_url` – URL to the placeholder supply cache object.

## Testing

Run the test script from the module root:

```bash
bash tests/test_module.sh
```

The script validates the configuration with `terraform validate` and ensures a successful plan using mock values.
