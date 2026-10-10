# Nightly Safehouse S3 Bucket

Utility that provisions an S3 bucket configured as a post‑apocalyptic safe‑house: versioning enabled, server‑side encryption with AWS‑managed keys, and a lifecycle rule that expires objects older than 30 days. The module is self‑contained and can be used in any Terraform configuration.

## Usage

```hcl
module "safehouse" {
  source      = "./src"
  bucket_name = "my-safehouse-bucket"
}
```

## Inputs

- `bucket_name` (string, required): Name of the S3 bucket.

## Outputs

- `bucket_arn` – ARN of the created bucket.

## Testing

Run the following command to execute the offline tests:

```bash
bash tests/test_module.sh
```
