# Nightly Safehouse S3 Bucket

Creates an S3 bucket configured for post‑apocalyptic data hoarding: versioning enabled, server‑side encryption (AES‑256), and a lifecycle rule that expires objects after 30 days. Ideal for storing backups of survivor logs.

## Usage

```hcl
module "safehouse" {
  source      = "./"
  bucket_name = "survivor-logs"
}
```

Run `terraform init` and then `terraform apply`.

## Inputs

- **bucket_name** *(string)* – Name of the bucket (must be globally unique).

## Outputs

- **bucket_arn** – ARN of the created bucket.

## Testing

Execute the test script to ensure the module validates and contains the expected resources:

```bash
bash tests/test_module.sh
```
