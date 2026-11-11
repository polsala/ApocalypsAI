# Nightly Safehouse S3 Bucket

Creates an S3 bucket configured for post‑apocalyptic data hoarding: versioning enabled, server‑side encryption with AES‑256, and a lifecycle rule that expires objects after 30 days. Ideal for storing survival manuals, ration logs, etc.

## Usage

```hcl
module "safehouse_bucket" {
  source      = "./src"
  bucket_name = "my-safehouse-bucket"
}
```

## Inputs

- `bucket_name` (string, required): Name of the bucket.

## Outputs

- `bucket_id`: The ID of the created bucket.

## Testing

Run the validation script to ensure the module is syntactically correct:

```bash
cd tests && ./validate.sh
```
