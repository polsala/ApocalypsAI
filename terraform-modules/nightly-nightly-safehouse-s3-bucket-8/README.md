# nightly-safehouse-s3-bucket

Creates an S3 bucket configured as a post‑apocalyptic safe‑house: versioning enabled, server‑side encryption, and a lifecycle rule that deletes objects older than 365 days. The module is provider‑agnostic; it only requires the AWS provider.

## Usage

```hcl
module "safehouse" {
  source      = "./utils/terraform-modules/nightly-safehouse-s3-bucket"
  bucket_name = "my-safe-house"
}
```

## Inputs

- `bucket_name` (string, required): Name of the bucket.

## Outputs

- `bucket_arn` – ARN of the created bucket.

## Testing

Run the validation script to ensure the module syntax is correct:

```sh
cd tests && ./validate.sh
```
