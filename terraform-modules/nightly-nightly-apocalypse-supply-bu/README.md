# Apocalypse Supply Bucket

A whimsical Terraform module that provisions a secure S3 bucket named "apocalypse-supply-<random>" with versioning, server‑side encryption, and a lifecycle rule that deletes objects older than 30 days. It also creates an initial placeholder object `supply-list.txt` containing a fun list of survival items.

## Usage

```hcl
module "supply_bucket" {
  source = "git::https://github.com/yourorg/apocalypsai.git//terraform-modules/nightly-apocalypse-supply-bucket"
  bucket_name_prefix = "apocalypse-supply"
}
```

## Inputs

- `bucket_name_prefix` (string): Prefix for bucket name. Default `"apocalypse-supply"`.

## Outputs

- `bucket_name` – The name of the created bucket.
- `supply_object_key` – Key of the placeholder object.

## Requirements

- Terraform >= 1.0
- AWS provider configured.

## Testing

Run the test script to validate the module locally:

```bash
bash tests/test_main.sh
```
