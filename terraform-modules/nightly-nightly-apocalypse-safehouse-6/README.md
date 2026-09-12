# Apocalypse Safehouse S3 Bucket

A whimsical Terraform module that provisions a secure S3 bucket for storing post‑apocalyptic supplies. The bucket has versioning, server‑side encryption, and a lifecycle rule that automatically deletes objects older than 30 days.

## Usage

```hcl
module "safehouse" {
  source      = "git::https://github.com/yourorg/apocalypsai.git//terraform-modules/nightly-apocalypse-safehouse-s3"
  bucket_name = "my‑safehouse‑bucket"
}
```

## Inputs

- `bucket_name` (string) – Name of the S3 bucket. Defaults to `apocalypse-safehouse`.

## Outputs

- `bucket_id` – The ID of the created bucket.

## Testing

Run the provided test script:

```sh
cd terraform-modules/nightly-apocalypse-safehouse-s3
bash tests/test_safehouse.sh
```
