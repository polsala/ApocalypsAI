# Nightly Safehouse S3

Terraform module that creates an S3 bucket with server‑side encryption, versioning, and a lifecycle rule that deletes non‑current versions after 30 days. Ideal for storing critical post‑apocalyptic data.

## Usage

```hcl
module "safehouse_s3" {
  source      = "./src"
  bucket_name = "my-safehouse-bucket"
}
```

## Variables

- `bucket_name` (string, required): Name of the S3 bucket.

## Outputs

- `bucket_id` – The ID of the created bucket.
- `bucket_arn` – The ARN of the bucket.

## Testing

Run the provided test suite (it mocks Terraform commands, so no network is required):

```sh
cd tests && python -m unittest test_module.py
```
