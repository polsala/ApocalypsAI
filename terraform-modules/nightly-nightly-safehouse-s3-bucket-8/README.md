# Safehouse S3 Bucket

A whimsical Terraform module that provisions an S3 bucket named for a post‑apocalyptic safe‑house. The bucket has versioning enabled, server‑side encryption (AES‑256), and a lifecycle rule that expires objects after 30 days. Ideal for storing survival guides, ration logs, or any other end‑of‑the‑world data.

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

- `bucket_arn` – ARN of the created bucket.

## Testing

Run `./tests/validate.sh` from the module root. The script runs `terraform init`, `terraform validate`, and `terraform plan` with a local backend and the `null` provider to ensure the configuration is syntactically correct.
