# Nightly Safehouse S3 Module

Creates an S3 bucket configured as a post‑apocalyptic safe‑house: versioning enabled, server‑side encryption with AES‑256, and a lifecycle rule that expires objects after 30 days. The module is provider‑agnostic; you can use any S3‑compatible provider (AWS, MinIO, etc.) and works with Terraform 1.5+.

## Usage

```hcl
module "safehouse" {
  source      = "./"
  bucket_name = "my-safehouse-bucket"
}
```

## Inputs

- `bucket_name` (string, required): Name of the bucket.

## Outputs

- `bucket_arn` (string): ARN of the created bucket.

## Testing

Run the included test script:

```sh
cd tests && ./test_validate.sh
```
