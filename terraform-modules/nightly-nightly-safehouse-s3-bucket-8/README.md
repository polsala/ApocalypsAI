# Safehouse S3 Bucket

A whimsical Terraform module that provisions a secure S3 bucket for storing post‑apocalyptic supplies. The bucket has versioning, server‑side encryption, and a lifecycle rule that automatically deletes objects older than 30 days.

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

Run the provided Bash test:

```sh
cd tests && ./test_main.sh
```
