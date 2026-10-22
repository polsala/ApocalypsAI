# Apocalyptic Safehouse S3 Module

Creates an S3 bucket configured for post‑apocalyptic data storage with versioning, server‑side encryption, and a lifecycle rule that deletes objects older than 30 days. Also seeds the bucket with a placeholder "supply cache" object.

## Usage

```hcl
module "safehouse" {
  source      = "./"
  bucket_name = "my-safehouse-bucket"
}
```

## Inputs

- `bucket_name` (string, required): Name of the S3 bucket.

## Outputs

- `bucket_arn`: ARN of the created bucket.
- `supply_cache_key`: Key of the placeholder object.

## Testing

Run `./tests/validate.sh` from the module directory.
