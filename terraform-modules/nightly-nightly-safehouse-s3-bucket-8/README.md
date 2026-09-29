# Nightly Safehouse S3 Bucket

Creates an S3 bucket configured for post‑apocalyptic data storage: versioning enabled, server‑side encryption with AES‑256, and a lifecycle rule that expires objects after 30 days. Ideal for storing backups of survival checklists, resource trackers, etc.

## Usage

```hcl
module "safehouse_bucket" {
  source      = "./"
  bucket_name = "my-safehouse-bucket"
}
```

## Inputs

- `bucket_name` (string, required): Name of the S3 bucket.

## Outputs

- `bucket_id`: The ID of the created bucket.

## Testing

Run `tests/test_main.sh` to validate the module.
