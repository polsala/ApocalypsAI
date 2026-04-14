# Safehouse S3 Bucket

A whimsical Terraform module that provisions an AWS S3 bucket configured as a post‑apocalyptic safe‑house: versioning enabled, server‑side encryption, and a lifecycle rule that deletes objects older than 30 days. Ideal for storing survival manuals, ration logs, or encrypted whispers.

## Usage

```hcl
module "safehouse" {
  source = "./src"

  bucket_name = "my-safehouse-bucket"
}
```

## Inputs

- `bucket_name` (string, required): Name of the S3 bucket.

## Outputs

- `bucket_arn` – ARN of the created bucket.

## Testing

Run the provided test script:

```sh
cd tests && ./validate.sh
```
