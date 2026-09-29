# Nightly Safehouse S3 Bucket

A whimsical Terraform module that creates an S3 bucket configured as a secure safe‑house for your apocalypse‑ready data. Features versioning, server‑side encryption, and a lifecycle rule that moves old objects to Glacier after 30 days.

## Usage

```hcl
module "safehouse_bucket" {
  source      = "./"
  bucket_name = "my-safehouse-data"
}
```

## Inputs

- `bucket_name` (string, required): Name of the bucket.

## Outputs

- `bucket_id` – The ID of the created bucket.

## Testing

Run `bash tests/test_module.sh` to verify the module contains required resources.
